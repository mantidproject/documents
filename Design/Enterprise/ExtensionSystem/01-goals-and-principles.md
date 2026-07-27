# Goals and principles

## Uniform mounting, not uniform language

Everything — core, compute extensions, GUI extensions, instrument data —
registers to the same kind of mounting mechanism. What's uniform is the
*discovery/interface contract* (a descriptor: name, version, capabilities,
entry point), not the implementation language. Core stays native C++ and
never needs a hard Python dependency; Python is the common ecosystem language
because it's convenient and low-friction, not because anything forces it.

## Separate the contract from the mechanism, and the mechanism from the payload

Three related splits recur throughout this design:

- **Discovery vs. invocation.** Registering into a registry (metadata: "I
  exist, here's my shape") is a different concern from actually being called.
  A C++ extension can be discoverable without ever touching Python; a call
  still needs a real binding.
- **Interface vs. implementation.** Everything implements the same small set
  of abstract interfaces (`IExtension` and friends). A caller holds a pointer
  to the interface and never needs to know whether the concrete thing behind
  it is C++ or Python.
- **Tracking layer vs. payload.** The provenance and validity-tracking
  mechanisms only need to know generic facts (identity, hash, validity
  window); the actual instrument-specific content stays opaque to them. This
  is why no single generalized schema is needed across instruments.

## Make the correct path the shortest path

The most reliable way to get compliant behavior — to prevent reinvention,
and from AI coding assistants that pattern-match onto whatever's easiest 
— is to make the tracked, correct, uniform way of doing something also 
the least-effort way to write working code. Where possible, provenance 
and governance are side effects of using the standard building blocks,
not additional steps someone has to remember.

This is also what makes the codebase legible to AI-assisted development: one
dispatch pattern, one workspace idiom, repeated everywhere, gives an LLM (and
a human skimming for the first time) one thing to imitate rather than several
competing ones. Concretely, this means:

- Strong typing and machine-readable descriptors at every interface boundary.
- A small number of excellent, canonical example scripts, rather than an
  exhaustive reference manual — most AI coding tools retrieve and imitate a
  handful of nearby examples more than they consult documentation.
- Exposing the registry's structured metadata (already needed for the mounting
  system itself) to AI tooling later, e.g. via an MCP server, so code
  generation can ground itself in real current signatures instead of
  hallucinated ones. Not built now — a natural extension of infrastructure
  already planned.

## What this buys, and what it doesn't

This architecture gives auditability, reproducibility, and a low-friction path
to compliance. It does not give correctness-checking — the system can always
answer "what exactly ran, with what inputs," but it cannot tell you the
science was right. That's a real and separate problem.
