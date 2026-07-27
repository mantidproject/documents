# Mantid extension architecture — doctree

Everything mounts uniformly — core included — but the contract that's uniform
is a discovery/interface descriptor, not a shared implementation language.
Core stays native C++ with no hard Python dependency; Python is the common
ecosystem language by convention, not by force. Extension code never enters
core's or Workbench's repository — both hosts discover extensions at runtime
and never merge them.

## Contents

1. [Goals and principles](01-goals-and-principles.md) — why uniform mounting,
   why the mechanism/contract split, why this also matters for AI-assisted
   code generation.
2. [Extension interoperability](02-extension-interoperability.md) — the
   `IExtension` interface, the pybind11 trampoline, automatic binding
   generation, arbitrary method and workspace-type binding, Arrow-based data
   interop.
3. [Hosts and registries](03-hosts-and-registries.md) — Core and
   MantidWorkbench as separate hosts, each owning its own registry; the
   compute/GUI split; headless deployment.
4. [Packaging, deployment, and governance](04-packaging-deployment-and-governance.md)
   — pixi/conda, the `mantid-extension-abi` virtual package, deployment
   scoping (a site decision, not Mantid's), and the policies that keep core
   from absorbing maintenance burden.
5. [Repo template and release workflow](05-repo-template-and-release-workflow.md)
   — the GitHub template, the one-branch/environment-gate model, and the
   conda-forge publish path.
6. [Provenance and facility data governance](06-provenance-and-facility-data-governance.md)
   — passive provenance capture, the facility config package, the
   calibration/normalization validity registry, and instrument data as
   independent packages.
7. [Extension catalog and discovery](07-extension-catalog-and-discovery.md)
   — pre-install discovery via search and a hosted catalog, the
   channel/allowlist trust separation, and the staleness check that keeps
   listings current.
8. [Open questions](open-questions.md) — real gaps not yet decided.

See also: [`extension-flow.mermaid`](extension-flow.mermaid) — the full
diagram of an extension's journey from repo to running and registered.