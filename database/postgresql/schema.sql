-- TechFlow — Esquema P0 (PostgreSQL)
-- Alcance: ciclo cliente -> equipo -> orden -> trabajos -> diagnóstico ->
-- cotización -> aprobación/rechazo -> reserva -> reparación -> listo -> pago -> entrega.
-- Fuente de las reglas de negocio: entrega-2/Caso-Completo-Reparacion.md, sección 4.
--
-- Modelo en una línea: una orden agrupa uno o más trabajos; cada trabajo tiene su
-- propio estado técnico y sus cotizaciones independientes (nunca versiones completas);
-- el total de la orden es la suma de las cotizaciones aprobadas. Los totales, el saldo
-- y el estado de pago NO se guardan: se derivan en vistas para que no se editen a mano.

-- ---------------------------------------------------------------------------
-- Tipos enumerados
-- ---------------------------------------------------------------------------

-- Estado global SIMPLE de la orden. El detalle técnico vive en cada trabajo.
CREATE TYPE estado_orden AS ENUM (
    'recibido',
    'en_proceso',
    'listo',
    'listo_no_retirado',
    'entregado'
);

-- Resultado de la orden; se fija al pasar a 'listo'. El cierre sin reparación
-- (todo rechazado o irreparable) llega a 'listo' con 'sin_reparacion' y luego a
-- 'entregado', sin pasar por estados de reparación.
CREATE TYPE resultado_orden AS ENUM (
    'reparado',
    'parcial',
    'sin_reparacion'
);

CREATE TYPE estado_tecnico_trabajo AS ENUM (
    'pendiente_diagnostico',
    'diagnosticado',
    'esperando_repuesto',
    'en_reparacion',
    'terminado',
    'irreparable',
    'cancelado'
);

CREATE TYPE estado_cotizacion AS ENUM (
    'pendiente',
    'aprobada',
    'rechazada',
    'reemplazada'
);

CREATE TYPE tipo_item_cotizacion AS ENUM (
    'repuesto',
    'mano_obra',
    'descripcion'
);

-- 'disponible' no es un estado de la reserva: la disponibilidad se calcula
-- (stock_total menos reservas en estado 'reservada', ver v_repuesto_disponibilidad).
CREATE TYPE estado_reserva AS ENUM (
    'reservada',
    'utilizada',
    'liberada'
);

-- ---------------------------------------------------------------------------
-- Identidad y datos maestros
-- ---------------------------------------------------------------------------

