# Правила внесения изменений

Этот репозиторий — компактный QA/DevOps портфолио-проект. Изменения должны оставаться небольшими, понятными для review и подтверждаться evidence.

## Development baseline

- Python 3.12+
- Docker
- Git
- Jenkins — только когда требуется проверить delivery pipeline локально или на Jenkins agent

Установка зафиксированных development tools:

```bash
python -m pip install --disable-pip-version-check -r requirements-dev.txt
python -m pip check
```

## Обязательная локальная проверка

Предпочтительный детерминированный preflight:

```bash
python scripts/verify-local.py
```

Он проверяет Python 3.12+, dependency consistency, Flake8, Pytest, Docker build, declared non-root image user и exact container stdout contract. Temporary local image удаляется в cleanup даже при failure.

Эквивалентные отдельные команды:

```bash
python -m pip check
python -m flake8 app.py test_app.py scripts/verify-local.py --count --statistics
python -m pytest -q
docker build -t qa-ci-smoke:local .
docker image inspect qa-ci-smoke:local --format '{{.Config.User}}'
docker run --rm qa-ci-smoke:local
```

Image должен объявлять non-root runtime user, а stdout container должен точно совпадать с:

```text
Hello from Docker! The application is running successfully.
```

Blocking Trivy policy выполняется в GitHub Actions. Container/security change не готов к merge, пока `Security / Trivy container scan` и aggregate `CI / Required gate` не стали green. CI сохраняет Trivy JSON и CycloneDX SBOM как security/supply-chain evidence, а Pytest JUnit XML — как test evidence.

## Политика изменений

- Один Pull Request — одна сфокусированная задача.
- Нельзя обходить failing dependency-integrity, Flake8, Pytest, Docker runtime, non-root или Trivy gate.
- Нельзя ослаблять test/security threshold только ради green CI.
- Не добавляйте retry, sleep или notification fallback, способные замаскировать owning quality signal.
- Dependency updates должны сохранять documented Python runtime contract.
- Credentials не хранятся в source control. GitHub Actions Telegram secrets находятся в repository secrets; Docker Hub и Jenkins Telegram credentials — в Jenkins Credentials.
- Notification delivery — вспомогательная observability и не должна скрывать build/test/security result.
- Docker Hub publish остаётся delivery action только для verified `main` refs.
- Если behavior изменилось, связанную документацию обновляйте в том же PR.

## Evidence для Pull Request

PR готов к merge, когда:

1. change scoped и технически объяснён;
2. local preflight выполнен, где применимо;
3. GitHub Actions показывает green dependency integrity/Flake8, Pytest, Docker runtime/non-root и Trivy jobs;
4. `CI / Required gate` — green;
5. необходимые artifacts сохранены: JUnit XML, Trivy JSON, CycloneDX SBOM;
6. runtime/dependency/security impact задокументирован;
7. PR не содержит secrets или generated local artifacts.

При подозрении на runner/platform incident используйте [`docs/pipeline-incident-runbook.md`](docs/pipeline-incident-runbook.md), а не rerun-until-green. Один targeted diagnostic rerun допустим только после concrete evidence внешней ошибки и восстановления.

## Ownership CI/CD

GitHub Actions — merge-validation path. Jenkins — delivery path, который повторяет quality checks и может публиковать versioned Docker image из `main`, после чего отправляет best-effort Telegram observability.

Успешный GitHub Actions run подтверждает repository-level validation, но не доступность внешних Jenkins/Docker Hub credentials. Аналогично Telegram transport failure не является заменой application/test/security/delivery failure.
