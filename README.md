# eTRAIN Shared Schema

This package centralizes the Pydantic models that define the contract between the
etrain agents, Django server, and Ionic Angular front end. Install it in any
Python environment to guarantee consistent validation, then generate matching
TypeScript interfaces for the Angular client.

## Python installation

```bash
# from the repo root
pip install .
```

After installation the models live under `etrain_schema`. Example:

```python
from etrain_schema import ClassroomSummary
summary = ClassroomSummary(classroom_overview=..., ...)
```

## Generate TypeScript typings

The project exposes a CLI that converts the packaged Pydantic models to
TypeScript interfaces using `pydantic2ts`.

```bash
# default output: typescript/etrain-schema.d.ts
etrain-schema-ts

# or specify a custom file
etrain-schema-ts --out ../etrain-ionic/src/app/types/etrain-schema.d.ts
```

Re-run the command whenever the Python models change. The generator only writes
the file if the contents changed to avoid needless churn.

## Angular usage

1. Generate the declaration file inside the Ionic repo (see above).
2. Reference the interfaces directly in services/components:

```ts
import type { ClassroomSummary } from '../types/etrain-schema';
```

Because the output is standard TypeScript, no Angular-specific tooling is
required.

## npm package

The repository now exposes a lightweight npm package that ships the generated
TypeScript declarations in `dist/`.

```bash
# install straight from the repo (local path)
npm install ../etrain_schema

# or point to the git repo/branch directly
npm install git+ssh://git@github.com/deCervo/etrain-ionic.git#main:etrain_schema
```

After installation you can import the interfaces via the package name:

```ts
import type { ClassroomSummary } from '@decervo/etrain-schema';
```

When schemas change, regenerate the published typings before packaging:

```bash
source .venv/bin/activate  # once
npm run build:ts            # updates dist/etrain-schema.d.ts
npm pack                    # optional, creates the tarball for distribution
```

## Development

- `pip install -e .[dev]`
- Run `pytest` or `ruff check .` as needed.
- `npm run build:ts` regenerates the declaration bundle inside `dist/`.
- Commit the updated `dist/` artifacts before publishing/installing via npm.


Version 0.2.1 adds optional `movement_counts` to department learning progress. These retain
statistical category keys and add `positive_movement` and `negative_movement`
for display. Original `classification_counts` are unchanged; older reports omit
the optional field. Install `v0.2.1` or later in Django before deploying consumers that require
movement counts.

Version 0.2.2 adds optional `classification_usernames`
with `improving` and `declining` username lists. These are authoritative backend
classifications for authorized department reports, not model-inferred identities.
Only usernames are included; first names and last names are not part of this
contract. Older reports may omit the field or use null; an empty list means no
officers in that classification. Existing cohort-suppression rules are unchanged.
Install v0.2.2 in Django before deploying the
report feature; version 0.2.1 does not preserve these lists during normalization.

Version 0.2.3 report snapshots add optional `report_snapshot` metadata to graded
department reports (`active_only`, ISO capture time, selected user count) and
`selected_officer_count` to department learning progress. Legacy reports may
omit both. Active count remains the actual number of active officers; the
selected count also includes inactive officers for all-user reports. These
fields require v0.2.3 installed before backend deployment. Optional
`paired_user_count` identifies unavailable prompt-type comparisons without
misrepresenting missing data as a measured zero.
