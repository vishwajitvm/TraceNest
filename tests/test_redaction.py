import pytest
from tracenest.security.redaction import redact_string, redact_dict, redact_list, redact_any

def test_redact_string_bearer():
    text = "Authorization: Bearer mysecrettoken123"
    result = redact_string(text)
    assert "mysecrettoken123" not in result
    assert "********" in result

def test_redact_string_key_value():
    text = "Connecting to DB with PASSWORD=supersecret&user=admin"
    result = redact_string(text)
    assert "supersecret" not in result
    assert "PASSWORD=********" in result

def test_redact_string_json():
    text = '{"username": "admin", "password": "mypassword123", "id": 1}'
    result = redact_string(text)
    assert "mypassword123" not in result
    assert "********" in result

def test_redact_string_db_url():
    text = "postgresql://user:mypassword@localhost:5432/mydb"
    result = redact_string(text)
    assert "mypassword" not in result
    assert "postgresql://user:********@localhost:5432/mydb" in result

def test_redact_dict():
    data = {
        "user": "admin",
        "password": "mypassword123",
        "nested": {
            "token": "secret_token",
            "public_key": "safe"
        }
    }
    result = redact_dict(data)
    assert result["user"] == "admin"
    assert result["password"] == "********"
    assert result["nested"]["token"] == "********"
    assert result["nested"]["public_key"] == "safe"

def test_redact_list():
    data = [
        "Authorization: Bearer secret",
        {"api_key": "12345"},
        "normal string"
    ]
    result = redact_list(data)
    assert result[0] == "Authorization: Bearer ********"
    assert result[1]["api_key"] == "********"
    assert result[2] == "normal string"

def test_redact_any():
    assert redact_any("password=123") == "password=********"
    assert redact_any({"api_key": "abc"}) == {"api_key": "********"}
    assert redact_any(["token=xyz"]) == ["token=********"]
    assert redact_any(123) == 123
