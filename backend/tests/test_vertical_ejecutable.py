"""Prueba de humo del vertical ejecutable: cliente -> equipo -> orden ->
trabajo -> diagnóstico -> cotización -> aprobación -> reserva -> confirmación
de uso -> orden lista -> pago -> entrega.

No reemplaza la suite de pruebas obligatorias (saldo pendiente, monto > 0,
reserva concurrente con stock = 1): esa queda a cargo de Brian según la
matriz RACI de docs/entrega-2/09-roles-y-organizacion-equipo.md. Esta prueba
solo demuestra que el recorrido completo funciona contra una base real.
"""

import os

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
                nombre="Técnico de prueba",
                email=f"tecnico-smoke-{os.urandom(4).hex()}@test.local",
                password_hash="x",
            )
            .returning(Usuario.id)
        )
        new_id = result.scalar_one()
        session.commit()
        return new_id


@pytest.fixture
def repuesto_id() -> int:
    with Session(get_engine()) as session:
        categoria_id = session.execute(
            insert(CategoriaRepuesto).values(nombre=f"Categoría smoke {os.urandom(4).hex()}").returning(
                CategoriaRepuesto.id
            )
        ).scalar_one()
        new_id = session.execute(
            insert(Repuesto)
            .values(nombre="Pantalla smoke test", categoria_id=categoria_id, stock_total=1, precio_referencia=100)
            .returning(Repuesto.id)
        ).scalar_one()
        session.commit()
        return new_id


def test_vertical_ejecutable_completo(usuario_id: int, repuesto_id: int):
    cliente = client.post("/api/v1/clientes", json={"nombre": "María", "telefono": "11-5555-5555"})
    assert cliente.status_code == 201
    cliente_id = cliente.json()["id"]

    equipo = client.post(
        f"/api/v1/clientes/{cliente_id}/equipos",
        json={"tipo": "celular", "marca": "Genérico", "modelo": "X1", "numero_serie": "SN-SMOKE-1"},
    )
    assert equipo.status_code == 201
    equipo_id = equipo.json()["id"]

    orden = client.post(
        "/api/v1/ordenes",
        json={
            "equipo_id": equipo_id,
            "tecnico_id": usuario_id,
            "falla_reportada": "No enciende",
            "estado_fisico_ingreso": "Sin daños visibles",
        },
    )
    assert orden.status_code == 201
    orden_data = orden.json()
    assert orden_data["estado"] == "recibido"
    orden_id = orden_data["id"]

    trabajo = client.post(
        f"/api/v1/ordenes/{orden_id}/trabajos",
        params={"usuario_id": usuario_id},
        json={"descripcion": "Reemplazo de pantalla"},
    )
    assert trabajo.status_code == 201
    trabajo_id = trabajo.json()["id"]

    diagnostico = client.patch(
        f"/api/v1/ordenes/trabajos/{trabajo_id}/diagnosticar",
        params={"usuario_id": usuario_id},
        json={"diagnostico": "Pantalla rota, requiere repuesto"},
    )
    assert diagnostico.status_code == 200
    assert diagnostico.json()["estado_tecnico"] == "diagnosticado"

    cotizacion = client.post(
        f"/api/v1/trabajos/{trabajo_id}/cotizaciones",
        params={"usuario_id": usuario_id},
        json={
            "items": [
                {
                    "tipo": "repuesto",
                    "descripcion": "Pantalla",
                    "repuesto_id": repuesto_id,
                    "cantidad": 1,
                    "precio_unitario": "15000.00",
                }
            ]
        },
    )
    assert cotizacion.status_code == 201
    cotizacion_id = cotizacion.json()["id"]

    decision = client.patch(
        f"/api/v1/cotizaciones/{cotizacion_id}/decidir",
        params={"usuario_id": usuario_id},
        json={"aprobar": True},
    )
    assert decision.status_code == 200
    assert decision.json()["estado"] == "aprobada"

    confirmar = client.post(
        f"/api/v1/trabajos/{trabajo_id}/confirmar-uso", params={"usuario_id": usuario_id}
    )
    assert confirmar.status_code == 204

    orden_lista = client.get(f"/api/v1/ordenes/{orden_id}/saldo")
    assert orden_lista.status_code == 200
    saldo = orden_lista.json()
    assert saldo["saldo"] == "15000.00"
    assert saldo["estado_pago"] == "pendiente"

    # Entregar antes de pagar debe fallar: regla 8, saldo pendiente bloquea entrega.
    entrega_bloqueada = client.patch(
        f"/api/v1/ordenes/{orden_id}/entregar", params={"usuario_id": usuario_id}
    )
    assert entrega_bloqueada.status_code == 400
    assert "saldo pendiente" in entrega_bloqueada.json()["detail"]

    pago = client.post(f"/api/v1/ordenes/{orden_id}/pagos", json={"monto": "15000.00", "registrado_por": usuario_id})
    assert pago.status_code == 201

    entrega = client.patch(f"/api/v1/ordenes/{orden_id}/entregar", params={"usuario_id": usuario_id})
    assert entrega.status_code == 200
    assert entrega.json()["estado"] == "entregado"
    assert entrega.json()["resultado"] == "reparado"
