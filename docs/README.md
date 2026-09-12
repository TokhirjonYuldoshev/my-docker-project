# Карта документации

Основной язык человекочитаемой документации проекта — русский. Технические имена jobs, checks, commands, variables и file paths сохраняются без перевода, чтобы текст точно соответствовал CI и коду.

## Документы

| Документ | Назначение |
| --- | --- |
| [`scope-and-nongoals.md`](scope-and-nongoals.md) | Честный scope проекта, что он доказывает и чего не заявляет |
| [`pipeline-incident-runbook.md`](pipeline-incident-runbook.md) | Signal ownership, triage, severity и resolution criteria для CI/CD incidents |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Change policy, local preflight и evidence перед merge |
| [`../SECURITY.md`](../SECURITY.md) | Работа с secrets и security findings |

## Быстрая навигация

- Нужно понять **зачем существует проект и где его границы** → `scope-and-nongoals.md`.
- Упал GitHub Actions или Jenkins → `pipeline-incident-runbook.md`.
- Готовится изменение/PR → `CONTRIBUTING.md`.
- Найден credential или security concern → `SECURITY.md`.
- Общий обзор GitHub Actions, Jenkins, Docker, Trivy и Telegram → корневой [`README.md`](../README.md).

Structured incident intake находится в `.github/ISSUE_TEMPLATE/pipeline_incident.yml`, а review checklist — в `.github/pull_request_template.md`.
