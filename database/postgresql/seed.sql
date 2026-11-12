-- TechFlow — Datos de demostración (idempotente: se puede correr varias veces).
-- Carga lo que la API no expone por endpoint: un técnico y el catálogo de repuestos.
--
-- Cuenta demo pública: demo@example.com / demo1234 (example.com es un dominio reservado
-- para documentación; el login rechaza dominios especiales como .local)
-- Es una cuenta ficticia para la evaluación; no corresponde a ningún integrante.

INSERT INTO usuarios (nombre, email, password_hash)
VALUES ('Técnico Demo', 'demo@example.com',
        '$2b$12$i8z5C5tLnaSFI9wqDjwV3.Azlb1ErRInqY3zXgs6xtYLkkNe/iwL6')
ON CONFLICT (email) DO NOTHING;

INSERT INTO categorias_repuesto (nombre)
VALUES ('Pantallas'), ('Baterías'), ('Conectores')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO repuestos (nombre, categoria_id, stock_total, precio_referencia)
SELECT v.nombre, c.id, v.stock, v.precio
FROM (VALUES
    ('Pantalla Samsung A32',       'Pantallas',  3, 45000.00),
    ('Batería Motorola G60',       'Baterías',   5, 18000.00),
    ('Pin de carga USB-C genérico', 'Conectores', 1,  6000.00)
) AS v(nombre, categoria, stock, precio)
JOIN categorias_repuesto c ON c.nombre = v.categoria
WHERE NOT EXISTS (SELECT 1 FROM repuestos r WHERE r.nombre = v.nombre);
