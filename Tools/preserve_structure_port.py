#!/usr/bin/env python3
"""Create a portable, structure-preserving export of this Unity project.

The script copies the Unity project as-is (Assets/Packages/ProjectSettings) and
emits a manifest with SHA256 hashes so the destination can verify integrity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

INCLUDE_ROOTS = ("Assets", "Packages", "ProjectSettings")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_under_roots(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root)
    return rel.parts and rel.parts[0] in INCLUDE_ROOTS


def build_manifest(repo_root: Path) -> list[dict[str, str | int]]:
    entries: list[dict[str, str | int]] = []

    for file_path in sorted(repo_root.rglob("*")):
        if not file_path.is_file():
            continue
        if not is_under_roots(file_path, repo_root):
            continue

        rel = file_path.relative_to(repo_root).as_posix()
        entries.append(
            {
                "path": rel,
                "size": file_path.stat().st_size,
                "sha256": sha256_file(file_path),
            }
        )

    return entries


def copy_project(repo_root: Path, output_root: Path) -> None:
    for top in INCLUDE_ROOTS:
        src = repo_root / top
        dst = output_root / top
        if not src.exists():
            continue
        shutil.copytree(src, dst, dirs_exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export Unity project while preserving file structure and assets."
    )
    parser.add_argument(
        "output",
        help="Directory where the exported project copy and manifest will be written.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Unity project root (default: current directory).",
    )

    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    output_root = Path(args.output).resolve()

    output_root.mkdir(parents=True, exist_ok=True)
    copy_project(repo_root, output_root)

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceRoot": str(repo_root),
        "includeRoots": list(INCLUDE_ROOTS),
        "files": build_manifest(repo_root),
    }

    manifest_path = output_root / "port-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Export completed: {output_root}")
    print(f"Manifest: {manifest_path}")
    print(f"Tracked files: {len(manifest['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
