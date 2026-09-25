-- TechFlow — Esquema P0 (PostgreSQL)
-- Alcance: ciclo cliente -> equipo -> orden -> diagnóstico -> presupuesto ->
-- aprobación/rechazo -> reparación -> listo -> entrega.
-- Fuente de las reglas de negocio: entrega-2/Caso-Completo-Reparacion.md, sección 4.

CREATE TYPE estado_orden AS ENUM (
    'recibido',
    'diagnosticado',
    'presupuestado',
    'esperando_aprobacion_adicional',
    'aprobado',
    'esperando_repuesto',
    'en_reparacion',
    'listo',
    'listo_no_retirado',
    'entregado'
);

CREATE TYPE estado_pago AS ENUM (
    'pendiente',
    'parcial',
    'pagado'
);

CREATE TYPE estado_item_presupuesto AS ENUM (
    'pendiente',
    'aprobado',
    'rechazado'
);

CREATE TYPE estado_repuesto AS ENUM (
    'disponible',
    'reservado',
    'utilizado'
);

CREATE TABLE clientes (
    id BIGSERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Un cliente puede traer más de un equipo, y un mismo equipo puede volver
-- en órdenes distintas (reincidencia de falla, nueva falla, etc.).
CREATE TABLE equipos (
    id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL REFERENCES clientes(id),
    tipo TEXT NOT NULL, -- celular, notebook, consola, etc. (categoría genérica)
    modelo TEXT NOT NULL,
    imei TEXT,
    estado_fisico_ingreso TEXT NOT NULL, -- constancia de daños preexistentes
    accesorios_entregados TEXT,
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
    stock_total INT NOT NULL DEFAULT 0
);

CREATE TABLE ordenes (
    id BIGSERIAL PRIMARY KEY,
    equipo_id BIGINT NOT NULL REFERENCES equipos(id),
    falla_reportada TEXT NOT NULL,
    diagnostico TEXT,
    repuesto_sugerido_id BIGINT REFERENCES repuestos(id),
    -- Estado técnico y estado de pago son campos separados: nunca combinar
    -- "entregado/cobrado" en un único estado (regla 4 del caso completo).
    estado estado_orden NOT NULL DEFAULT 'recibido',
    estado_pago estado_pago NOT NULL DEFAULT 'pendiente',
    fecha_listo TIMESTAMPTZ,
    fecha_primer_aviso_no_retirado TIMESTAMPTZ,
    fecha_segundo_aviso_no_retirado TIMESTAMPTZ,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Presupuestos versionados por orden: un presupuesto rechazado o
-- reemplazado nunca se borra, queda en el historial (regla 1).
CREATE TABLE presupuestos (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes(id),
    version INT NOT NULL,
    total NUMERIC(12, 2) NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (orden_id, version)
);

-- Ítems de un presupuesto: permite aprobar el cambio de conector y
-- rechazar el altavoz sin afectar el resto de la misma orden (regla 3).
CREATE TABLE presupuesto_items (
    id BIGSERIAL PRIMARY KEY,
    presupuesto_id BIGINT NOT NULL REFERENCES presupuestos(id),
    descripcion TEXT NOT NULL,
    repuesto_id BIGINT REFERENCES repuestos(id),
    mano_obra NUMERIC(12, 2) NOT NULL DEFAULT 0,
    estado estado_item_presupuesto NOT NULL DEFAULT 'pendiente',
    motivo_rechazo TEXT
);

-- Un repuesto asociado a un ítem de presupuesto queda "reservado" y sólo
-- se descuenta de stock_total cuando el técnico confirma su uso (regla 2).
CREATE TABLE repuesto_reservas (
    id BIGSERIAL PRIMARY KEY,
    presupuesto_item_id BIGINT NOT NULL REFERENCES presupuesto_items(id),
    repuesto_id BIGINT NOT NULL REFERENCES repuestos(id),
    estado estado_repuesto NOT NULL DEFAULT 'reservado',
    utilizado_en TIMESTAMPTZ
);

-- Pagos registrados por orden. Sin cuenta corriente en el P0: el saldo
-- pendiente se calcula como total del presupuesto vigente menos pagos.
CREATE TABLE pagos (
    id BIGSERIAL PRIMARY KEY,
    orden_id BIGINT NOT NULL REFERENCES ordenes(id),
    monto NUMERIC(12, 2) NOT NULL,
    pagado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_equipos_cliente ON equipos(cliente_id);
CREATE INDEX idx_ordenes_equipo ON ordenes(equipo_id);
CREATE INDEX idx_presupuestos_orden ON presupuestos(orden_id);
CREATE INDEX idx_presupuesto_items_presupuesto ON presupuesto_items(presupuesto_id);
CREATE INDEX idx_pagos_orden ON pagos(orden_id);
CREATE INDEX idx_ordenes_estado ON ordenes(estado);

-- Nota: PIN/contraseña del equipo no se modela como columna persistente
-- (regla 5); si el diagnóstico lo requiere, se maneja fuera de la base.
