# Runbook по инцидентам CI/CD-пайплайна

Этот документ задаёт детерминированный triage независимых quality и delivery signals. Цель — исправить owning layer, сохранить evidence и не позволить вспомогательным системам скрыть реальный failure.

## Владельцы сигналов

| Сигнал | Source of truth | Блокирует | Первое действие |
| --- | --- | --- | --- |
| Flake8 | `Quality / Flake8` | Да | Проверить static-analysis output и изменённые Python files |
| Pytest | `Tests / Pytest` | Да | Проверить failing assertion/collection и JUnit evidence |
| Docker build/runtime | `Docker / Build + runtime smoke` | Да | Разделить image-build failure и container runtime/output failure |
| Container security | `Security / Trivy container scan` | Да | Найти fixable `CRITICAL` и affected layer/package |
| Aggregate CI gate | `CI / Required gate` | Да | Вернуться к первому обязательному upstream signal с non-success result |
| Jenkins publish | Jenkins delivery stage | Да для delivery | Разделить pre-publish quality failure и registry/auth/push failure |
| Telegram | notification/diagnostic workflow | Нет | Считать observability transport, а не build health |

## Порядок triage

1. Начните с aggregate result и найдите первый обязательный failing signal.
2. Откройте owning job/stage и сохраните его исходные logs/evidence.
3. Классифицируйте failure: code quality, test behavior, packaging/runtime, security, delivery infrastructure или observability transport.
4. Воспроизводите только минимальный failing path.
5. Исправьте owning layer; не ослабляйте downstream gate для компенсации.
6. Проверьте исправление теми же PR checks, которые обнаружили проблему.

## Ошибка static analysis

Для Flake8 failure:

- используйте точный rule/code и file/line из CI;
- исправляйте source/test code, а не отключайте правило глобально, если нет доказанной несовместимости с project policy;
- отдельно повторите Flake8 перед интерпретацией test или Docker signals.

## Ошибка теста

Для Pytest failure:

- отделите collection/environment problem от assertion failure;
- проверьте failing test, observed value, expected contract и JUnit evidence;
- не меняйте expected result только ради соответствия необъяснённой regression;
- сохраняйте tests детерминированными и независимыми.

## Ошибка Docker build/runtime

Build и runtime smoke — разные сигналы.

Если падает build, проверяйте Dockerfile syntax, base-image availability, copied files, permissions и build context.

Если build успешен, но runtime smoke падает, проверяйте:

- container exit code;
- declared non-root runtime user и permissions;
- exact stdout contract;
- entrypoint/CMD behavior;
- runtime-only dependencies.

Успешный Docker build **не доказывает**, что container корректно запускается.

## Ошибка container security

Если security gate сообщает fixable `CRITICAL` vulnerability:

1. определите, пришла она из base image или project-installed package;
2. предпочитайте patched compatible base/dependency version;
3. пересоберите image и повторите тот же runtime smoke;
4. не suppress finding только ради green badge.

Если finding не имеет исправления, перед изменением enforcement policy документируются exact advisory, exposure, compensating controls и review date.

## Ошибка Jenkins delivery

Сначала классифицируйте failing stage:

- runtime/version validation;
- dependency installation;
- lint/test;
- image build/runtime smoke;
- Docker Hub authentication/publish;
- cleanup;
- Telegram notification.

Quality/test/runtime failures — product/pipeline signals. Registry/network failures — delivery-infrastructure signals. Telegram — только observability.

Нельзя публиковать image после failure обязательного quality или runtime gate.

## Только Telegram failure

Если все обязательные build/test/security gates зелёные, а Telegram delivery упал:

- успешный pipeline result сохраняется;
- manual Telegram diagnostic workflow проверяет token, chat target и API delivery отдельно;
- product pipeline не ослабляется и не объявляется failed только из-за notification transport.

## External runner/platform incident

Evidence внешнего incident: failure до project logic, runner provisioning error, registry/service outage или unrelated network/package infrastructure problem.

Политика:

- сохранить original run;
- подтвердить, что project revision не внесла failing behavior;
- разрешить максимум один targeted diagnostic rerun после concrete evidence восстановления внешнего условия;
- не перезапускать до случайного green;
- не добавлять permanent arbitrary sleep/retry как workaround.

## Модель severity

| Severity | Пример | Реакция |
| --- | --- | --- |
| SEV-1 | Опубликованный image заведомо сломан или критически уязвим | Остановить delivery/use и исправить немедленно |
| SEV-2 | Required CI/security/runtime gate сломан на `main` | Блокировать дальнейший delivery и восстановить gate |
| SEV-3 | Docker Hub/Jenkins недоступен при здоровой PR validation | Исправить delivery path без ослабления validation |
| SEV-4 | Только Telegram/reporting presentation issue | Исправить observability обычным change flow |

## Критерии закрытия

Incident закрыт только когда:

- owning signal проходит на corrected revision;
- aggregate gate корректно отражает upstream results;
- runtime/security evidence сохранено;
- sleep, retry inflation, blanket ignore или notification workaround не маскируют root cause;
- новое operational rule, выявленное incident, задокументировано.

## Запрещённые практики

Нельзя:

- мержить только потому, что unrelated jobs green, если required gate red;
- считать successful build доказательством healthy runtime;
- публиковать image после failing lint/tests/runtime/security validation;
- превращать fixable `CRITICAL` в косметический warning;
- делать Telegram prerequisite для build health;
- repeatedly rerun до случайного pass;
- расширять ignore/suppression без документированного reason и scope.
