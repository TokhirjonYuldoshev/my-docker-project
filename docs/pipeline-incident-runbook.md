# CI/CD Pipeline Incident Runbook

This runbook defines deterministic triage for the repository's independent quality and delivery signals. The goal is to fix the owning layer, preserve evidence, and prevent auxiliary systems from hiding a real failure.

## Signal ownership

| Signal | Source of truth | Blocking? | First triage action |
| --- | --- | --- | --- |
| Flake8 | `Quality / Flake8` | Yes | Inspect static-analysis output and changed Python files |
| Pytest | `Tests / Pytest` | Yes | Inspect failing assertion/test collection and JUnit evidence |
| Docker build/runtime | `Docker / Build + runtime smoke` | Yes | Separate image-build failure from container-start/output failure |
| Container security | Trivy/security gate | Yes when configured as required | Identify fixable CRITICAL vulnerability and affected layer/package |
| Aggregate CI gate | `CI / Required gate` | Yes | Trace back to the first non-success required signal |
| Jenkins publish | Jenkins delivery stage | Yes for delivery | Separate pre-publish quality failure from registry/auth/push failure |
| Telegram | notification/diagnostic workflow | No | Treat as observability transport, not build health |

## Triage order

1. Start from the aggregate result and identify the first required signal that failed.
2. Open the owning job/stage and preserve its original logs and evidence.
3. Classify the failure as code quality, test behavior, packaging/runtime, security, delivery infrastructure, or observability transport.
4. Reproduce only the smallest failing path.
5. Fix the owning layer; do not weaken a downstream gate to compensate.
6. Validate through the same PR checks that detected the problem.

## Static-analysis failure

For Flake8 failures:

- use the exact rule/code and file/line from CI;
- change source/test code rather than suppressing the rule globally unless the rule is demonstrably incompatible with the project policy;
- rerun Flake8 independently before interpreting test or Docker signals.

## Test failure

For Pytest failures:

- distinguish collection/environment failures from assertion failures;
- inspect the failing test, observed value, expected contract, and JUnit evidence;
- do not modify the expected result merely to match an unexplained regression;
- keep tests deterministic and independent.

## Docker build/runtime failure

Build and runtime smoke are separate signals.

If build fails, inspect Dockerfile syntax, base-image availability, copied files, permissions, and build context.

If build succeeds but runtime smoke fails, inspect:

- container exit code;
- declared non-root runtime user and permissions;
- exact stdout contract;
- entrypoint/CMD behavior;
- runtime-only dependencies.

A successful Docker build is not proof that the resulting container starts correctly.

## Container-security failure

When the security gate reports a fixable CRITICAL vulnerability:

1. identify whether it originates in the base image or project-installed package;
2. prefer a patched compatible base/dependency version;
3. rebuild and run the same runtime smoke after remediation;
4. do not silence the finding merely to restore a green badge.

If a finding is not fixable, document the exact advisory, exposure, compensating controls, and review date before changing enforcement policy.

## Jenkins delivery failure

Classify the failing stage first:

- runtime/version validation;
- dependency installation;
- lint/test;
- image build/runtime smoke;
- Docker Hub authentication/publish;
- cleanup;
- Telegram notification.

Quality/test/runtime failures are product/pipeline signals. Registry and network failures are delivery-infrastructure signals. Telegram is observability only.

Never push an image after a required quality or runtime gate failed.

## Telegram-only failure

If all required build/test/security gates are green but Telegram delivery fails:

- preserve the successful pipeline result;
- use the manual Telegram diagnostic workflow to validate token, chat target, and API delivery independently;
- do not fail or weaken the product pipeline solely because notification transport is unavailable.

## External runner/platform incident

Evidence of an external incident includes failure before project logic executes, runner provisioning errors, registry/service outages, or unrelated network/package infrastructure errors.

Policy:

- preserve the original run;
- confirm the project revision itself did not introduce the failing behavior;
- allow at most one targeted diagnostic rerun after concrete evidence that the external condition recovered;
- never loop reruns until a random green result appears;
- never add arbitrary sleeps/retries as a permanent workaround for an external incident.

## Severity model

| Severity | Example | Response |
| --- | --- | --- |
| SEV-1 | Published image is known broken or critically vulnerable | Stop delivery/use; remediate immediately |
| SEV-2 | Required CI/security/runtime gate is broken on `main` | Block further delivery and restore the gate |
| SEV-3 | Docker Hub/Jenkins delivery unavailable while PR validation is healthy | Repair delivery path without weakening validation |
| SEV-4 | Telegram/reporting presentation issue only | Repair observability through normal change flow |

## Resolution criteria

An incident is resolved only when:

- the owning signal passes on the corrected revision;
- the aggregate gate reflects upstream results correctly;
- runtime/security evidence remains intact;
- no sleep, retry inflation, blanket ignore, or notification workaround masks the root cause;
- any newly discovered operational rule is documented.

## Anti-patterns

Do not:

- merge because unrelated jobs are green while a required gate is red;
- interpret a successful build as proof of a healthy runtime;
- publish after failing lint/tests/runtime/security validation;
- downgrade fixable CRITICAL vulnerabilities to cosmetic warnings;
- make Telegram a prerequisite for build health;
- rerun repeatedly until CI happens to pass;
- broaden ignore/suppression rules without a documented reason and scope.
