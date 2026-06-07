# GitHub Classroom Guide

## Overview

This repository is set up with GitHub Classroom for automated grading. The workflow file `.github/workflows/ci.yml` will automatically run CI checks when you push to your repository.

## CI Workflow

The GitHub Actions workflow runs two main checks:

1. **Structure Check** (`ci/check_structure.py`) - Verifies all required files are present
2. **Smoke Test** (`ci/smoke_imports.py`) - Ensures all Python modules can be imported without errors

## How to Submit

1. Fork or clone this repository
2. Complete the lab assignments
3. Commit and push your changes
4. The CI will automatically run and check your submission

## Required Files

Make sure all required files are present before pushing:

```
README.md
REPORT_TEMPLATE.md
RUBRIC_LAB7.md
requirements.txt
configs/
docs/
src/
ci/
outputs/
```

## Checking Locally

You can run the structure check locally:

```bash
python ci/check_structure.py
```

And the smoke test:

```bash
python ci/smoke_imports.py
```

## Getting Help

If you encounter issues with the CI workflow, check:
1. All required files exist
2. Python imports work correctly
3. Output files are in the correct directories
