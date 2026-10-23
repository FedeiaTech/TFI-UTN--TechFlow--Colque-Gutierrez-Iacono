from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa compartida por todos los modelos. Las tablas ya existen
    en PostgreSQL (database/postgresql/schema.sql aplicado manualmente); estos
    modelos solo mapean, no gestionan migraciones."""
