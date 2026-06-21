from __future__ import annotations

import time

from clickadvisor.core.version import detect_version, parse_version


def test_detect_version() -> None:
    version = None
    for _ in range(30):
        version = detect_version("http://localhost:8123", user="default", password="clickadvisor")
        if version is not None:
            break
        time.sleep(1)

    assert version is not None
    major, minor = parse_version(version)
    assert major >= 22
    assert minor >= 0
