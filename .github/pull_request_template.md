## Summary

<!-- Describe one focused engineering outcome and why it is needed. -->

## Risk area

- [ ] Python behavior / tests
- [ ] GitHub Actions / quality gates
- [ ] Docker image / runtime
- [ ] Dependency / security
- [ ] Jenkins delivery / credentials / notifications
- [ ] Documentation only

## Verification

Mark the evidence relevant to this change:

- [ ] Quality / Flake8
- [ ] Tests / Pytest
- [ ] Docker / Build + runtime smoke
- [ ] Security / Trivy container scan
- [ ] CI / Required gate
- [ ] Jenkins-specific behavior reviewed when Jenkinsfile changed

Evidence / run links:

<!-- Add links when they help review or failure triage. -->

## Safeguards

- [ ] No token, password or registry credential was committed
- [ ] CI does not publish images or require external secrets
- [ ] A functional test failure is not masked by notification/cleanup logic
- [ ] Docker runtime validation still exercises the built image
- [ ] Security policy was not weakened to make a dependency update green
- [ ] Documentation matches the implemented pipeline
- [ ] No unrelated workaround or scope creep is bundled into this PR

## Failure classification

If this PR responds to a failure, classify the original signal:

- [ ] Application/test behavior
- [ ] Packaging/container runtime
- [ ] Dependency/security
- [ ] Jenkins/registry delivery
- [ ] Notification/observability only
- [ ] Not applicable
