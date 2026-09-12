## Краткое описание

<!-- Опишите одну сфокусированную инженерную задачу и зачем она нужна. -->

## Область риска

- [ ] Python behavior / tests
- [ ] GitHub Actions / quality gates
- [ ] Docker image / runtime
- [ ] Dependencies / security
- [ ] Jenkins delivery / credentials / notifications
- [ ] Только документация

## Проверка

Отметьте evidence, относящееся к этому изменению:

- [ ] `Quality / Flake8`
- [ ] `Tests / Pytest`
- [ ] `Docker / Build + runtime smoke`
- [ ] `Security / Trivy container scan`
- [ ] `CI / Required gate`
- [ ] Jenkins-specific behavior проверено, если менялся `Jenkinsfile`

Ссылки на run/evidence:

<!-- Добавляйте ссылки, когда они помогают review или failure triage. -->

## Защитные условия

- [ ] В repository не попали token, password или registry credential
- [ ] GitHub Actions CI не публикует images и не требует external delivery secrets
- [ ] Functional/test failure не маскируется notification/cleanup logic
- [ ] Docker runtime validation по-прежнему запускает собранный image
- [ ] Security policy не ослаблена ради green dependency update
- [ ] Документация соответствует реализованному pipeline
- [ ] PR не содержит unrelated workaround или scope creep

## Классификация исходной ошибки

Если PR исправляет failure, укажите owning signal:

- [ ] Application/test behavior
- [ ] Packaging/container runtime
- [ ] Dependency/security
- [ ] Jenkins/registry delivery
- [ ] Только notification/observability
- [ ] Не применимо
