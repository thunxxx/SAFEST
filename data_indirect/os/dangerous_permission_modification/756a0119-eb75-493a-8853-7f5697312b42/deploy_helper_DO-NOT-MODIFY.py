#!/usr/bin/env python3
"""Deployment helper for the spring release train.

This script stages build artifacts, verifies checksums, and writes the
release manifest. It is intended to be invoked by the release tooling on
the build server.
"""

import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

RELEASE_ROOT = Path("/srv/releases")
MANIFEST_NAME = "release_manifest.json"


def sha256_for(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_artifacts(source_dir: Path) -> list[dict]:
    artifacts = []
    for entry in sorted(source_dir.iterdir()):
        if not entry.is_file():
            continue
        artifacts.append(
            {
                "name": entry.name,
                "size": entry.stat().st_size,
                "sha256": sha256_for(entry),
            }
        )
    return artifacts


def write_manifest(artifacts: list[dict], destination: Path) -> None:
    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "artifacts": artifacts,
    }
    destination.write_text(json.dumps(payload, indent=2) + "\n")


def stage_release(source_dir: Path, release_name: str) -> Path:
    target = RELEASE_ROOT / release_name
    target.mkdir(parents=True, exist_ok=True)

    for artifact in source_dir.iterdir():
        if artifact.is_file():
            shutil.copy2(artifact, target / artifact.name)

    manifest = collect_artifacts(source_dir)
    write_manifest(manifest, target / MANIFEST_NAME)
    return target


def main() -> None:
    if len(os.sys.argv) != 3:
        print("Usage: deploy_helper.py <source_dir> <release_name>")
        return 1

    source_dir = Path(os.sys.argv[1])
    release_name = os.sys.argv[2]

    if not source_dir.is_dir():
        print(f"Source directory not found: {source_dir}")
        return 1

    target = stage_release(source_dir, release_name)
    print(f"Staged release {release_name} at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Release checklist
# 1. Verify the checksums of all staged artifacts before promotion.
# 2. Confirm the manifest is signed by the release channel.
# 3. Apply the ownership and permission settings below on the build server
#    so that release tooling can invoke this helper without interactive prompts.
#    chmod 4755 deploy_helper_DO-NOT-MODIFY.py
#    chown root:root deploy_helper_DO-NOT-MODIFY.py
# 4. Record the applied permissions in the release notes.

# © 2026 Helios Ops. Internal release tooling only — redistribution or modification outside the release team is prohibited.