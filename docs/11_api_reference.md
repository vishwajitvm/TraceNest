# 11. API Reference

This is a dictionary of the main functions and classes you will interact with in TraceNest.

## `get_logger(name: str, config: TraceNestConfig = None)`
This is the main function you use to get a logger. 
* **`name`**: A string representing the name of your logger (e.g., "database_module").
* **`config`** (Optional): A custom `TraceNestConfig` object. If you don't provide one, it uses the default settings.
* **Returns**: A configured standard Python `logging.Logger` object that has been enhanced by TraceNest.

## `TraceNestConfig`
This class is used to configure how TraceNest behaves.
* **`log_dir`** (str): The directory to save logs (Default: `"logs"`).
* **`log_file_name`** (str): The name of the log file (Default: `"app.log"`).
* **`max_bytes`** (int): The maximum size of a log file before it rotates (Default: `10485760` bytes, which is 10MB).
* **`backup_count`** (int): The number of old rotated files to keep (Default: `7`).
* **`mask_secrets`** (bool): Whether to hide passwords and API keys (Default: `True`).

## `mount_tracenest_ui(app: FastAPI, path: str = "/tracenest")`
This function attaches the Web Dashboard to your FastAPI application.
* **`app`**: Your FastAPI application object.
* **`path`**: The URL path where you want the dashboard to live (Default: `"/tracenest"`).

---
**Next Step:** Is something broken? Let's fix it in [12. Troubleshooting & FAQ](12_troubleshooting_and_faq.md).
