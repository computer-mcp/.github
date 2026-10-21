# Plugin release workflow

The reusable [workflow](../../.github/workflows/plugin-release.yml) builds and
publishes reproducible plugin packages. [VERSIONING.md](../../VERSIONING.md#plugin-release-contents)
owns the contents, receipt schema, provenance and recovery rules. Codex uses its
documented native artifact promotion exception.

## Caller

Add `.github/workflows/release.yml` in the plugin repository, substituting the
full standards commit SHA and the exact artifact name from its `ci.yml`:

```yaml
name: Release
on:
  workflow_dispatch:
    inputs:
      ref:
        description: Version tag, or commit for a dry run
        type: string
        required: true
      publish:
        description: Publish the verified release
        type: boolean
        default: false
permissions: {}
jobs:
  release:
    permissions:
      contents: write
      actions: read
    uses: computer-mcp/.github/.github/workflows/plugin-release.yml@<full-commit-sha> # master
    with:
      ref: ${{ inputs.ref }}
      publish: ${{ inputs.publish }}
      build: python3 Scripts/build_package.py
      ci_artifact: <exact-ci-artifact-name-with-${commit}>
  notify-catalog:
    needs: release
    if: needs.release.outputs.published == 'true'
    permissions: {}
    uses: ./.github/workflows/notify-catalog.yml
    secrets:
      CATALOG_APP_PRIVATE_KEY: ${{ secrets.CATALOG_APP_PRIVATE_KEY }}
```

`notify-catalog.yml` is the caller repository's existing reusable notification
workflow. It receives the catalog App private key; the release workflow has no
secret inputs. Its `verify` job receives only `contents: read` and
`actions: read`; its `publish` job receives only `contents: write`. The caller
grants the permission ceiling needed by both jobs. Verification executes the
build command without passing its GitHub token into the build environment.
Publication does not check out the caller or run its build command.

| Input | Contract |
| --- | --- |
| `ref` | Required. `vX.Y.Z` (including `-alpha.N`, `-beta.N`, `-rc.N`) for publication; a version tag or commit for a dry run |
| `publish` | Boolean, default `false` |
| `build` | Required shell command run at the source checkout; a quoted absolute output-directory argument is appended. It must create that directory with only the plugin ZIP archives |
| `ci_artifact` | Required exact artifact name from `ci.yml`; `${commit}` expands to the resolved full commit SHA. For matrix jobs, choose one exact matrix member |
| `runner` | Verification runner, default `ubuntu-24.04`; publication runs on `ubuntu-24.04`. Python 3.13 is supplied for verification |

| Output | Contract |
| --- | --- |
| `published` | String `true` after publishing or verifying an already public release; `false` for a dry run |
| `release_id` | Published GitHub Release ID, empty for a dry run |
| `tag` | Verified version tag, empty for an untagged commit dry run |

The release workflow must be pinned by its full commit SHA. It loads its helper
from that immutable workflow revision, found in the caller run's
`referenced_workflows` metadata. An embedded SHA-256 checks the helper both
before verification and before publication; caller code cannot supply an
executable publisher. The receipt digest passed between jobs binds the bundle
to verification, and publication checks the archive hashes and `SHA256SUMS`
before any Release write.

## Run and recover

1. Obtain successful default-branch push CI for the candidate commit. Set
   `ci_artifact` to its exact artifact name, including any matrix suffix.
2. Dispatch with that commit and `publish: false`. Inspect the
   `plugin-release-<run-id>-<attempt>` Actions artifact: `assets/` contains the
   verified ZIPs, deterministic `release-receipt.json` and `SHA256SUMS`.
   An untagged dry run reports the signed annotated tag still required.
3. Perform the plugin repository's manual archive acceptance. Create the signed
   annotated version tag on that same commit. Record the manual results and
   limits in a draft Release's notes, targeting the full commit SHA.
4. Dispatch with the version tag and `publish: true`. The workflow verifies the
   tag signature through GitHub, the manifest version and `plugin_api`, the CI
   source and archive set, then rebuilds and assembles the same release files.
   It creates a draft if none exists, uploads the receipt first, completes and
   verifies all assets, and publishes. The dependent job requests catalog
   reconciliation only after `published` is `true`.

A failed publication can be rerun. A complete receipt in a draft freezes its
provenance: verification downloads the recorded CI artifact by ID and checks its
digest, rebuilds against those bytes, and reproduces the same receipt and
checksums. A new CI attempt or a new release workflow pin does not change it.
If receipt upload itself was incomplete, no source has been frozen yet.

Missing assets are uploaded; matching completed assets are retained. Only
expected `starter` assets in a draft are removed and uploaded again. A completed
asset conflict requires inspecting the unpublished draft and its intended
source; the workflow does not replace it. If the recorded CI artifact expired
or was removed, delete the unpublished draft, obtain fresh successful CI
artifacts and dispatch again. This deliberately starts a new assembly with new
provenance. Published tags and assets remain immutable.

An already public release is checked against its frozen receipt and exact asset
set and reported as published without writes. Verification still rebuilds the
archives; it can compare against the public archive bytes after CI retention
has expired. Notification failure needs only a rerun of the notification job or
a manual dispatch of `notify-catalog.yml`; publication need not be repeated.

## Maintaining the shared workflow

Release logic lives in `Scripts/plugin_release.py`, behind a four-operation
GitHub API interface. The offline tests use an in-memory API and inject failures
before and after draft creation, every asset upload, starter deletion and
publication. They also exercise provenance recovery, immutable public releases,
source checks, archive comparison and the workflow's helper boundary.

When changing the helper, update `PLUGIN_RELEASE_SHA256` in the workflow to its
SHA-256. The repository CI runs the offline suite and verifies that digest:

```sh
python3 -m unittest discover -s Tests
actionlint .github/workflows/*.yml
```
