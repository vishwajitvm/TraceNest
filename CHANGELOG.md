# Changelog

## v0.1.14 - 2026-07-16

### Fixed
* Fixed a Mermaid syntax error in the documentation (`01_introduction.md`) that caused the high-level architecture diagram to fail to render on GitHub.

## v0.1.13 - 2026-07-16

### Added
* Completely rebuilt the `docs/` folder with an exhaustive, beginner-friendly 14-chapter Master Guide! Everything from core concepts (Configuration, Formatter, Retention, Rotation) to Advanced Customizations and Troubleshooting is now thoroughly explained with examples and diagrams.

## v0.1.12 - 2026-07-15

### Fixed
* Fixed z-index issue causing the dropdown menus (Levels and Themes) to incorrectly render underneath the sticky table headers. 

## v0.1.11 - 2026-07-15

### Added
* 4 Beautiful New Themes: Emerald (Green), Ruby (Red), Amethyst (Purple), and Midnight (OLED High Contrast).
* Redesigned footer showcasing the current TraceNest version and developer credit.

### Fixed
* Fixed search input box retaining a white background when using dark themes.

## v0.1.10 - 2026-07-15

### Fixed
* Fixed white background issue on table rows and dropdown menus when using Dark or Dark Blue themes. All components now properly inherit theme colors.

## v0.1.9 - 2026-07-15

### Fixed
* Fatal UI crash preventing logs from displaying on fresh installs due to a DOM mismatch.
* Replaced inline level badges with a clean dropdown menu for improved UX.
* Removed the "Versions" modal entirely for a simpler, decluttered interface.

## v0.1.8 - 2026-07-15

### Added
* Auto-refresh functionality to stream logs live in the dashboard without manually reloading.
* Manual refresh button.
* Slide-out Details Panel providing deep-dive capabilities into structured logs and traceback without losing table context.
* PyPI version checking directly in the UI versions modal.

### UI
* Completely redesigned UI dashboard inspired by modern observability platforms (e.g., Grafana/Vercel).
* High contrast, beautiful themes (Dark, Light, Dark Blue) relying on modern `CSS variables`.
* Refined typography utilizing Inter and JetBrains Mono fonts.
* Advanced layout featuring fixed-width columns and custom level badges.

### Fixed
* Current log selection bug: Re-rendering the dashboard on polling no longer destroys user selection.
* DOM flickering issues eliminated.

### Performance
* Achieved O(1) table updates per polling interval by intelligently caching parsed logs and dynamically computing diffs on the frontend.

### Breaking Changes
* None

## v0.1.7 - 2026-07-03

### Added
* Markdown-based changelog system directly integrated into the UI.
* Dynamic Versions modal featuring a beautiful two-pane layout, fetching and rendering markdown using `marked.js`.
* Synced main project `README.md` with the full project changelog to ensure release notes are visible directly on PyPI.

### Changed
* Improved UI links, adding proper developer attribution linking back to GitHub in the UI footer.
* Removed the static `changelog.json` in favor of the dynamic API.


## v0.1.6 - 2026-07-03

### Added
* Added built-in secret redaction to prevent credentials, tokens, API keys, cookies, and database passwords from leaking in logs.
* Added recursive masking for dictionaries, lists, nested metadata, request data, and response data.
* Added pattern-based masking for raw log strings, Authorization headers, JWTs, database URLs, Redis URLs, and key-value secrets.
* Added configuration options for custom sensitive keys and redaction mask.

### Changed
* Logs are now redacted before storage and before UI/API display for defense-in-depth safety.
* Middleware logging now masks sensitive headers, cookies, request bodies, and response bodies.

### Tests
* Added tests for key-based redaction, regex redaction, nested data structures, middleware safety, and custom redaction configuration.
