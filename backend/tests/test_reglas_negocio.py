"""Suite de pruebas obligatorias para reglas de negocio P0 (Brian).
Cubre:
1. Monto de pago mayor a cero (HTTP 422).
2. Bloqueo de entrega con saldo pendiente (HTTP 400).
3. Reserva de repuesto sin disponibilidad suficiente (HTTP 400).
4. Concurrencia: dos reservas simultáneas sobre stock = 1 (solo una pasa).
"""

import os
import threading
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.database.session import get_engine
from app.main import app
from app.models import CategoriaRepuesto, Repuesto, Usuario

pytestmark = pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL not set")

client = TestClient(app)


@pytest.fixture
def usuario_id() -> int:
    with Session(get_engine()) as session:
        result = session.execute(
            insert(Usuario)
            .values(
                nombre="Técnico de prueba reglas",
                email=f"tecnico-reglas-{os.urandom(4).hex()}@test.local",
                password_hash="x",
            )
            .returning(Usuario.id)
        )
        new_id = result.scalar_one()
        session.commit()
        return new_id


@pytest.fixture
def repuesto_stock_uno_id() -> int:
    with Session(get_engine()) as session:
        categoria_id = session.execute(
            insert(CategoriaRepuesto)
            .values(nombre=f"Cat reglas {os.urandom(4).hex()}")
            .returning(CategoriaRepuesto.id)
        ).scalar_one()
        new_id = session.execute(
            insert(Repuesto)
            .values(
                nombre="Pin de carga stock 1",
                categoria_id=categoria_id,
                stock_total=1,
                precio_referencia=5000,
            )
            .returning(Repuesto.id)
        ).scalar_one()
        session.commit()
        return new_id


def _crear_orden_y_trabajo(usuario_id: int):
    """Crea cliente, equipo, orden y trabajo diagnosticado listo para cotizar."""
    cli = client.post("/api/v1/clientes", json={"nombre": "Cliente Reglas", "telefono": "11-4444-4444"})
    assert cli.status_code == 201
    cliente_id = cli.json()["id"]

    eq = client.post(
        f"/api/v1/clientes/{cliente_id}/equipos",
        json={"tipo": "celular", "marca": "Motorola", "modelo": "G52", "numero_serie": f"SN-{os.urandom(3).hex()}"},
    )
    assert eq.status_code == 201
    equipo_id = eq.json()["id"]

    ord_resp = client.post(
        "/api/v1/ordenes",
        json={
            "equipo_id": equipo_id,
            "tecnico_id": usuario_id,
            "falla_reportada": "Falla de prueba reglas",
            "estado_fisico_ingreso": "Bueno",
        },
    )
    assert ord_resp.status_code == 201
    orden_id = ord_resp.json()["id"]

    trab = client.post(
        f"/api/v1/ordenes/{orden_id}/trabajos",
        params={"usuario_id": usuario_id},
        json={"descripcion": "Reparación técnica"},
    )
    assert trab.status_code == 201
    trabajo_id = trab.json()["id"]

    diag = client.patch(
        f"/api/v1/ordenes/trabajos/{trabajo_id}/diagnosticar",
        params={"usuario_id": usuario_id},
        json={"diagnostico": "Revisado ok"},
    )
    assert diag.status_code == 200

    return orden_id, trabajo_id


def test_regla_pago_monto_debe_ser_mayor_a_cero():
    """Valida que la API rechace pagos con monto <= 0 devolviendo 422."""
    response = client.post("/api/v1/ordenes/1/pagos", json={"monto": 0})
    assert response.status_code == 422


def test_regla_bloqueo_entrega_con_saldo_pendiente(usuario_id: int, repuesto_stock_uno_id: int):
    """Valida que no se pueda entregar una orden con saldo pendiente (HTTP 400)."""
    orden_id, trabajo_id = _crear_orden_y_trabajo(usuario_id)

    # Cotizar
    cot = client.post(
        f"/api/v1/trabajos/{trabajo_id}/cotizaciones",
        params={"usuario_id": usuario_id},
        json={
            "items": [
                {
                    "tipo": "repuesto",
                    "descripcion": "Repuesto prueba",
                    "repuesto_id": repuesto_stock_uno_id,
                    "cantidad": 1,
                    "precio_unitario": "10000.00",
                }
            ]
        },
    )
    assert cot.status_code == 201
    cotizacion_id = cot.json()["id"]

    # Aprobar cotización
    dec = client.patch(
        f"/api/v1/cotizaciones/{cotizacion_id}/decidir",
        params={"usuario_id": usuario_id},
        json={"aprobar": True},
    )
    assert dec.status_code == 200

    # Confirmar uso -> pasa la orden a 'listo'
    conf = client.post(f"/api/v1/trabajos/{trabajo_id}/confirmar-uso", params={"usuario_id": usuario_id})
    assert conf.status_code == 204

    # Intentar entregar con saldo pendiente -> HTTP 400
    entrega = client.patch(f"/api/v1/ordenes/{orden_id}/entregar", params={"usuario_id": usuario_id})
    assert entrega.status_code == 400
    assert "saldo pendiente" in entrega.json()["detail"].lower()


def test_regla_reserva_repuesto_sin_disponibilidad(usuario_id: int, repuesto_stock_uno_id: int):
    """Valida el rechazo (HTTP 400) cuando la cantidad pedida supera la disponibilidad del repuesto."""
    _, trabajo_id = _crear_orden_y_trabajo(usuario_id)

    # El repuesto tiene stock 1, solicitamos 5 unidades
    response = client.post(
        f"/api/v1/trabajos/{trabajo_id}/cotizaciones",
        params={"usuario_id": usuario_id},
        json={
            "items": [
                {
                    "tipo": "repuesto",
                    "descripcion": "Repuesto excede stock",
                    "repuesto_id": repuesto_stock_uno_id,
                    "cantidad": 5,
                    "precio_unitario": "5000.00",
                }
            ]
        },
    )
    assert response.status_code == 400
    assert "disponibilidad" in response.json()["detail"].lower()


def test_regla_concurrencia_dos_reservas_simultaneas_stock_uno(usuario_id: int, repuesto_stock_uno_id: int):
    """Regla exigida por Oscar:
    Stock = 1 -> dos hilos concurrentes intentan reservar -> solo uno tiene éxito.
    """
    _, trabajo_id_1 = _crear_orden_y_trabajo(usuario_id)
    _, trabajo_id_2 = _crear_orden_y_trabajo(usuario_id)

    resultados = []

    def intentar_reserva(t_id: int):
        resp = client.post(
            f"/api/v1/trabajos/{t_id}/cotizaciones",
            params={"usuario_id": usuario_id},
            json={
                "items": [
                    {
                        "tipo": "repuesto",
                        "descripcion": "Reserva concurrente",
                        "repuesto_id": repuesto_stock_uno_id,
                        "cantidad": 1,
                        "precio_unitario": "5000.00",
                    }
                ]
            },
        )
        resultados.append(resp.status_code)

    h1 = threading.Thread(target=intentar_reserva, args=(trabajo_id_1,))
    h2 = threading.Thread(target=intentar_reserva, args=(trabajo_id_2,))

    h1.start()
    h2.start()
    h1.join()
    h2.join()

    # Como stock_total = 1, solo una puede dar 201 Created
    exitos = [c for c in resultados if c == 201]
    assert len(exitos) == 1, f"Fallo de concurrencia: pasaron {len(exitos)} de 2 (códigos: {resultados})"