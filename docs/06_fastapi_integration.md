# 06. FastAPI Integration

If you are building a web API using **FastAPI**, TraceNest is the absolute perfect companion. 

Because TraceNest uses an *Asynchronous Handler* (which means it uses a background worker to save files), it will **never** block or slow down your FastAPI requests.

## How to Mount the Dashboard in FastAPI

To see your logs in the beautiful Web Dashboard, you need to "mount" (attach) the TraceNest UI to your FastAPI app.

Here is the complete code to do that:

```python
from fastapi import FastAPI
from tracenest.logger import get_logger
from tracenest.ui.dashboard import mount_tracenest_ui

# 1. Create your FastAPI app
app = FastAPI()

# 2. Get the TraceNest logger
logger = get_logger("my_fastapi_app")

# 3. Mount the Dashboard UI!
# This tells FastAPI: "If someone goes to /tracenest in their browser, show them the dashboard!"
mount_tracenest_ui(app, path="/tracenest")

# 4. Write a normal FastAPI route
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Log the request!
    logger.info("Fetching user from database", user_id=user_id)
    
    if user_id > 100:
        logger.warning("User ID seems very high!", user_id=user_id)
        
    return {"user_id": user_id, "name": "TraceNest Fan"}
```

## How to Test It
1. Run the code above using `uvicorn main:app --reload`
2. Open your browser and go to `http://127.0.0.1:8000/users/50` to trigger a log.
3. Open a new tab and go to `http://127.0.0.1:8000/tracenest`.

You will immediately see the TraceNest Dashboard showing the log you just triggered!

## Under the Hood (Technical Context)
When you invoke `mount_tracenest_ui(app, path="/tracenest")`, you are executing a dependency injection pattern that mutates the FastAPI application instance:
1. **API Endpoints:** TraceNest creates a new `fastapi.APIRouter()`. It registers a `GET` endpoint at `/api/logs` returning a `fastapi.responses.JSONResponse`.
2. **Template Serving:** It registers a `GET` endpoint at the root `/` of the router that returns a `fastapi.templating.Jinja2Templates.TemplateResponse` which renders `index.html`.
3. **Static Assets:** It mounts a `fastapi.staticfiles.StaticFiles` instance to serve `styles.css` and `app.js`.
4. **App Mounting:** Finally, it calls `app.mount(path, router)` which safely isolates all TraceNest endpoints within their own ASGI sub-application context, preventing any URL collisions with your main API routes.

---
**Next Step:** Let's learn all the cool things the dashboard can do in [07. UI Dashboard Guide](07_ui_dashboard_guide.md).
