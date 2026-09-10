# Security Policy

This repository is a public QA/DevOps portfolio project. It contains CI, container, Jenkins and notification examples, but it must not contain real credentials.

## Supported state

Security fixes are applied to the current `main` branch. Historical commits and old portfolio branches are not maintained as separate supported versions.

## Reporting a security concern

If you find a security issue in the repository configuration, dependency setup, Docker image, Jenkins pipeline or credential handling:

1. do **not** publish real tokens, passwords, private registry credentials or other secrets in an issue, pull request, screenshot or log;
2. describe the affected file/component and the observable risk without including secret material;
3. use a private contact method listed on the maintainer's GitHub profile when the report itself contains sensitive information.

For an accidentally exposed credential, the first response is **revocation/rotation of the credential**, not merely deleting the Git line that contained it.

## CI security controls

The repository currently uses independent security/quality signals:

- pinned development dependencies with controlled Dependabot update pull requests;
- a Docker base-image update stream;
- a Trivy container scan that blocks fixable CRITICAL vulnerabilities;
- a non-root application user in the runtime image;
- read-only `contents` permission in GitHub Actions;
- Docker Hub and Telegram secrets supplied through Jenkins Credentials rather than repository files;
- an aggregate `CI / Required gate` that cannot pass when its security dependency fails.

Security findings are treated as engineering signals. The preferred response is to remove or mitigate the underlying risk rather than weakening a gate solely to restore a green pipeline.
