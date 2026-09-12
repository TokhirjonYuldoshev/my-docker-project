# Политика безопасности

Это публичный QA/DevOps портфолио-проект с примерами CI, Docker, Jenkins и notification integration. Реальные credentials в репозитории **не допускаются**.

## Поддерживаемое состояние

Security fixes применяются к текущей ветке `main`. Исторические commits и старые portfolio branches не поддерживаются как отдельные версии.

## Как сообщить о проблеме безопасности

Если найдена проблема в repository configuration, dependency setup, Docker image, Jenkins pipeline или credential handling:

1. **не публикуйте** реальные tokens, passwords, private registry credentials или другие secrets в Issue, Pull Request, screenshot или log;
2. опишите затронутый file/component и observable risk без чувствительных значений;
3. если сам report содержит sensitive information, используйте приватный контакт из GitHub-профиля владельца.

При случайном раскрытии credential первое действие — **revocation/rotation**, а не только удаление строки из Git. Значение могло остаться в истории.

## Текущие security controls

Репозиторий использует независимые security/quality signals:

- pinned development dependencies и controlled Dependabot Pull Requests;
- отдельный update stream для Docker base image;
- Trivy container scan, блокирующий fixable `CRITICAL` vulnerabilities;
- CycloneDX container SBOM как supply-chain evidence;
- non-root application user в runtime image;
- read-only `contents` permission в GitHub Actions;
- Docker Hub и Telegram secrets через Jenkins Credentials, а не repository files;
- GitHub Actions Telegram credentials через repository secrets;
- `CI / Required gate`, который не может стать green при failure обязательного security dependency.

Security findings рассматриваются как инженерные сигналы. Предпочтительное действие — убрать или снизить реальный риск, а не ослабить gate только ради зелёного pipeline.
