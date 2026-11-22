# Infrastructure Policy Release Gate — Starter Repository

**Fictional demo project.** This starter contains a small policy checker, 18 wholly synthetic resource records, and Python standard-library unit tests. It does not connect to AWS and contains no credentials or real customer information.

## Scenario

A platform team needs a repository release gate that checks proposed infrastructure inventory changes for encryption, public access, tagging, logging, and recovery rules. A change must fail checks when a resource is noncompliant, and pass again when corrected.

## Starting point

The seeded app and tests are supplied as *preparation*. This repository intentionally **does not contain a GitHub Actions workflow or branch ruleset**. Your recorded task is to create and configure those yourself in GitHub, then demonstrate the actual behavior.

### Commands for PRE-RECORDING practice only

```bash
python -m unittest discover -s tests -v
python -m scripts.check_inventory
```

Expected baseline: 11 passing unit tests and an inventory report with 18/18 resources passing. `reports/policy-report.json` is generated and ignored by Git.

## Desired recorded outcome (GitHub Advanced candidate)

1. Create a multi-stage GitHub Actions pipeline on pull requests and pushes, using minimal permissions.
2. Run unit tests and the inventory validation, and save the generated `reports/policy-report.json` as a workflow artifact.
3. Show a genuine failing check by changing `encryption_enabled` to `false` for `demo-bucket-01` on a separate branch and opening a pull request.
4. Correct the policy violation, rerun, and demonstrate green checks.
5. Configure a `main` branch ruleset requiring pull requests and the actual CI status checks (if supported by your account/repository).
6. Export the finished repository via **Code > Download ZIP** for your Workada output file; verify that it contains the workflow file.

## Recording safety

Do not record a real work account or real data. Sign in and set up the account before recording. Use GitHub's normal web UI during the recording, with Bloom set to Entire screen and the Workada timer running. Do not use AI assistance, macros, or custom automation during recording. Read the tool-specific Workada Calibration directions first; they control the evaluation rules.
