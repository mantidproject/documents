# Hosts and registries

## Two hosts, two registries

Core and MantidWorkbench are separate hosts, each owning its own registry,
scoped to its own domain:

- **Core registry** — compute extensions (algorithms, workspace types).
  Language-neutral discovery; cross-language calls use the trampoline pattern
  from [Extension interoperability](02-extension-interoperability.md). Works
  with zero awareness of whether a GUI is even installed — a headless
  facility server running batch reduction never needs Workbench at all.
- **GUI registry** — owned by Workbench, not core. GUI extensions are
  Python-only (no sensible use case for a C++ GUI extension), so this
  registry needs none of the cross-language machinery the core registry does.
  It's a plain Python plugin system.

Core has no concept of menus or dock widgets, and shouldn't. Workbench has no
business managing algorithm dispatch. What's shared between them is the
mounting *mechanism* (entry-point discovery, packaging, the never-merges
policy) — instantiated twice, once per host, each with its own interface
family.

## GUI interface family

- `IMenuContribution` — adds a menu action
- `IDockFactory` — adds a dockable panel
- `IViewProvider` — supplies a custom view for a given workspace type

`IViewProvider` is the one point of coupling back to core: it needs to know
which workspace type it's providing a view for, so it reads core's registry as
a read-only data source. That stays one-directional, at the data level, not
the binding level.

## Discovery

One entry-point group per contribution type
(`mantidworkbench.menus`, `mantidworkbench.docks`, `mantidworkbench.views`),
mirroring Python's own split of `console_scripts` from `gui_scripts`.
Workbench enumerates the group it cares about at startup — no runtime
type-inspection needed.

## Packaging: GUI is an optional extra

A single extension package can register into both the core registry and the
GUI registry, if it ships both a compute algorithm and a UI for it — but the
GUI half should be an optional extra (or a separate companion package), so a
headless install never pulls in Qt/PyQt. This matters directly for unattended
batch pipelines on instrument servers.

## The Qt binding boundary

Qt already has its own C++/Python binding system (SIP for PyQt, Shiboken for
PySide) — it's how any Python `QWidget` subclass exists at all. Given GUI
extensions are Python-only and Workbench is a Python/Qt application, the
common case needs no new binding machinery: it's Python calling Python. A
C++-only GUI extension trying to hand a raw `QWidget*` into a Python-hosted
shell would require bridging two independent binding systems via pointer
hand-off utilities (`shiboken6.wrapInstance` or SIP's equivalent) — solvable,
but fiddly enough that it isn't worth first-class support until someone
actually needs it.
