# Scope and non-goals

## Purpose

This repository is a compact QA/DevOps portfolio system for demonstrating deterministic quality gates around a deliberately small Python application.

The engineering value is in the pipeline contract rather than application complexity:

- static analysis and dependency integrity;
- unit-test evidence;
- container build and runtime validation;
- non-root runtime policy;
- container vulnerability scanning and CycloneDX SBOM evidence;
- aggregate CI gating;
- Jenkins delivery controls and non-blocking observability.

## What this repository proves

A revision is considered healthy only when the independent validation signals agree:

1. Python dependencies are internally consistent.
2. Flake8 passes.
3. Pytest passes and produces JUnit evidence.
4. The Docker image builds from the checked-in source.
5. The container starts and returns the expected observable output.
6. The image declares a non-root runtime user.
7. The Trivy security policy passes and SBOM generation succeeds.
8. The aggregate required gate remains green only when every blocking upstream gate is green.

## Non-goals

This project intentionally does **not** claim to be:

- a production application;
- a large automated test suite;
- a Kubernetes or cloud-deployment platform;
- a production SRE monitoring system;
- a substitute for environment-specific release approval.

Adding technologies without a real validation signal would make the repository noisier rather than stronger.

## Delivery boundary

GitHub Actions is the repository-level validation path. It does not publish Docker images.

Jenkins is the demonstration delivery path. Image publication is restricted to the verified main branch and uses Jenkins-managed credentials. Telegram is an observability channel only; notification delivery cannot rewrite the underlying pipeline result.

## Failure-handling principles

- Fail on observable product or pipeline contract violations.
- Preserve evidence before enforcing a failure where practical.
- Do not hide failures with arbitrary sleeps, rerun-until-green loops or permissive exit-code handling.
- Treat security, test, build and runtime signals independently before aggregation.
- Keep credentials outside source control.
- Prefer explicit runtime and dependency baselines over implicit latest-version behavior.

## Review rule

A pipeline change is complete only when its expected failure semantics are understandable from the diff and the repository CI confirms the changed contract.
