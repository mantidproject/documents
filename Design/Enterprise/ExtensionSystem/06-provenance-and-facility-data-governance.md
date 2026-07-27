# Provenance and facility data governance

## Passive provenance capture

Provenance is a side effect of the one path every algorithm call already goes
through — the dispatcher — not a parallel system requiring compliance.
Instrumenting the dispatcher to record lineage (inputs, parameters, versions,
environment hash, timestamp) captures provenance for every reduction, whether
it's a formal workflow or a three-line ad hoc script, without the scientist
doing anything differently. This also matters for AI-generated code, for the
same reason described in [Goals and principles](01-goals-and-principles.md):
the tracked path being the easiest path is what both humans and LLMs reach
for by default.

Provenance travels with the data (an append-only lineage record attached to
each workspace, surviving being copied off-site) and is mirrored into
`NXprocess` on disk — NeXus already has a group built for this purpose.
Internally, structure the record around the W3C PROV vocabulary (entity /
activity / agent) rather than a bespoke schema, for interoperability with
external audit tooling.

This gives auditability, not correctness: it guarantees you can always answer
"what exactly ran, with what inputs" — not that the science was right.

## Instrument-specific data as independent packages

Instrument data must not be bundled with core or tied to Mantid's release 
cycle — an instrument's data changes on its own timeline, unrelated to 
when Mantid ships. Each is just another independently versioned package, 
following the same lifecycle as any compute or GUI extension. The 
tracking layer stays generic (identity, hash, validity window,
instrument, asset type); the payload stays instrument-specific and opaque 
to the registry. This is why no single generalized schema is needed across
instruments — only the tracking layer needs to be uniform.

## Facility config package

A small, versioned package (pixi-solved like everything else, discovered via
its own entry point, one per deployment), providing the mechanism a site uses
to manage its data, with sensible defaults so a standard facility needs zero
configuration:

- **Run resolver** — maps a run/experiment identifier to its data location.
  Facility-specific conventions (SNS, ISIS, ILL all differ) live here. Raw
  run data is typically already immutable once collected, so this is mostly
  about addressing, not verification.
- **Calibration / normalization validity registry** — an explicit, queryable
  index (not left to individual instrument scientists) recording, per asset:
  content hash, valid-from/valid-to or run-number range, instrument, who
  registered it and when. Registering a new calibration is itself a tracked
  dispatcher operation, not a side-channel file copy — the record and the
  file are always created together, the same way, on every instrument.
- **Content-addressed store** — stores and verifies bytes by hash. Hashing
  happens once, at registration time, not on every read.

## Resolve → fetch → verify, with a hard branch on mismatch

At reduction time: the validity registry is queried for the run in question,
returning the intended calibration and its recorded hash; the content store
fetches the actual bytes and computes their hash; if the hashes match, the
reduction proceeds and the pairing is recorded in provenance; if they don't,
that's surfaced as a flagged anomaly rather than passing silently. A hash
alone can only tell you "is this identical to before" — the validity
registry's record of intent is what tells you "was this the one that should
have been used."

Registration always creates a new address rather than overwriting one, so
"overwriting" through the system's own path is structurally not possible. The
residual risk — someone bypassing the system and editing a file in place —
can't be fully prevented by software alone; where facility IT allows it, back
the store with real immutable-storage semantics (read-only permissions
post-registration, object versioning). Short of that, hash verification at
resolve time turns the remaining case into a flagged outlier instead of a
silent failure.
