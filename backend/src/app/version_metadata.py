"""Sift product and upstream version metadata."""

import os
from importlib.resources import files


def _version_file(name: str) -> str:
    return files("app").joinpath(name).read_text(encoding="utf-8").strip()


def get_version_metadata() -> dict[str, str]:
    commit = os.environ.get("BUILD_COMMIT", "unknown")
    return {
        "sift_version": _version_file("SIFT_VERSION"),
        "upstream_name": "NewsGator",
        "upstream_version": _version_file("NEWSGATOR_UPSTREAM_VERSION"),
        "build_commit": commit[:12] if commit != "unknown" else commit,
    }
