"""Tiny standalone smoke runner for rate-limit and ops helpers."""

from app import (
    _build_audit_query,
    _memory_rate_limit_retry_after,
    build_rate_limit_metrics_snapshot,
    get_rate_limit_mode,
)


def main() -> int:
    bucket = "smoke:rate-limit:127.0.0.1"
    base = 2000.0

    assert _memory_rate_limit_retry_after(bucket, 2, 30, base) == 0
    assert _memory_rate_limit_retry_after(bucket, 2, 30, base + 1) == 0
    assert _memory_rate_limit_retry_after(bucket, 2, 30, base + 2) > 0

    sql, params = _build_audit_query("history.delete", "admin", "", "example.com")
    assert "WHERE" in sql
    assert len(params) == 3

    snap = build_rate_limit_metrics_snapshot()
    assert "mode" in snap and "counters" in snap

    mode = get_rate_limit_mode()
    assert mode in {"memory", "redis"}
    print(f"RATE_LIMIT_MODE={mode}")
    print("SMOKE_RATE_LIMIT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

