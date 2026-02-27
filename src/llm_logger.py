import atexit
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)
atexit.register(lambda: logger.info("App shutting down"))

_DB_PATH = Path("data/logs/history.db")


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_logs (
            id INTEGER PRIMARY KEY,
            ts TEXT,
            feature TEXT,
            resume_filename TEXT,
            model TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            duration_ms INTEGER,
            status TEXT,
            error_message TEXT
        )
    """)
    conn.commit()
    return conn


def log_llm_call(
    feature: str,
    model: str,
    duration_ms: int,
    status: str,
    resume_filename: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    error_message: str | None = None,
) -> None:
    conn = _get_conn()
    conn.execute(
        """
        INSERT INTO llm_logs
            (ts, feature, resume_filename, model, input_tokens, output_tokens, duration_ms, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            feature,
            resume_filename,
            model,
            input_tokens,
            output_tokens,
            duration_ms,
            status,
            error_message,
        ),
    )
    conn.commit()
    conn.close()
    logger.info(f"Logged LLM call: feature={feature} status={status} duration={duration_ms}ms")
