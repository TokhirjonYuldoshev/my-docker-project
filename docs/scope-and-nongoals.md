# Scope и non-goals проекта

## Назначение

Этот репозиторий — компактная QA/DevOps portfolio system для демонстрации детерминированных quality gates вокруг намеренно небольшого Python-приложения.

Инженерная ценность находится в pipeline contract, а не в сложности приложения:

- static analysis и dependency integrity;
- unit-test evidence;
- container build и runtime validation;
- non-root runtime policy;
- container vulnerability scanning и CycloneDX SBOM evidence;
- aggregate CI gating;
- Jenkins delivery controls и non-blocking observability.

## Что репозиторий действительно доказывает

Revision считается healthy только когда независимые validation signals согласованы:

1. Python dependencies внутренне совместимы.
2. Flake8 проходит.
3. Pytest проходит и создаёт JUnit evidence.
4. Docker image собирается из checked-in source.
5. Container запускается и возвращает ожидаемый observable output.
6. Image объявляет non-root runtime user.
7. Trivy security policy проходит, а SBOM generation завершается успешно.
8. `CI / Required gate` остаётся green только когда все blocking upstream gates green.

## Что не является целью

Проект намеренно **не заявляет себя** как:

- production application;
- большая automated test suite;
- Kubernetes или cloud-deployment platform;
- production SRE monitoring system;
- замена environment-specific release approval.

Добавление технологий без нового проверяемого сигнала сделало бы репозиторий шумнее, а не сильнее.

## Граница delivery

GitHub Actions — repository-level validation path. Он не публикует Docker images.

Jenkins — демонстрационный delivery path. Публикация image разрешена только для verified `main` и использует Jenkins-managed credentials. Telegram — observability channel; notification delivery не может переписать underlying pipeline result.

## Принципы обработки ошибок

- Fail на observable product или pipeline contract violation.
- Где возможно, сохранять evidence до enforcement failure.
- Не скрывать failures через arbitrary sleeps, rerun-until-green loops или permissive exit-code handling.
- Рассматривать security, test, build и runtime signals независимо до aggregation.
- Хранить credentials вне source control.
- Предпочитать explicit runtime/dependency baselines неявному `latest` behavior.

## Правило review

Изменение pipeline считается завершённым только когда ожидаемые failure semantics понятны из diff, а CI репозитория подтверждает изменённый contract.
