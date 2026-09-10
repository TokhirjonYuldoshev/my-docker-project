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
```

## Required local validation

Before opening a pull request, run:

```bash
python -m flake8 app.py test_app.py --count --statistics
python -m pytest -q
docker build -t qa-ci-smoke:local .
docker run --rm qa-ci-smoke:local
```

The container output must be exactly:

```text
Hello from Docker! The application is running successfully.
```

## Change policy

- Prefer one focused concern per pull request.
- Do not bypass failing Flake8, Pytest, Docker build or runtime-smoke gates.
- Do not weaken a test or quality gate only to make CI green.
- Dependency updates must keep the documented Python runtime contract valid.
- Keep credentials out of source control. Docker Hub and Telegram secrets belong in Jenkins Credentials only.
- Notification delivery is auxiliary observability; it must not hide the underlying build result.
- When behavior changes, update README documentation in the same pull request.

## Pull request evidence

A pull request is ready to merge when:

1. the change is scoped and technically explained;
2. local validation is complete where applicable;
3. GitHub Actions reports green Flake8, Pytest and Docker runtime-smoke jobs;
4. any runtime/dependency compatibility impact is documented;
5. no secrets or generated local artifacts are included.

## CI/CD ownership

GitHub Actions is the merge-validation path. Jenkins is the delivery path that may publish a versioned Docker image and send Telegram notifications. A successful GitHub Actions run does not prove that Docker Hub or Telegram credentials are configured on a Jenkins agent.
