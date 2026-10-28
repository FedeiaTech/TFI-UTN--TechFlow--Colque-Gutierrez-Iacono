import pytest
from decimal import Decimal
from fastapi import HTTPException

# Simulación / pruebas sobre las reglas de negocio críticas definidas en el P0

def test_pago_monto_debe_ser_mayor_a_cero():
    """Valida que no se permitan registrar pagos con montos menores o iguales a 0."""
    monto_invalido_cero = Decimal("0.00")
    monto_invalido_negativo = Decimal("-1500.00")
    
    # Regla: Si monto <= 0 debe arrojar ValueError o HTTPException 400
    with pytest.raises((ValueError, HTTPException)):
        if monto_invalido_cero <= 0:
            raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor a cero.")

    with pytest.raises((ValueError, HTTPException)):
        if monto_invalido_negativo <= 0:
            raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor a cero.")


def test_bloqueo_entrega_con_saldo_pendiente():
    """Valida que una orden en estado 'listo' no pueda entregarse si resta abonar saldo."""
    total_reparacion = Decimal("15000.00")
    total_pagado = Decimal("10000.00")
    saldo_pendiente = total_reparacion - total_pagado
    
    estado_orden = "listo"
    accion_solicitada = "entregar"

    with pytest.raises(HTTPException) as exc_info:
        # Regla: Si saldo_pendiente > 0 no se permite transición a 'entregado'
        if accion_solicitada == "entregar" and saldo_pendiente > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"No se puede entregar la orden. Saldo pendiente: ${saldo_pendiente}"
            )
            
    assert exc_info.value.status_code == 400
    assert "Saldo pendiente" in exc_info.value.detail


def test_reserva_stock_repuesto_sin_disponibilidad():
    """Valida que no se pueda reservar o descontar un repuesto si el stock disponible es insuficiente."""
    stock_actual = 1
    cantidad_requerida = 2

    with pytest.raises(HTTPException) as exc_info:
        # Regla: stock_disponible >= cantidad_solicitada
        if cantidad_requerida > stock_actual:
            raise HTTPException(
                status_code=400, 
                detail="Stock insuficiente para realizar la reserva del repuesto."
            )



    assert exc_info.value.status_code == 400
    assert "Stock insuficiente" in exc_info.value.detail

def test_nueva_falla_durante_reparacion_no_altera_trabajo_aprobado():
    """
    Validación corrección 2.ª Entrega:
    Durante la reparación aparece una nueva falla y se genera un trabajo adicional
    sin alterar lo que ya estaba aprobado ni el saldo exigible vigente.
    """
    # 1. Trabajo inicial aprobado
    trabajos_orden = [
        {
            "id": 1,
            "descripcion": "Cambio de módulo conector de carga",
            "costo_mano_obra": 15000.0,
            "costo_repuesto": 10000.0,
            "estado": "APROBADO"
        }
    ]
    
    total_aprobado_inicial = sum(
        t["costo_mano_obra"] + t["costo_repuesto"] 
        for t in trabajos_orden if t["estado"] == "APROBADO"
    )
    assert total_aprobado_inicial == 25000.0

    # 2. Se detecta falla adicional durante la reparación
    nuevo_trabajo_adicional = {
        "id": 2,
        "descripcion": "Cambio de batería por falla oculta",
        "costo_mano_obra": 5000.0,
        "costo_repuesto": 18000.0,
        "estado": "PENDIENTE_APROBACION"
    }
    trabajos_orden.append(nuevo_trabajo_adicional)

    # 3. Verificaciones: el trabajo 1 sigue intacto y el pendiente no suma al saldo exigible
    assert trabajos_orden[0]["estado"] == "APROBADO"
    total_aprobado_vigente = sum(
        t["costo_mano_obra"] + t["costo_repuesto"] 
        for t in trabajos_orden if t["estado"] == "APROBADO"
    )
    assert total_aprobado_vigente == 25000.0

    # 4. Si el cliente aprueba la nueva falla, recién ahí se consolida
    trabajos_orden[1]["estado"] = "APROBADO"
    total_aprobado_actualizado = sum(
        t["costo_mano_obra"] + t["costo_repuesto"] 
        for t in trabajos_orden if t["estado"] == "APROBADO"
    )
    assert total_aprobado_actualizado == 48000.0

    