# 02. Quick Start

Getting started with TraceNest is incredibly simple. It requires no complex dependencies and works out-of-the-box in just 2 minutes.

## 1. Installation

Open your terminal and install TraceNest using `pip`:

```bash
pip install tracenest
```

## 2. Basic Setup (The Easiest Way)

You can drop TraceNest into any Python script and start logging beautifully formatted JSON logs instantly.

Create a file named `main.py`:

```python
from tracenest.logger import get_logger

# 1. Initialize the logger
# It will automatically create a "logs" folder and an "app.log" file
logger = get_logger("my_app")

# 2. Start logging!
logger.info("Application started successfully!")
logger.debug("Connecting to database...")

try:
    1 / 0
except Exception as e:
    logger.error("Something went horribly wrong", error=e)
```

Run your script:
```bash
python main.py
```

That's it! If you check your project folder, you will see a new `logs/` directory containing `app.log`. If you open that file, you'll see your logs perfectly formatted as JSON objects.

## 3. Viewing the Dashboard (Optional but Recommended)

Reading JSON files manually is boring. TraceNest includes a gorgeous web UI to read your logs!

You can easily run the built-in UI using FastAPI. If you don't have FastAPI installed, install it first:

```bash
pip install fastapi uvicorn
```

Then, update your `main.py`:

```python
from fastapi import FastAPI
from tracenest.logger import get_logger
from tracenest.ui.dashboard import mount_tracenest_ui

app = FastAPI()
logger = get_logger("my_fastapi_app")

# Mount the beautiful UI dashboard at the /logs URL
mount_tracenest_ui(app, path="/logs")

@app.get("/")
def home():
    logger.info("Someone visited the home page!")
    return {"message": "Welcome to my app!"}
```

Run the server:
```bash
uvicorn main:app --reload
```

Now, open your browser and go to:
**http://127.0.0.1:8000/logs**

You will see the TraceNest Dashboard displaying your logs in real-time!

---
**Next Step:** Want to know exactly how it does this magic? Read [03. Core Concepts Explained](03_core_concepts_explained.md).
