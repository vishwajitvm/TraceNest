import json
import base64

def get_mermaid_url(code):
    state = {
        "code": code,
        "mermaid": {"theme": "default"}
    }
    json_str = json.dumps(state)
    b64_str = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')
    return f"https://mermaid.ink/svg/{b64_str}"

arch_code = """graph TD
    A[Your Application code] -->|logger.info| B(TraceNest In-Memory Queue)
    C[Incoming HTTP Request] -->|Intercepted by| D(TraceNest Middleware)
    D --> B
    B -->|Background Thread Flushes| E[TraceNestLogs / 2026-08-16.log]
    
    F[Developer Browser] -->|http://localhost:8000/tracenest| G(TraceNest UI Router)
    G -->|Reads| E"""

lifecycle_code = """sequenceDiagram
    participant App as Application
    participant Core as TraceNest Core
    participant Redact as Redaction Engine
    participant Queue as Memory Queue
    participant Disk as File System (TraceNestLogs)
    participant UI as Developer UI

    App->>Core: logger.error("DB Timeout", password="secret123")
    Core->>Redact: Scan and Mask
    Redact-->>Core: {"msg": "DB Timeout", "password": "***"}
    Core->>Queue: Push to Buffer (Non-blocking)
    App->>App: Continues Execution...
    
    loop Background Thread
        Queue->>Disk: Flush Buffer to File
        Disk->>Disk: Check File Size / Rotate if needed
    end

    UI->>Core: GET /tracenest/api/logs
    Core->>Disk: Read latest entries
    Disk-->>UI: Return JSON payload
    UI->>UI: Render in Dashboard"""

print("Architecture URL:")
print(get_mermaid_url(arch_code))
print("\nLifecycle URL:")
print(get_mermaid_url(lifecycle_code))
