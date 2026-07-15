# 04. Project Architecture

To truly understand TraceNest, it helps to know how the project is organized. Let's take a tour of the source code! 

Here is the basic structure of the `tracenest` folder:

```text
tracenest/
├── core/
├── formatters/
├── handlers/
├── ui/
├── __init__.py
└── logger.py
```

Let's break down exactly what each folder and file does.

## 1. `tracenest/logger.py`
This is the **Main Entry Point**. When you import `get_logger()` into your project, it comes from this file. This file acts as the conductor of the orchestra. It reads your configuration, sets up the formatters and handlers, and hands you a ready-to-use logger.

## 2. `tracenest/core/` (The Brain)
This folder contains the core logic and settings.
* **`config.py`:** This is where the `TraceNestConfig` class lives. It defines all the default settings (like log paths, UI settings, retention days, etc.).
* **`constants.py`:** A simple file that stores words or numbers that are used over and over again in the project, so we don't have to re-type them.
* **`security.py`:** This is a very important file! It contains the logic to scan your log messages and hide passwords, API keys, and credit card numbers before they are saved.

## 3. `tracenest/formatters/` (The Designers)
* **`json_formatter.py`:** This file contains the code that takes your standard Python log message and transforms it into the structured JSON format that the Dashboard UI needs to read.

## 4. `tracenest/handlers/` (The Delivery Workers)
* **`async_file.py`:** This file is responsible for saving your logs to a file (like `app.log`). It is "async" (asynchronous), which means it uses a background worker thread. When you log a message, it hands the message to the background worker and instantly goes back to your app, so your app is never slowed down by saving files.

## 5. `tracenest/ui/` (The Web Dashboard)
This folder contains everything needed to run the beautiful website you view your logs on.
* **`dashboard.py`:** The Python code that connects the UI to FastAPI.
* **`templates/`:** Contains the actual website files!
  * **`index.html`:** The HTML structure of the dashboard.
  * **`styles.css`:** The design, colors, and themes (like Dark Blue, Emerald, Ruby).
  * **`app.js`:** The Javascript that automatically refreshes the logs and makes the dropdown filters work.

## 6. Outside of `tracenest/`
* **`pyproject.toml`:** This file isn't code. It's a configuration file that tells Python package managers (like `pip`) how to build TraceNest so it can be uploaded to PyPI (the website where you download Python packages).
* **`docs/`:** The folder you are reading right now!

## Under the Hood (Technical Context)
From a strictly technical perspective, here is the class hierarchy and standard library usage:
* **Core:** The `TraceNestConfig` object in `config.py` is implemented using Python's built-in `@dataclass` decorator for strict typing and minimal boilerplate.
* **Security:** `SecretRedactor` in `security.py` uses `re.compile()` to pre-compile regular expressions for passwords and tokens. Pre-compiling the regex ensures that the redaction check happens in microseconds and doesn't bottleneck the logging queue.
* **Formatters & Handlers:** `json_formatter.py` inherits directly from `logging.Formatter`. `async_file.py` implements a custom class wrapping `logging.handlers.RotatingFileHandler` inside a `threading.Thread` and a `queue.Queue`.
* **UI:** The frontend is entirely vanilla. `app.js` has zero dependencies on React, Vue, or Angular. It heavily utilizes the modern Browser `Fetch API`, `Promises`, and DOM manipulation (`document.getElementById`, `innerHTML`). The UI uses Bootstrap 5 CSS variables (`--bs-bg-opacity`, etc.) and heavily overrides them with CSS Custom Properties (`--bg-panel`, `--text-main`) to support dynamic theming (Dark, Emerald, Ruby) without requiring page reloads.

---
**Next Step:** Let's learn how to tweak and customize the project in [05. Configuration Guide](05_configuration_guide.md).
