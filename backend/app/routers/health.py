import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database.session import get_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/db")
def health_db() -> dict[str, str]:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        # Log only the exception type: messages may embed connection details.
        logger.warning("Database health check failed: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok"}
