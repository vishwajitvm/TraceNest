# FastAPI Integration

TraceNest provides native and seamless integration with **FastAPI**, enabling automatic request and response logging with minimal setup.

This integration is optional but strongly recommended for API-based applications.

---

## Why FastAPI Integration

When integrated with FastAPI, TraceNest automatically logs:

- Incoming HTTP requests
- Response status codes
- Request execution time
- Unhandled exceptions
- Application-level errors

This eliminates the need for manual request logging.

---

## Installation Requirement

Ensure TraceNest is installed:

```bash
pip install tracenest
```

---

## Basic Integration

Add the TraceNest middleware to your FastAPI application.

```python
from fastapi import FastAPI
from tracenest.fastapi import TraceNestMiddleware

app = FastAPI()

app.add_middleware(TraceNestMiddleware)
```

No additional configuration is required.

---

## What Gets Logged Automatically

For every HTTP request, TraceNest records:

- HTTP method
- Request path
- Response status code
- Execution duration (milliseconds)
- Timestamp
- Error details (if any)

---

## Example Log Output

```text
[2026-01-12 10:22:41] [INFO]
GET /api/users
status=200 duration=34ms
```

---

## Exception Handling

Unhandled exceptions are automatically captured and logged.

```text
[2026-01-12 10:23:10] [ERROR]
Unhandled exception occurred
path=/api/payments
method=POST
```

Stack traces are included when available.

---

## Custom Route Logging

You can continue to use TraceNest logger inside routes.

```python
from tracenest import logger

@app.post("/orders")
async def create_order():
    logger.info("Creating order")
    return {"status": "ok"}
```

This works alongside automatic request logging.

---

## Performance Considerations

- Middleware execution is lightweight
- Logging is non-blocking
- No request latency impact
- Safe for high-throughput APIs

---

## Disabling FastAPI Integration

If middleware is not added, TraceNest will continue to function as a standard logging SDK without request-level logging.

---

## Compatibility

- FastAPI
- Starlette (indirectly)
- ASGI-based servers

Tested with:
- Uvicorn
- Hypercorn
- Gunicorn (ASGI workers)

---

## Best Practices

- Enable middleware in development and production
- Avoid logging sensitive request bodies
- Use structured logging for business events
- Combine with day-wise log mode for APIs

---

## Safety Guarantees

- Middleware failures never crash the application
- Exceptions are logged safely
- Application behavior remains unchanged

TraceNest FastAPI integration is designed to be transparent, safe, and production-ready.
