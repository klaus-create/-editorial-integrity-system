#!/usr/bin/env python3
"""Validate a project editorial manifest against the canonical JSON Schema."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys."""


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "editorial-integrity-router"
    / "references"
    / "project-editorial-manifest.schema.yaml"
)


def fail(message: str) -> None:
    print(f"INVALID: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> object:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:
        fail(f"cannot parse YAML in {path}: {exc}")


def format_path(parts: list[object]) -> str:
    if not parts:
        return "<root>"
    return ".".join(str(part) for part in parts)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_manifest.py <manifest.yaml>")

    manifest_path = Path(sys.argv[1]).resolve()
    if not manifest_path.is_file():
        fail(f"file not found: {manifest_path}")
    if not SCHEMA_PATH.is_file():
        fail(f"canonical schema not found: {SCHEMA_PATH}")

    manifest = load_yaml(manifest_path)
    schema = load_yaml(SCHEMA_PATH)

    if not isinstance(manifest, dict):
        fail("manifest root must be a mapping")
    if "project_editorial_manifest" in manifest:
        fail(
            "legacy project_editorial_manifest wrapper detected; migrate to the "
            "canonical manifest_version/project/authorship/defaults/governance structure"
        )
    if not isinstance(schema, dict):
        fail("canonical schema root must be a mapping")

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            print(
                f"INVALID: {format_path(list(error.path))}: {error.message}",
                file=sys.stderr,
            )
        raise SystemExit(1)

    project = manifest.get("project", {})
    print(
        f"VALID: {project.get('name', 'Unnamed project')} "
        f"(manifest {manifest.get('manifest_version')})"
    )


if __name__ == "__main__":
    main()