-- Identidad mínima para autenticación (OAuth2 + JWT) y trazabilidad.
-- La matriz de roles queda fuera del P0 (ver Modulos-P0.md).
CREATE TABLE usuarios (
    id BIGSERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL, -- solo el hash; nunca la contraseña
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE clientes (
    id BIGSERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Solo datos estables del dispositivo. El estado físico y los accesorios cambian
-- en cada ingreso, por eso viven en la orden. Un mismo equipo puede volver en
-- órdenes distintas (reincidencia de falla, nueva falla, etc.).
CREATE TABLE equipos (
    id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL REFERENCES clientes(id),
    tipo TEXT NOT NULL, -- celular, notebook, consola, etc. (categoría genérica)
    marca TEXT,
    modelo TEXT NOT NULL,
    numero_serie TEXT, -- genérico: sirve para cualquier tipo de equipo
    imei TEXT,         -- opcional: solo aplica a celulares
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE categorias_repuesto (
    id BIGSERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE repuestos (
    id BIGSERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria_id BIGINT NOT NULL REFERENCES categorias_repuesto(id),
    stock_total INT NOT NULL DEFAULT 0 CHECK (stock_total >= 0),
    -- Solo referencia del catálogo. El precio efectivamente cotizado se guarda
    -- como snapshot en cotizacion_items.precio_unitario.
    precio_referencia NUMERIC(12, 2) CHECK (precio_referencia >= 0)
);

-- ---------------------------------------------------------------------------
-- Orden y trabajos
-- ---------------------------------------------------------------------------

CREATE TABLE ordenes (
    id BIGSERIAL PRIMARY KEY,
    equipo_id BIGINT NOT NULL REFERENCES equipos(id),
    tecnico_id BIGINT NOT NULL REFERENCES usuarios(id), -- técnico responsable
    falla_reportada TEXT NOT NULL,
    estado_fisico_ingreso TEXT NOT NULL, -- constancia de daños preexistentes en este ingreso
    accesorios_entregados TEXT,          -- accesorios que el cliente deja en este ingreso
    -- Estado global simple. El estado de pago NO se almacena: se deriva en
    -- v_orden_saldo (regla 4 del caso completo).
    estado estado_orden NOT NULL DEFAULT 'recibido',
    resultado resultado_orden, -- se fija al pasar a 'listo'
    fecha_listo TIMESTAMPTZ,
    fecha_primer_aviso_no_retirado TIMESTAMPTZ,
    fecha_segundo_aviso_no_retirado TIMESTAMPTZ,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- El resultado existe solo desde que la orden está lista.
    CONSTRAINT ck_ordenes_resultado_segun_estado CHECK (
        (estado IN ('recibido', 'en_proceso') AND resultado IS NULL)
        OR (estado IN ('listo', 'listo_no_retirado', 'entregado') AND resultado IS NOT NULL)
    )
);

-- Un trabajo es una falla/tarea concreta dentro de la orden, con su propio
-- diagnóstico y estado técnico. Una falla nueva durante la reparación es un
-- trabajo nuevo: no bloquea los trabajos ya aprobados (regla 3).
-- La decisión del cliente NO se guarda aquí: se deriva de la cotización
-- vigente del trabajo (ver v_trabajo_decision_cliente).
CREATE TABLE trabajos (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes(id),
    descripcion TEXT NOT NULL, -- hallazgo o falla que origina el trabajo
    diagnostico TEXT,
    estado_tecnico estado_tecnico_trabajo NOT NULL DEFAULT 'pendiente_diagnostico',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Cotizaciones
-- ---------------------------------------------------------------------------

-- Cotizaciones independientes por trabajo (no versiones completas de la orden).
-- Nunca se borran: una rechazada o reemplazada queda en el historial (regla 1).
-- El total de la orden es la suma de las cotizaciones aprobadas.
CREATE TABLE cotizaciones (
    id BIGSERIAL PRIMARY KEY,
    trabajo_id BIGINT NOT NULL REFERENCES trabajos(id),
    numero INT NOT NULL CHECK (numero > 0), -- secuencial por trabajo (1, 2, ...)
    estado estado_cotizacion NOT NULL DEFAULT 'pendiente',
    motivo_rechazo TEXT,
    creada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    decidida_en TIMESTAMPTZ,
    UNIQUE (trabajo_id, numero)
);

-- Solo una cotización vigente (pendiente o aprobada) por trabajo. El trabajo
-- adicional de una falla nueva se modela como otro trabajo, no como segunda
-- cotización vigente del mismo.
CREATE UNIQUE INDEX uq_cotizaciones_vigente_por_trabajo
    ON cotizaciones(trabajo_id)
    WHERE estado IN ('pendiente', 'aprobada');

-- Ítems de una cotización. precio_unitario es un SNAPSHOT del precio aplicado:
-- cambios posteriores en repuestos.precio_referencia no alteran cotizaciones previas.
-- No hay columna de total: ver v_cotizacion_totales.
CREATE TABLE cotizacion_items (
    id BIGSERIAL PRIMARY KEY,
    cotizacion_id BIGINT NOT NULL REFERENCES cotizaciones(id),
    tipo tipo_item_cotizacion NOT NULL,
    descripcion TEXT NOT NULL,
    repuesto_id BIGINT REFERENCES repuestos(id),
    cantidad INT NOT NULL DEFAULT 1 CHECK (cantidad > 0),
    precio_unitario NUMERIC(12, 2) NOT NULL CHECK (precio_unitario >= 0),
    -- Un ítem de tipo 'repuesto' referencia el catálogo; los demás no.
    CONSTRAINT ck_cotizacion_items_repuesto CHECK (
        (tipo = 'repuesto' AND repuesto_id IS NOT NULL)
        OR (tipo <> 'repuesto' AND repuesto_id IS NULL)
    )
);

-- ---------------------------------------------------------------------------
-- Reservas de repuestos
-- ---------------------------------------------------------------------------

-- Un ítem de cotización de tipo repuesto genera una reserva (regla 2).
-- Ciclo: reservada -> utilizada (el técnico confirma el uso) o reservada -> liberada
-- (rechazo de la cotización, cancelación o decisión manual del técnico).
--
-- IMPORTANTE (transacciones, responsabilidad del backend):
--  * Pasar la reserva de 'reservada' a 'utilizada' y decrementar
--    repuestos.stock_total debe ocurrir en la MISMA transacción.
--  * La reserva concurrente se resuelve con bloqueo de fila: el backend ejecuta
--    SELECT ... FROM repuestos WHERE id = ... FOR UPDATE, verifica la disponibilidad
--    (v_repuesto_disponibilidad) y recién entonces inserta la reserva.
CREATE TABLE repuesto_reservas (
    id BIGSERIAL PRIMARY KEY,
    cotizacion_item_id BIGINT NOT NULL REFERENCES cotizacion_items(id),
    repuesto_id BIGINT NOT NULL REFERENCES repuestos(id),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    estado estado_reserva NOT NULL DEFAULT 'reservada',
    reservada_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    utilizada_en TIMESTAMPTZ,
    liberada_en TIMESTAMPTZ,
    UNIQUE (cotizacion_item_id)
);

-- ---------------------------------------------------------------------------
-- Pagos
-- ---------------------------------------------------------------------------

-- Pagos registrados por orden. Sin cuenta corriente en el P0.
CREATE TABLE pagos (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes(id),
    monto NUMERIC(12, 2) NOT NULL CHECK (monto > 0),
    registrado_por BIGINT NOT NULL REFERENCES usuarios(id),
    pagado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Historial de estados (simple, sin arquitectura de eventos)
-- ---------------------------------------------------------------------------

-- usuario_id es NULL solo para transiciones automáticas del sistema
-- (por ejemplo, el paso a 'listo_no_retirado' a los 30 días).
CREATE TABLE historial_estados_orden (
    id BIGSERIAL PRIMARY KEY,
    entidad_id BIGINT NOT NULL REFERENCES ordenes(id),
    estado_anterior estado_orden,
    estado_nuevo estado_orden NOT NULL,
    usuario_id BIGINT REFERENCES usuarios(id),
    motivo TEXT,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE historial_estados_trabajo (
    id BIGSERIAL PRIMARY KEY,
    entidad_id BIGINT NOT NULL REFERENCES trabajos(id),
    estado_anterior estado_tecnico_trabajo,
    estado_nuevo estado_tecnico_trabajo NOT NULL,
    usuario_id BIGINT REFERENCES usuarios(id),
    motivo TEXT,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Índices
-- ---------------------------------------------------------------------------

CREATE INDEX idx_equipos_cliente ON equipos(cliente_id);
CREATE INDEX idx_repuestos_categoria ON repuestos(categoria_id);
CREATE INDEX idx_ordenes_equipo ON ordenes(equipo_id);
CREATE INDEX idx_ordenes_tecnico ON ordenes(tecnico_id);
CREATE INDEX idx_ordenes_estado ON ordenes(estado);
CREATE INDEX idx_trabajos_orden ON trabajos(orden_id);
CREATE INDEX idx_trabajos_estado_tecnico ON trabajos(estado_tecnico);
CREATE INDEX idx_cotizaciones_trabajo ON cotizaciones(trabajo_id);
CREATE INDEX idx_cotizacion_items_cotizacion ON cotizacion_items(cotizacion_id);
CREATE INDEX idx_cotizacion_items_repuesto ON cotizacion_items(repuesto_id);
CREATE INDEX idx_reservas_repuesto_estado ON repuesto_reservas(repuesto_id, estado);
CREATE INDEX idx_pagos_orden ON pagos(orden_id);
CREATE INDEX idx_pagos_registrado_por ON pagos(registrado_por);
CREATE INDEX idx_historial_orden_entidad ON historial_estados_orden(entidad_id, creado_en);
CREATE INDEX idx_historial_trabajo_entidad ON historial_estados_trabajo(entidad_id, creado_en);

-- ---------------------------------------------------------------------------
-- Vistas derivadas (el saldo y el estado de pago no son editables a mano)
-- ---------------------------------------------------------------------------

-- Total de cada cotización = suma de cantidad * precio_unitario de sus ítems.
CREATE VIEW v_cotizacion_totales AS
SELECT
    c.id AS cotizacion_id,
    c.trabajo_id,
    t.orden_id,
    c.numero,
    c.estado,
    COALESCE(SUM(i.cantidad * i.precio_unitario), 0)::NUMERIC(12, 2) AS total
FROM cotizaciones c
JOIN trabajos t ON t.id = c.trabajo_id
LEFT JOIN cotizacion_items i ON i.cotizacion_id = c.id
GROUP BY c.id, c.trabajo_id, t.orden_id, c.numero, c.estado;

-- Saldo de la orden: total aprobado (suma de cotizaciones aprobadas), total
-- pagado, saldo y estado de pago derivado. La regla "no entregar con saldo
-- pendiente" se valida en el backend consultando esta vista (regla 8).
CREATE VIEW v_orden_saldo AS
SELECT
    o.id AS orden_id,
    a.total_aprobado,
    p.total_pagado,
    (a.total_aprobado - p.total_pagado)::NUMERIC(12, 2) AS saldo,
    CASE
        WHEN p.total_pagado = 0 THEN 'pendiente'
        WHEN p.total_pagado < a.total_aprobado THEN 'parcial'
        ELSE 'pagado'
    END AS estado_pago
FROM ordenes o
CROSS JOIN LATERAL (
    SELECT COALESCE(SUM(ct.total), 0)::NUMERIC(12, 2) AS total_aprobado
    FROM v_cotizacion_totales ct
    WHERE ct.orden_id = o.id AND ct.estado = 'aprobada'
) a
CROSS JOIN LATERAL (
    SELECT COALESCE(SUM(pg.monto), 0)::NUMERIC(12, 2) AS total_pagado
    FROM pagos pg
    WHERE pg.orden_id = o.id
) p;

-- Decisión del cliente por trabajo, derivada de la última cotización del trabajo
-- (la vigente, o la última decidida si no hay vigente).
CREATE VIEW v_trabajo_decision_cliente AS
SELECT
    t.id AS trabajo_id,
    t.orden_id,
    COALESCE(u.estado::TEXT, 'sin_cotizacion') AS decision_cliente
FROM trabajos t
LEFT JOIN LATERAL (
    SELECT c.estado
    FROM cotizaciones c
    WHERE c.trabajo_id = t.id
    ORDER BY c.numero DESC
    LIMIT 1
) u ON TRUE;

-- Disponibilidad efectiva = stock_total menos reservas en estado 'reservada'.
-- Las reservas 'utilizada' ya descontaron stock_total; las 'liberada' no cuentan.
CREATE VIEW v_repuesto_disponibilidad AS
SELECT
    r.id AS repuesto_id,
    r.stock_total,
    COALESCE(SUM(rr.cantidad) FILTER (WHERE rr.estado = 'reservada'), 0)::INT AS reservado,
    (r.stock_total
        - COALESCE(SUM(rr.cantidad) FILTER (WHERE rr.estado = 'reservada'), 0))::INT AS disponible
FROM repuestos r
LEFT JOIN repuesto_reservas rr ON rr.repuesto_id = r.id
GROUP BY r.id, r.stock_total;

-- ---------------------------------------------------------------------------
-- Notas
-- ---------------------------------------------------------------------------
-- * PIN/contraseña del equipo no se modela como columna persistente (regla 5);
--   si el diagnóstico lo requiere, se maneja fuera de la base.
-- * Reglas que NO se resuelven en el DDL, sino en el backend (con test obligatorio,
--   ver Esquema-Base-Datos.md): una orden no pasa a 'entregado' con saldo pendiente;
--   la orden pasa a 'listo' solo cuando todos sus trabajos están en estado terminal
--   (terminado, irreparable o cancelado); una cotización sin respuesta queda
--   'pendiente' y su reserva se libera por decisión manual del técnico.
