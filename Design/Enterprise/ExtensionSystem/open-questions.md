# Open questions

Genuine gaps in what's been decided so far — not fully solved here, flagged
so they don't get lost.

## Crash and exception isolation for native extensions

If a third-party C++ extension throws an unhandled exception, or worse,
segfaults, inside `execute()`, what happens to the rest of the process? A
Python exception is recoverable; a native crash in an in-process extension
can take down core (and everything else mounted in it) with no warning. At
minimum this needs an exception-safety convention (the dispatcher wraps every
call in try/catch, extensions must not let exceptions cross the boundary
uncaught) — but that doesn't help against a genuine segfault or memory
corruption. Worth deciding: is in-process execution acceptable for all
extensions, or do less-trusted / higher-risk extensions need some form of
process isolation, at the cost of the coarse-grained-call overhead that would
introduce?

## Security and trust boundary for what runs on facility servers

This deploys to production instrument servers. Nothing so far restricts which
channels or packages a facility is willing to install — conda-forge and
private channels are both just "a channel" in the design as written. Worth
deciding: channel allowlisting per facility, package signing verification
(conda supports content-trust signing), and whether the facility config
package is also the natural place to declare a site's trust policy.

## Communicating breaking changes to an ecosystem core can't fully see

The abi versioning policy (N and N-1 supported for some window) assumes core
can announce a deprecation to affected maintainers. But the whole design
explicitly avoids requiring central visibility into who's building extensions
— there's no merge, no required registration with Mantid the project. Worth
deciding: does the package metadata require a maintainer contact field, is
there a lightweight index/catalog (mentioned in passing during the
architecture discussion but never designed) that doubles as a
deprecation-notice channel, or is "the abi bump itself, plus the solver
failing loudly" the whole mechanism?

## Testing conventions for extension authors

Not discussed at all: does the SDK provide a test harness or fixtures for
extension authors, what's the expectation for testing against multiple
supported abi versions, and does the facility validity registry have a
sandboxed/dry-run mode for testing a new calibration before it's live.

## Workspace schema evolution

If a workspace type's Arrow schema changes over time (columns added, meaning
of a field changes), how do older provenance records and previously stored
data remain interpretable? Not urgent, but worth a policy before it happens
by accident.
