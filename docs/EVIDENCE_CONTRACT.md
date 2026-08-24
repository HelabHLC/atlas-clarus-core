# Evidence contract

ATLAS Clarus separates two evidence levels:

- `schemas/binding-record.schema.json` records one atomic deterministic binding.
- `schemas/run-manifest.schema.json` records a complete Workflow v3.4.0 execution context, including the input and master hashes, operating mode, candidate corridor, selection rule, binding records, and the status of later evidence layers.

A valid binding record is not by itself proof of a complete v3.4.0 run. Likewise, a runtime `PASS` does not imply persistence, cross-system, device, or measured-QC evidence.

## CI gates

The public CI job runs deterministic synthetic contract tests and validates both evidence schemas on every push and pull request. These tests require no third-party master asset.

The real-master job is deliberately separate. It runs only on a trusted self-hosted runner when repository variable `ATLAS_CLARUS_REAL_MASTER_GATE` is `enabled` and `ATLAS_CLARUS_MASTER_PATH` points to the authorised local master. `AtlasMaster.load()` verifies the frozen SHA-256 before PKL deserialisation. The job covers both known POSTHOC fixtures and an ACTIVE two-ID regression.

This separation prevents the absence of a redistributable master asset from weakening the public contract tests while retaining a defined verified-real-master gate.

The real-master regression matrix is stored in `tests/fixtures/real_master_regressions.json`. It currently covers four POSTHOC bindings (including exact and non-zero nearest matches) and an ACTIVE two-ID change. Master validation also enforces the frozen row count/index, finite λ fields, and `delta_lambda_nm = lambda_v2_nm - lambda_ee_nm` within a documented `0.001 nm` absolute tolerance.

## Manifest construction

`atlas_clarus.build_run_manifest()` constructs the complete record from one `BindingResult` per processed pixel. It rejects mixed operating modes, non-frozen master hashes, malformed input hashes, and POSTHOC records that alter source identity. Repeated atomic bindings are deduplicated while the two-ID evidence retains exact pixel counts and fractions, Source→Production mapping, production RGB rank, Δλ values, and the selection reason.
