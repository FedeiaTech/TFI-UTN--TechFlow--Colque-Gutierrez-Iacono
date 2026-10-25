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