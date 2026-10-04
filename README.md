# Jev CI branch comparison demo

A small, deliberately seeded example created with a coding agent for a video about [Jev CI](https://github.com/krisitown/jev-quality-gate).

Two alternative pull requests add ordered label replacement to the same `main` baseline:

- `storage-leak`: the application service deletes rows, assigns row positions, inserts replacements, and flushes through a port interface.
- `storage-owned`: the application service delegates to the existing `replace_labels` operation.

Both versions produce the same results in the five supplied behavioral cases and import only the port from the application layer. The example illustrates storage procedure leaking through an interface. It is not a campaign result or a held-out accuracy benchmark.

## Run Jev CI

Install Jev CI using its README. Set `AI_GATEWAY_API_KEY` in your shell, or pass `--env-file` with your private key file. Run from this checkout on `main`, so `.jev-ci` is the trusted baseline control bundle. Fetch both PR branches before evaluating.

```sh
git fetch origin
jev-ci validate --config .jev-ci/config.json
jev-ci evaluate --repo . --source origin/storage-leak --target origin/main \
  --config .jev-ci/config.json --output /tmp/jev-leak-pack
open /tmp/jev-leak-pack/report.html
jev-ci evaluate --repo . --source origin/storage-owned --target origin/main \
  --config .jev-ci/config.json --output /tmp/jev-owned-pack
open /tmp/jev-owned-pack/report.html
```

Choose fresh output paths for each run. Evaluation makes hosted API calls. This illustrative policy is report-only: findings do not fail CI. Live judgments can vary.

## Behavioral and import checks

```sh
git switch storage-leak
python3 -m unittest discover -s tests -v
git switch storage-owned
python3 -m unittest discover -s tests -v
git switch main
```

On `main`, feature tests are skipped because the new service operation does not exist yet. Both feature branches run the same tests. These checks verify behavior and direct imports; the Jev policy evaluates responsibility ownership.

## Policy

The baseline `.jev-ci` folder contains the unchanged exploratory `responsibility-boundary-leakage` policy and hash-bound conventions from Jev CI. Its central rule is:

> A responsibility should not depend on another responsibility's internal procedure or representation without an evidenced need.

Keep both PRs open for the demonstration; they are alternative implementations, not changes to merge together.
