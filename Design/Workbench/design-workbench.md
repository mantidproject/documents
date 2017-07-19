Summary
=======

This document describes the architecture of the new workbench. It includes the intended design for the `mantdidui` package.

Widgets
=======

The intention is that the workbench be comprised, as much as possible and is sensible, of reusable widgets. These widgets will live in a new `mantidui.widgets` subpackage (see [layout](design-layout.md) for it's layout within the rest of the framework.

Plotting
========

`matplotlib` will provide the plotting abilities within the new workbench. It is extremely powerful but some of its defaults are not necessarily what we would want but its OO api makes
it simple to provide our own replacements for items such as toolbars etc.
