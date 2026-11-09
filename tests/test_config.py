"""Tests for application configuration."""
import pytest
from sqlalchemy import create_engine

from app.config import _normalize_database_url


@pytest.mark.parametrize(
    "database_url",
    [
        "postgres://example.invalid/education",
        "postgresql://example.invalid/education",
    ],
)
def test_postgres_urls_use_installed_psycopg2_driver(monkeypatch, database_url):
    monkeypatch.setenv("DATABASE_URL", database_url)

    engine = create_engine(_normalize_database_url("sqlite:///education.db"))
    try:
        assert engine.dialect.driver == "psycopg2"
    finally:
        engine.dispose()


def test_default_database_url_remains_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    assert _normalize_database_url("sqlite:///education.db") == "sqlite:///education.db"
