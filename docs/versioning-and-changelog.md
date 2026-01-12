# Versioning and Changelog

TraceNest follows **Semantic Versioning (SemVer)** to ensure predictable upgrades and backward compatibility.

Version format:

```text
MAJOR.MINOR.PATCH
```

---

## Versioning Strategy

- **MAJOR** version increments indicate breaking changes
- **MINOR** version increments add new features in a backward-compatible way
- **PATCH** version increments include bug fixes and internal improvements

Backward compatibility is preserved within the same MAJOR version whenever possible.

---

## Current Version

### v0.1.0

Initial public release of TraceNest.

#### Features

- Core logging API
- Zero-configuration setup
- Automatic `TraceNestLogs/` folder creation
- Day-wise logging mode
- Single-file logging mode
- Log size enforcement
- Retention-based log cleanup
- Built-in local UI
- FastAPI middleware integration
- Structured logging with metadata
- Non-blocking and safe logging behavior

---

## Planned Versions

### v0.2.0

#### Planned Features

- Command-line interface (CLI)
- Log export (JSON / CSV)
- Improved UI filtering and search
- Config hot-reload support
- Improved error grouping

---

### v0.3.0

#### Planned Features

- Team-based log views
- Role-based access (local)
- Enhanced UI performance
- Log replay and timeline view

---

### v1.0.0

#### Stability Milestone

- Fully stabilized API
- Long-term support guarantees
- Backward compatibility commitment
- Production-hardened release

---

## Deprecation Policy

- Deprecated features will be documented clearly
- Deprecations will remain available for at least one MINOR release
- Removal only occurs in a MAJOR version bump

---

## Upgrade Guidelines

- Always review the changelog before upgrading
- Test upgrades in non-production environments first
- Avoid skipping MAJOR versions

---

## Changelog Maintenance

- Each release documents additions, changes, and fixes
- Changelog entries are chronological
- All breaking changes are clearly marked

TraceNest versioning is designed to be predictable, transparent, and developer-friendly.
