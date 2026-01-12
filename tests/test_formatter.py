import json

from tracenest.core.formatter import format_log


def test_basic_log_format():
    line = format_log(
        level="info",
        message="hello",
        metadata={"a": 1},
    )

    data = json.loads(line)

    assert data["schema"] == "tracenest.v1"
    assert data["level"] == "INFO"
    assert data["msg"] == "hello"
    assert data["meta"]["a"] == 1
    assert "ts" in data


def test_large_message_is_truncated():
    msg = "x" * 100_000
    line = format_log(level="info", message=msg)
    data = json.loads(line)

    assert len(data["msg"]) < len(msg)


def test_invalid_metadata_is_safe():
    class Bad:
        pass

    line = format_log(
        level="info",
        message="test",
        metadata={"bad": Bad()},
    )

    data = json.loads(line)
    assert "bad" in data["meta"]


def test_exception_is_serialized():
    try:
        1 / 0
    except Exception as e:
        line = format_log(
            level="error",
            message="fail",
            exception=e,
        )

    data = json.loads(line)
    assert "exc" in data
    assert "stack" in data["exc"]
