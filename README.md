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
