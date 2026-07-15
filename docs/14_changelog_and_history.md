# 14. Changelog & History

TraceNest is constantly evolving! To see the exact, version-by-version history of what features were added and what bugs were fixed, you can read the main **CHANGELOG.md** file located at the root of the project.

## How we Version

TraceNest follows **Semantic Versioning** (SemVer). 
A version number looks like this: `MAJOR.MINOR.PATCH` (e.g., `v0.1.13`).

* **MAJOR:** We increase this number if we completely change how TraceNest works, and you have to rewrite your code to use the new version. (We are currently on version 0, which means we are still in early development!).
* **MINOR:** We increase this number when we add cool new features (like new themes or a new search bar) that don't break your existing code.
* **PATCH:** We increase this number when we fix small bugs (like a button being the wrong color).

## Recent Major Milestones

* **v0.1.0:** The initial release! We built the core asynchronous logger and the basic JSON formatter.
* **v0.1.8:** We added the beautiful Web Dashboard UI!
* **v0.1.11:** We added multiple colorful themes (Emerald, Ruby, Midnight) to the UI.
* **v0.1.13:** We completely rewrote the documentation to make it easy for beginners to understand. 

## Under the Hood (Technical Context)
As developers, we know that breaking API contracts is a cardinal sin. We strictly enforce Semantic Versioning rules.
* **Backward Compatibility:** Any changes to the `get_logger` signature or the `TraceNestConfig` structure will only happen on a MAJOR version bump (e.g. `v1.0.0`). 
* **Deprecation Warnings:** If we ever intend to remove a feature, we will first emit a standard Python `DeprecationWarning` for at least two MINOR version lifecycles before removal.

**Thank you for using TraceNest!**
