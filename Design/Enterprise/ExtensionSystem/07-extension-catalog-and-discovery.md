# Extension catalog and discovery

Everything so far covers *runtime* discovery — an environment that already
has an extension installed finding it. This covers *pre-install* discovery:
someone with a fresh core install finding out what extensions exist at all,
without relying on hearsay.

## No new metadata to author

The SDK build step already produces a registry descriptor (name, version,
category, parameter schema) for every extension, purely so the runtime
registry can work. That same descriptor is what a catalog needs to display.
Nothing here requires extension authors to write catalog entries by hand.

## Two layers, for two different moments

- **Immediate, in-terminal:** if extension packages carry a consistent tag
  (a keyword in the conda recipe, or a small metapackage dependency used
  purely as a marker), `pixi search` / `conda search` against the configured
  channels already answers "what's out there" with no additional
  infrastructure — existing tooling, not something to build.
- **Browsable catalog with aggregated docs:** a scheduled job (a nightly
  GitHub Action is enough) scans the channel for anything carrying that tag,
  pulls its descriptor and README, and regenerates a static site (GitHub
  Pages is sufficient hosting). Documentation is generated from what's
  actually shipped, at publish time, from the same structured source used
  for bindings — the same idea behind `docs.rs` — so it can't drift out of
  sync with real signatures the way hand-maintained wiki pages do.

## Channel publishing and catalog listing are different trust surfaces

The channel stays exactly as designed elsewhere in this doctree — anyone can
publish, ungated, no review. That's still correct for installation; what a
facility chooses to install is its own decision. What needs a gate is
narrower: what gets displayed on Mantid's own hosted catalog, since that
carries an implied endorsement a raw channel listing doesn't.

Reviewing "is this a real, distinct submission" is a much cheaper task than
reviewing extension code, and doesn't reintroduce the maintenance burden the
no-absorption policy protects against — no one is reviewing anyone's
implementation, just a few lines of metadata.

### Allowlist, gated by a PR and an automated ownership check

A maintainer submits a PR to a small index file:

```yaml
- name: gaussian-fit-suite
  repo: https://github.com/some-facility/gaussian-fit-suite
  maintainer_contact: jane.doe@facility.org
  verification_file: .mantid-extension-verify
```

An automated check fetches that file from the claimed repo and confirms it
matches — the same pattern as domain ownership verification (Google Search
Console, GitHub's verified domains): proving control of the thing being
claimed, without a human inspecting any code. A human only glances at the PR
to confirm it's a real, distinct submission. conda-forge's own
`staged-recipes` process works the same way and scales fine at their size.

The catalog site lists only the intersection: published on the channel *and*
present in the allowlist.

### Two different attacks, two different fixes

- **A fake or impersonated extension getting listed** — solved by the
  ownership-verification step above.
- **A malicious payload injected through README rendering** (a script tag,
  not just a bad link) — a solved problem already. Use a standard, hardened
  markdown sanitizer for rendering — the same category of tooling GitHub
  itself uses to render arbitrary READMEs safely — rather than naively
  rendering untrusted markdown/HTML.

## Staleness check: shrinks the attack surface, not just keeps things tidy

An old, quiet repo left in the allowlist is exactly the kind of target that
gets hit by account takeover or ownership-transfer hijacking — a compromised
or abandoned maintainer identity, still trusted, still listed. Purging stale
entries isn't only about freshness; it's closing that window.

**Primary signal:** the abi support window (N and N-1 supported for some
period) already defines "kept up to date" precisely. An extension that
hasn't published a release compatible with the current or N-1 abi within
that window is demonstrably unmaintained.

**Secondary signal:** no commits or releases on the source repo for 12-18
months, catching cases where the abi hasn't moved but the repo is obviously
abandoned regardless.

**Grace period, not silent delisting.** The same periodic re-verification job
that checks ownership also checks staleness. On a hit, it notifies the
allowlist entry's `maintainer_contact` with a window (30-60 days) to publish
a compatible release or confirm they're still active, before delisting. The
same contact field also serves as the channel for reaching maintainers about
breaking abi changes generally (see `open-questions.md`) — one field, two
uses, rather than a second notification path.

**Purging only ever means delisting from the catalog, never removing
anything from the channel.** A facility already depending on an old extension
is unaffected — it simply stops surfacing as something new users would
discover. Reinstatement is as lightweight as the original listing: a
maintainer publishing a compatible release again gets picked up automatically
on the next harvest run, not forced through onboarding a second time. The
gate is about freshness, not punishment.
