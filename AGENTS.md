# Organization Agent Guide

Read `README.md` first for repository purpose and entry points.
Apply this guide before making changes.

## First-Principles Work

Before changing code, docs, schemas, scripts, templates, examples, governance,
or automation, reduce the task to observable behavior, root cause, invariant,
owner, data flow, and validation.

- Do not silently choose among plausible interpretations. State assumptions,
  surface conflicts, and ask when the decision materially changes the result.
- Deliver the complete requested behavior with bounded design. Do not stop at a
  toy result when production behavior is requested, and do not add abstraction,
  configurability, workflow machinery, or future-facing features unless the
  request, source evidence, or owning invariant requires them.
- Change the owning layer, not the nearest convenient file.
- Keep changes traceable to the request, source evidence, or owning invariant.
- Do not clean up, reformat, rename, or refactor unrelated nearby material
  unless it is required by the request or owning invariant.
- Use the strongest feasible validation for the result. If validation is
  skipped, say what was skipped and why.

Use this check:

1. What behavior is wrong, missing, or at risk?
2. What root cause explains it?
3. What invariant must hold?
4. Which artifact, layer, or workflow owns it?
5. What data or decision flows into that owner?
6. What remains variable, configurable, or case-local?
7. What evidence proves the result beyond one literal case?

## Canonical Artifacts

- Treat conversation, review feedback, plans, and intermediate attempts as
  editing input. Recompute the complete accepted result before finalizing.
- Active artifacts depend only on that result and their repository role, not
  on the editing path. Apply this to code, symbols, files, wrappers, branches,
  configuration, schemas, defaults, generated sources, scripts, templates,
  automation, comments, DocC, diagrams, tests, fixtures, snapshots, examples,
  and normative docs.
- If an intermediate result is `A + B` and the accepted result is `A`, express
  `A` directly. Remove `B` and its residual surface rather than retaining names
  such as `AOnly` or `AWithoutB`, or prose such as "B was removed."
- Normalize by semantic identity and artifact role, not by token. A rejected
  current capability does not invalidate a distinct historical fact,
  migration, ownership record, or safety boundary that uses the same term.
- Keep a negative constraint only when excluding `B` is independently required
  by a current compatibility, safety, or ownership invariant.
- A disabled B flag, skipped B test, dead B branch, retained B fixture, or
  "do not add B" rule is residue when it exists only because B was attempted;
  disabled state alone is not an invariant.
- Keep change history only in commits, pull requests, changelogs, release
  records, migrations, archives, or accepted decision records with durable
  value. Do not create a history artifact merely to preserve a correction.
- Preserve role-owned facts unless separate evidence changes them; do not
  rewrite history or ownership merely to make a rejected term disappear.
- Leave an already-correct history, migration, provenance, ownership, or safety
  artifact unchanged when the task does not change its facts. Do not polish or
  restate it merely because it is relevant to the current edit.
- Comments explain non-obvious current semantics and invariants, not the
  sequence of edits.
- Before handoff, verify that a new agent with no editing conversation can
  derive the complete current behavior, boundaries, and operating guidance
  without mentally subtracting a rejected concept.

## Task Route

- For the public organization entry point, edit `profile/catalog.json` and
  regenerate `profile/README.md`; `README.md` gives the commands.
- For conventions shared by every repository, read `MAINTENANCE.md`.
- Before changing shared version, plugin compatibility or dependency rules,
  read `VERSIONING.md`.
- For repository settings, GitHub Apps and Actions credentials, change
  `MAINTENANCE.md` with the setting; the organization check in
  [computer-mcp/github-workflows](https://github.com/computer-mcp/github-workflows)
  compares it with live settings.
- For visual identity, read `DESIGN.md`. Icon sources and their provenance
  live in `.github/design/icons/`, fonts in `.github/design/fonts/`, and
  `README.md` gives the generator and toolchain commands.
- For a reusable workflow or a check more than one repository needs, work in
  `computer-mcp/github-workflows`; this repository keeps only thin callers.
- For positioning, the tagline and other text rendered into images, read the
  main repository's
  [ProductIdentity](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Architecture/ProductIdentity.md).
- For the default community files, use the root governance files,
  `.github/ISSUE_TEMPLATE/` and the pull request template.
- Stop and clarify before mixing route instructions into `README` files or
  index text into `AGENTS.md`.

## Authority

- `AGENTS.md` is the agent guide: first-principles guardrails, task
  route, authority boundaries, and boundary guardrails.
- `README.md` indexes scope, icon generation, profile and social-preview
  rendering, and delivery.
- `MAINTENANCE.md` is current truth for cross-repository operating conventions.
  `VERSIONING.md` owns shared version and dependency rules; each repository
  owns its version sources, release procedure and written exceptions.
- `DESIGN.md` is current truth for visual identity and `profile/catalog.json`
  for the profile's repositories, groups and sentences. `profile/README.md`
  and the social previews are rendered from them; consumed icon copies are
  recorded in each icon's `provenance.json`.
- The main repository's ProductIdentity is current truth for product meaning.
- Root governance files and `.github/*` are GitHub-facing governance and the
  organization's default community files.

## Boundary Guardrails

After the owner and invariant are clear, classify concrete values by stability,
variability, and ownership before writing reusable artifacts.

Do not promote context-bound values into reusable artifacts. A value is
context-bound if it depends on the current machine, local workspace, current
input, one fixture, one runtime run, one user-specific path, or temporary
execution state.

Keep shipped documentation focused on current product facts, supported behavior,
and operating guidance. Keep temporary implementation notes, local evidence,
local paths, run-specific artifacts, and historical comparison notes out of
README files, the profile, `MAINTENANCE.md`, `DESIGN.md` and the community
files. Change history belongs in commits and pull requests.

Use this decision test:

- If a value changes by input, get it from input, spec, config, parameters, or
  an explicit user decision.
- If a value changes by environment, get it from configuration, runtime state,
  environment variables, or local execution notes.
- If a value belongs only to one example, fixture, or run, keep it there. Do
  not generalize it into reusable docs, schemas, templates, scripts,
  validation rules, or automation.
- If the artifact being edited is not the source of truth for the value, do not
  hardcode it there. Pass it in, derive it, configure it, or link to the
  owning artifact.
- Only stable invariants and values owned by the current artifact may be fixed
  in reusable artifacts.

Classify concrete values before writing:

1. Name the variable parts.
2. Decide which artifact owns each variable.
3. Replace context-bound literals with placeholders, parameters, config keys,
   derived values, or links to the owning artifact.
4. Keep concrete literals only inside the artifact that owns them.

When in doubt, use a placeholder, parameter, configuration key, or repo-owned
source of truth instead of a literal value.

## Operating Notes

- Keep Agent Guide and Index separate.

## Repository Guardrails

- Text rendered into images must match ProductIdentity. Preserve repository
  visibility and integration ownership.
- Change `DESIGN.md` or `profile/catalog.json`, regenerate, and commit inputs
  and outputs together. Never edit generated files by hand.
- Before committing, lint DESIGN and check the profile with the
  `github-readme-design` toolchain.
- Deliver icons and social previews to other repositories through a pull
  request in each repository, and record each consumed copy in the icon's
  `provenance.json`.
- Keep `.agent/` local and untracked. Profile content must be understandable
  from committed artifacts alone.
