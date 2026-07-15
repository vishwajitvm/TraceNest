# 07. UI Dashboard Guide

The TraceNest Web Dashboard is where the magic really happens. Instead of squinting at massive text files, you can use the dashboard to filter, search, and analyze your logs comfortably.

## Features

### 1. Live Auto-Refresh
At the top left of the screen, you will see a toggle switch labeled **Live**. 
When this is turned on, the dashboard will automatically fetch new logs every few seconds. If a new error occurs on your server, it will pop up on your screen instantly without you having to refresh the page!

### 2. The Level Filter
At the top right, there is a dropdown menu labeled **Level**. 
If you only want to see Errors, simply click this dropdown and select **Error**. All the annoying `INFO` and `DEBUG` messages will instantly vanish, letting you focus on fixing the bug.

### 3. The Search Bar
Next to the Level filter is a **Search Box**.
You can type *anything* in here. Looking for a specific user ID? Type it in. Looking for a specific error code? Type it in. It searches instantly.

### 4. The Details Panel
The table shows you the Time, Level, and Message. But what if you want more details?
Simply **click on any row in the table**. A beautiful sidebar will slide out from the right side of the screen containing the complete JSON data for that log!

This panel will show you:
* Exactly which file the log came from (e.g., `main.py`).
* Exactly which line number the log was on (e.g., `line 42`).
* Any custom variables you passed into the logger.

### 5. Beautiful Themes
We know developers love dark mode. In the top right corner, there is a **Palette Icon**. Click it to choose between 6 gorgeous themes:
* **Light**
* **Dark** (Standard gray dark mode)
* **Dark Blue** (Like Grafana or Vercel)
* **Emerald** (A Matrix-style green)
* **Ruby** (A deep dark red)
* **Amethyst** (A rich dark purple)
* **Midnight** (High contrast OLED black)

## Under the Hood (Technical Context)
The UI is a Single Page Application (SPA) driven by Vanilla Javascript (`app.js`).
* **Live Refresh Mechanism:** It uses standard `setInterval(fetchLogs, 5000)` combined with the standard `fetch()` browser API. By default, it requests the `/api/logs` endpoint.
* **DOM Rendering:** The JSON payload returned from the server is parsed (`await response.json()`) and then iterated over to dynamically reconstruct the `innerHTML` of the HTML table (`<tbody>`).
* **State Management:** Filters and search terms are maintained as global mutable variables in the JS runtime context, which are evaluated linearly on every render cycle.
* **Theming Implementation:** The color themes are not hardcoded hex values in the components. Instead, the `<body>` tag receives a class (e.g. `class="theme-ruby"`). In `styles.css`, this class overrides a set of CSS Custom Properties (`--bg-main`, `--text-main`). Because Bootstrap 5 is configured to inherit these variables, the entire DOM tree repaints synchronously without requiring a network request.

---
**Next Step:** Let's talk about how TraceNest keeps your data safe in [08. Security & Performance](08_security_and_performance.md).
