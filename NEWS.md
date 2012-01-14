---

# Changes in version 0.3 (2012-01-13)

---

## Major Changes

  - IPython 0.12 or newer is now required. Dropped Matplotlib dependency.

## Bug Fixes

  - Better integration with the QGIS event loop.

  - Improperly closing external consoles will no longer hose the entire QGIS
    application.


---

# Changes in version 0.2 (2011-08-19)

---

## Major Changes

  - Targetted IPython 0.11 stable release.

  - IPython consoles now executed as external processes. This is because the
    consoles rely on Version 2 of the PyQt API and QGIS uses Version 1 of the
    API which is incompatible.


---

# Changes in version 0.1 (2011-02-06)

---

First public release. Targetted IPython 0.11-dev.

