from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence


IMAGE = "qa-ci-smoke:local"
EXPECTED_OUTPUT = "Hello from Docker! The application is running successfully."


def run(command: Sequence[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"+ {' '.join(command)}", flush=True)
    return subprocess.run(
        list(command),
        check=True,
        text=True,
        capture_output=capture,
    )


def verify_python_runtime() -> None:
    if sys.version_info < (3, 12):
        raise RuntimeError(
            f"Python 3.12+ is required; current runtime is {sys.version.split()[0]}"
        )
    print(f"Python runtime: {sys.version.split()[0]}")


def verify_non_root_image() -> None:
    result = run(
        ["docker", "image", "inspect", IMAGE, "--format", "{{.Config.User}}"],
        capture=True,
    )
    configured_user = result.stdout.strip()
    if not configured_user or configured_user.lower() == "root" or configured_user == "0":
        raise RuntimeError(
            "Docker image must declare a non-root runtime user; "
            f"got {configured_user or '<empty>'!r}"
        )
    print(f"Non-root runtime user: {configured_user}")


def verify_container_contract() -> None:
    result = run(["docker", "run", "--rm", IMAGE], capture=True)
    actual = result.stdout.strip()
    if actual != EXPECTED_OUTPUT:
        raise RuntimeError(
            "Container stdout contract mismatch: "
            f"expected {EXPECTED_OUTPUT!r}, got {actual!r}"
        )
    print("Container runtime contract: PASS")


def cleanup_image() -> None:
    subprocess.run(
        ["docker", "image", "rm", "--force", IMAGE],
        check=False,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    verify_python_runtime()

    try:
        run([sys.executable, "-m", "pip", "check"])
        run(
            [
                sys.executable,
                "-m",
                "flake8",
                "app.py",
                "test_app.py",
                "scripts/verify-local.py",
                "--count",
                "--statistics",
            ]
        )
        run([sys.executable, "-m", "pytest", "-q"])
        run(["docker", "build", "--tag", IMAGE, "."])
        verify_non_root_image()
        verify_container_contract()
    finally:
        cleanup_image()

    print("Local quality preflight: PASS")
    print("Note: the blocking Trivy security gate remains owned by GitHub Actions.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Local quality preflight: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
