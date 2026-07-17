#!/usr/bin/env python3
"""Validate dataset survey directories without changing their contents."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FILES = {
    "dataset_card.md",
    "facts.yaml",
    "evidence.md",
    "sources.yaml",
    "relevance_to_uos_v2.md",
}
REQUIRED_CARD_SECTIONS = (
    "Identity",
    "Purpose and scope",
    "Acquisition setup",
    "Sensors and channels",
    "Operating conditions",
    "Fault conditions and labels",
    "Data organization and access",
    "Validation reported by source",
    "Known limitations and conflicts",
    "Evidence coverage",
)
EVIDENCE_HEADER = (
    "| Evidence ID | Claim | Evidence summary | Source ID | "
    "Page/Section/Table/Figure | Confidence | Status |"
)
ALLOWED_BOOLEAN_STATES = {"Yes", "Partial", "No", "Unknown"}
BOOLEAN_PATHS = {
    "publication.dedicated_dataset_paper",
    "dataset_mode.batch",
    "dataset_mode.run_to_failure",
    "dataset_mode.variable_speed",
    "channels.triaxial",
    "channels.simultaneous_sampling",
    "channels.synchronized_acquisition",
    "faults.healthy",
    "faults.inner_race",
    "faults.outer_race",
    "faults.ball_or_roller",
    "faults.cage",
    "faults.rotor",
    "faults.gear",
    "compound_faults.internal_bearing",
    "compound_faults.bearing_rotor",
    "compound_faults.bearing_gear",
    "compound_faults.other",
    "operating_conditions.bearing_type_shift",
    "fault_generation.artificial",
    "fault_generation.natural",
    "fault_generation.run_to_failure",
    "raw_data_available",
    "processed_data_available",
    "metadata_available",
    "code_available",
}


def nested_get(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def validate_dataset_dir(dataset_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    missing = sorted(REQUIRED_FILES - {p.name for p in dataset_dir.iterdir() if p.is_file()})
    if missing:
        errors.append(f"missing required files: {', '.join(missing)}")

    card = dataset_dir / "dataset_card.md"
    if card.exists():
        text = card.read_text(encoding="utf-8")
        for section in REQUIRED_CARD_SECTIONS:
            if f"## {section}" not in text:
                errors.append(f"dataset_card.md missing section: {section}")

    facts: dict[str, Any] | None = None
    facts_path = dataset_dir / "facts.yaml"
    if facts_path.exists():
        try:
            loaded = yaml.safe_load(facts_path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                errors.append("facts.yaml root must be a mapping")
            else:
                facts = loaded
        except yaml.YAMLError as exc:
            errors.append(f"facts.yaml is invalid YAML: {exc}")
    if facts is not None:
        for path in sorted(BOOLEAN_PATHS):
            value = nested_get(facts, path)
            if value is not None and value not in ALLOWED_BOOLEAN_STATES:
                errors.append(f"invalid Yes/No state at {path}: {value!r}")

    evidence = dataset_dir / "evidence.md"
    if evidence.exists() and EVIDENCE_HEADER not in evidence.read_text(encoding="utf-8"):
        errors.append("evidence.md header is invalid")

    sources_path = dataset_dir / "sources.yaml"
    if sources_path.exists():
        try:
            sources_data = yaml.safe_load(sources_path.read_text(encoding="utf-8")) or {}
            sources = sources_data.get("sources", []) if isinstance(sources_data, dict) else []
            ids = [s.get("source_id") for s in sources if isinstance(s, dict)]
            duplicate_ids = sorted({sid for sid in ids if sid and ids.count(sid) > 1})
            if duplicate_ids:
                errors.append(f"duplicate source_id: {', '.join(duplicate_ids)}")
            if not sources:
                warnings.append("no sources recorded")
        except yaml.YAMLError as exc:
            errors.append(f"sources.yaml is invalid YAML: {exc}")
    return errors, warnings


def validate_repository(root: Path) -> tuple[list[str], list[str]]:
    all_errors: list[str] = []
    all_warnings: list[str] = []
    datasets_dir = root / "survey" / "datasets"
    if not datasets_dir.exists():
        return ["survey/datasets directory is missing"], []
    dataset_dirs = sorted(path for path in datasets_dir.iterdir() if path.is_dir())
    if not dataset_dirs:
        all_errors.append("no dataset directories found")
    for dataset_dir in dataset_dirs:
        errors, warnings = validate_dataset_dir(dataset_dir)
        all_errors.extend(f"{dataset_dir.name}: {message}" for message in errors)
        all_warnings.extend(f"{dataset_dir.name}: {message}" for message in warnings)

    registry = root / "survey" / "dataset_registry.csv"
    if registry.exists():
        with registry.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                verification = row.get("verification_status", "").strip().lower()
                survey = row.get("survey_status", "").strip().lower()
                if survey == "complete" and verification != "complete":
                    all_errors.append(
                        f"{row.get('dataset_id', 'Unknown')}: survey_status complete without verification_status complete"
                    )
    else:
        all_errors.append("survey/dataset_registry.csv is missing")
    return all_errors, all_warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, warnings = validate_repository(args.root)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Validation finished: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
