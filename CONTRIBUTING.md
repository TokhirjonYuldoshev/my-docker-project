# Contributing

This repository is a compact QA/DevOps portfolio project. Changes should stay small, reviewable and evidence-driven.

## Development baseline

- Python 3.12+
- Docker
- Git
- Jenkins only when validating the delivery pipeline locally/in a Jenkins agent

Install the pinned development tools:

```bash
python -m pip install --disable-pip-version-check -r requirements-dev.txt
python -m pip check
```

## Required local validation

Before opening a pull request that changes Python code, tests or Docker packaging, run the applicable checks:

```bash
python -m pip check
python -m flake8 app.py test_app.py --count --statistics
python -m pytest -q
docker build -t qa-ci-smoke:local .
docker image inspect qa-ci-smoke:local --format '{{.Config.User}}'
docker run --rm qa-ci-smoke:local
```

The image must declare a non-root runtime user and the container output must be exactly:

```text
Hello from Docker! The application is running successfully.
```

The blocking Trivy policy is enforced in GitHub Actions. Container/security changes are not ready to merge until the `Security / Trivy container scan` and aggregate `CI / Required gate` checks are green. CI retains the Trivy JSON report as security evidence and Pytest JUnit XML as test evidence.

## Change policy

- Prefer one focused concern per pull request.
- Do not bypass failing dependency-integrity, Flake8, Pytest, Docker runtime, non-root or Trivy gates.
- Do not weaken a test/security threshold only to make CI green.
- Do not add retries, sleeps or notification fallbacks that can mask the owning quality signal.
- Dependency updates must keep the documented Python runtime contract valid.
- Keep credentials out of source control. GitHub Actions Telegram secrets belong in repository secrets; Docker Hub and Jenkins Telegram credentials belong in Jenkins Credentials.
- Notification delivery is auxiliary observability; it must not hide the underlying build/test/security result.
- Docker Hub publishing remains a delivery action restricted to verified `main` refs.
- When behavior changes, update the relevant documentation in the same pull request.

## Pull request evidence

A pull request is ready to merge when:

1. the change is scoped and technically explained;
2. local validation is complete where applicable;
3. GitHub Actions reports green dependency integrity/Flake8, Pytest, Docker runtime/non-root and Trivy jobs;
4. `CI / Required gate` is green;
5. retained artifacts exist where applicable (JUnit and Trivy evidence);
6. any runtime/dependency/security impact is documented;
7. no secrets or generated local artifacts are included.

For a suspected runner/platform incident, follow `docs/pipeline-incident-runbook.md` rather than rerunning until green. A targeted diagnostic rerun is justified only after concrete external-failure evidence and recovery.

## CI/CD ownership

GitHub Actions is the merge-validation path. Jenkins is the delivery path that repeats quality checks and may publish a versioned Docker image from `main` before sending best-effort Telegram observability.

A successful GitHub Actions run proves repository-level validation, not the availability or correctness of external Jenkins/Docker Hub credentials. Conversely, a Telegram transport failure is not a substitute for a failed application, test, security or delivery signal.
