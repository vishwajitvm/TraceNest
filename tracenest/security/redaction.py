"""
TraceNest Security Redaction Engine

Provides utilities for masking sensitive data (passwords, tokens, API keys) 
before they are written to logs or displayed in the UI.
"""

import re
from typing import Any, Dict, List, Tuple

from ..core.config import MASK_SECRETS, REDACTION_MASK, SENSITIVE_KEYS

# Compile regex patterns for raw string redaction
_PATTERNS = [
    # Authorization / Bearer tokens
    (re.compile(r'(?i)(authorization:\s*(?:bearer\s+)?)[^\s\'"]+'), r'\1' + REDACTION_MASK),
    # Key=Value secrets (e.g. PASSWORD=abc123)
    (re.compile(r'(?i)\b(?:' + '|'.join(SENSITIVE_KEYS) + r')\s*=\s*[^\s\'"&]+'), lambda m: m.group(0).split('=')[0] + '=' + REDACTION_MASK),
    # JSON-like / Dict-like secrets (e.g. "password": "abc123" or 'password': 'abc')
    (re.compile(r'(?i)([\'"])(?:' + '|'.join(SENSITIVE_KEYS) + r')\1\s*:\s*([\'"])[^\2]+?\2'), r'\1\g<1>:\s*\2' + REDACTION_MASK + r'\2'),
    # Database URIs with credentials (postgres, mysql, mongodb, redis, etc.)
    (re.compile(r'(?i)([a-z+]+://[^:]+:)[^@]+(@)'), r'\1' + REDACTION_MASK + r'\2'),
]

# Fix the JSON-like pattern to be safer and actually work properly:
_JSON_PATTERNS = [
    re.compile(r'(?i)([\'"](?:' + '|'.join(SENSITIVE_KEYS) + r')[\'"]\s*:\s*[\'"])(?:[^\'"]+)([\'"])')
]


def redact_string(text: str) -> str:
    """
    Masks credentials found in raw strings using regex patterns.
    """
    if not MASK_SECRETS or not text:
        return text

    redacted_text = text
    
    # Redact Bearer and Auth
    redacted_text = re.sub(r'(?i)(bearer\s+)[a-zA-Z0-9_\-\.]+', r'\1' + REDACTION_MASK, redacted_text)
    redacted_text = re.sub(r'(?i)(authorization:\s*(?:bearer\s+)?)[a-zA-Z0-9_\-\.]+', r'\1' + REDACTION_MASK, redacted_text)
    
    # Redact key=value
    key_pattern = r'(?i)\b(?:' + '|'.join(SENSITIVE_KEYS) + r')\s*=\s*([^\s\'"&]+)'
    redacted_text = re.sub(key_pattern, lambda m: m.group(0).replace(m.group(1), REDACTION_MASK), redacted_text)
    
    # Redact JSON/Dict style keys
    json_pattern = r'(?i)([\'"](?:' + '|'.join(SENSITIVE_KEYS) + r')[\'"]\s*:\s*[\'"])([^\'"]+)([\'"])'
    redacted_text = re.sub(json_pattern, r'\1' + REDACTION_MASK + r'\3', redacted_text)

    # Redact DB URLs
    url_pattern = r'(?i)([a-z+]+://[^:]+:)([^@]+)(@)'
    redacted_text = re.sub(url_pattern, r'\1' + REDACTION_MASK + r'\3', redacted_text)

    return redacted_text


def redact_dict(data: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Recursively redacts dictionary values if their key matches SENSITIVE_KEYS.
    """
    if not MASK_SECRETS or not isinstance(data, dict):
        return data

    redacted = {}
    for key, value in data.items():
        key_str = str(key).lower()
        if key_str in SENSITIVE_KEYS:
            redacted[key] = REDACTION_MASK
        else:
            redacted[key] = redact_any(value)
    return redacted


def redact_list(data: List[Any]) -> List[Any]:
    """
    Recursively maps over a list to redact its items.
    """
    if not MASK_SECRETS or not isinstance(data, list):
        return data
    return [redact_any(item) for item in data]


def redact_tuple(data: Tuple[Any, ...]) -> Tuple[Any, ...]:
    """
    Recursively maps over a tuple to redact its items.
    """
    if not MASK_SECRETS or not isinstance(data, tuple):
        return data
    return tuple(redact_any(item) for item in data)


def redact_any(data: Any) -> Any:
    """
    Entrypoint to dynamically redact any type.
    """
    if not MASK_SECRETS:
        return data

    if isinstance(data, dict):
        return redact_dict(data)
    elif isinstance(data, list):
        return redact_list(data)
    elif isinstance(data, tuple):
        return redact_tuple(data)
    elif isinstance(data, str):
        return redact_string(data)
    return data
