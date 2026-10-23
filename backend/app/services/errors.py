class DomainError(Exception):
    """Violación de una regla de negocio (no un error de infraestructura).
    Los routers la traducen a HTTP 400/409 con el mensaje tal cual."""
