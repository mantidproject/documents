# Packaging, deployment, and governance

## Why conda/pixi

Conda-format packages carry real binary ABI metadata for compiled libraries,
which pip/PyPI doesn't do well. Given a C++ core plus a Python-heavy extension
ecosystem, the solver needs to reason about native library compatibility and
Python package compatibility in the same graph — conda/pixi's home turf.

## The versioning axis that actually matters

Extensions shouldn't pin against core's feature version — they pin against a
small virtual package, `mantid-extension-abi`, representing interface/ABI
compatibility specifically. Core's feature version and its extension-ABI
version aren't the same axis: core can ship new algorithms without touching
the `IExtension` contract, or bump the ABI without much else changing. Core
propagates the constraint automatically via conda `run_exports` when built,
so extension authors don't hand-pin ranges.

## Extension-to-extension dependencies

Extensions declare normal conda run-dependencies on other extension package
names and version ranges; pixi resolves the whole graph at once, including
diamond dependencies through core and the abi package.

## Deployment scoping is not Mantid's governance concern

The deployable unit is a pixi manifest plus its resolved lockfile. How a site
scopes that — per instrument, per beamline, per experiment type, or something
else entirely — is an operational decision made by whoever runs the server,
not something Mantid should prescribe or bake into its own architecture.
Mantid's governance stops at providing the mechanism: the mounting system,
the packaging conventions, and the abi versioning policy. "Facility-wide"
consistency, where it exists, is an emergent property of shared package
dependencies, not a special case to design for.

## Two phases: solve, then discover

Pixi resolving and installing an environment is a deploy-time concern.
Runtime discovery — the registry finding what's installed — happens once, at
process startup, via a different mechanism (native `dlopen` scanning for
headless C++, Python entry points where Python is present). See
[Extension interoperability](02-extension-interoperability.md) for the
registration mechanics and the mermaid flow for the full pipeline.

## Policies, not tooling, handle the rest

- **Unsatisfiable environments will happen** once enough independently
  versioned extensions exist. No solver invents compatibility that doesn't
  exist — the fix is a stated abi support window (e.g. "N and N-1 supported
  for 12 months"), not a smarter resolver.
- **Extension code never enters core's or Workbench's repository.** Both
  hosts discover extensions at runtime and never merge them in. This is the
  load-bearing boundary that keeps "everything mounts uniformly" from turning
  into "core absorbs everyone's maintenance burden."
- **Promotion to core or Workbench is a deliberate decision**, never a
  default outcome of a long-lived PR. An extension earns that status only
  when the team explicitly takes on the maintenance burden.
- **Non-conforming code simply doesn't mount.** There's no "stuck" case for
  core — if an extension author skips the SDK conventions, they don't get a
  registry entry or a generated Python binding. That's a natural consequence,
  not a support gap to close.
