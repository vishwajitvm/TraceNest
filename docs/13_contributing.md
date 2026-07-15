# 13. Contributing

TraceNest is an open-source project, which means anyone in the world (including you!) can help make it better. 

Whether you want to fix a bug, add a new colorful theme to the dashboard, or improve this documentation, we would love your help.

## How to Set Up the Project for Development

If you want to edit the TraceNest code, you shouldn't install it using `pip install tracenest`. Instead, you should download the source code to your computer.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vishwajitvm/TraceNest.git
   cd TraceNest
   ```

2. **Install in "Editable" Mode:**
   This tells Python to use the code inside the folder you just downloaded. Any changes you make to the files will instantly apply!
   ```bash
   pip install -e .
   ```

3. **Run the Test Project:**
   We have a separate project folder called `tracenest-fastapi-test`. This is a dummy FastAPI application designed specifically so you can test your changes to TraceNest.
   ```bash
   cd ../tracenest-fastapi-test
   python -m uvicorn main:app --reload
   ```

## What can I work on?
* **Themes:** Are you good at CSS? Add a new theme to `tracenest/ui/templates/styles.css`!
* **Formatters:** Want to support logging to XML or CSV? Create a new formatter!
* **Bug Fixes:** Check the GitHub Issues page to see if anyone has reported a bug you can fix.

## Under the Hood (Technical Context)
When contributing, please adhere to these technical standards:
1. **Python Version:** The codebase uses advanced typing features (`Final`, `@dataclass`) and is strictly compatible with Python 3.8 and higher. Do not use syntax exclusive to Python 3.10+ (like `match` statements) to maintain backward compatibility.
2. **Formatting:** We strictly use standard PEP8 formatting. 
3. **No Database Dependencies:** Do not introduce ORMs (SQLAlchemy) or database drivers. The library must remain zero-dependency (other than FastAPI for the UI extension).

---
**Next Step:** See how far we've come in [14. Changelog & History](14_changelog_and_history.md).
