from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import clientes, cotizaciones, health, ordenes, pagos
from app.services.errors import DomainError
from app.routers.auth import router as auth_router

app = FastAPI(title="TechFlow API")


@app.exception_handler(DomainError)
def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


app.include_router(health.router)
app.include_router(clientes.router)
app.include_router(ordenes.router)
app.include_router(cotizaciones.router)
app.include_router(pagos.router)
app.include_router(auth_router)
