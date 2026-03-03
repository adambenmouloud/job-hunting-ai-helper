import sqlite3
from unittest.mock import patch

from src.llm_logger import log_llm_call


def test_log_inserts_row(tmp_path):
    db_path = tmp_path / "logs" / "history.db"
    with patch("src.llm_logger._DB_PATH", db_path):
        log_llm_call(
            feature="full",
            model="claude-sonnet-4-6",
            duration_ms=500,
            status="success",
            provider="anthropic",
            resume_filename="resume.typ",
            input_tokens=100,
            output_tokens=50,
        )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM llm_logs").fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0]["resume_filename"] == "resume.typ"
    assert rows[0]["status"] == "success"
    assert rows[0]["provider"] == "anthropic"


def test_log_handles_none_fields(tmp_path):
    db_path = tmp_path / "logs" / "history.db"
    with patch("src.llm_logger._DB_PATH", db_path):
        log_llm_call(
            feature="score",
            model="claude-sonnet-4-6",
            duration_ms=200,
            status="error",
            error_message="timeout",
        )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM llm_logs").fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0]["error_message"] == "timeout"
    assert rows[0]["provider"] == "anthropic"  # default
