#!/usr/bin/env python3
"""Build CSV and Markdown comparison tables from facts files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

import yaml

COLUMNS = [
    "dataset_id", "dataset_name", "institution", "year", "comparison_group",
    "dataset_mode", "modalities", "channel_count", "multi_channel", "sensor_positions",
    "multi_position", "sensor_directions", "multi_direction", "sensor_mounting",
    "position_selection_rationale", "position_validation_methods", "simultaneous_sampling",
    "synchronized_acquisition", "sampling_rates_hz", "rpm_conditions",
    "record_duration_seconds", "samples_per_record",
    "bearing_internal_compound", "bearing_rotor_compound", "bearing_gear_compound",
    "multiple_bearing_types", "variable_rpm", "load_variation", "artificial_fault",
    "natural_fault", "run_to_failure", "raw_available", "metadata_available",
    "validation_methods", "file_formats", "official_url", "survey_status",
    "verification_status",
]
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def get(data: dict[str, Any], *path: str) -> Any:
    value: Any = data
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return "Unknown"
        value = value[key]
    return "Unknown" if value is None or value == "" else value


def display(value: Any) -> str:
    if value is None or value == "" or value == []:
        return "Unknown"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) if value else "Unknown"
    if isinstance(value, dict):
        parts = [f"{key}={item}" for key, item in value.items() if item not in (None, "", "Unknown")]
        return "; ".join(parts) if parts else "Unknown"
    return str(value)


def multiplicity(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "Unknown"
    return "Yes" if len(value) > 1 else "No"


def channel_flag(count: Any) -> str:
    if isinstance(count, int):
        return "Yes" if count > 1 else "No"
    if isinstance(count, list) and count:
        parsed: list[int] = []
        for item in count:
            if isinstance(item, int):
                parsed.append(item)
                continue
            match = re.match(r"\s*(\d+)", str(item))
            if not match:
                return "Unknown"
            parsed.append(int(match.group(1)))
        if all(value > 1 for value in parsed):
            return "Yes"
        if all(value == 1 for value in parsed):
            return "No"
    return "Unknown"


def row_from_facts(facts: dict[str, Any], registry: dict[str, str]) -> dict[str, str]:
    channel_count = get(facts, "channels", "count")
    mode = get(facts, "dataset_mode")
    return {
        "dataset_id": display(get(facts, "dataset_id")),
        "dataset_name": display(get(facts, "dataset_name")),
        "institution": display(get(facts, "institution")),
        "year": display(get(facts, "release_year")),
        "comparison_group": registry.get("comparison_group") or "Unknown",
        "dataset_mode": display(mode),
        "modalities": display(get(facts, "modalities")),
        "channel_count": display(channel_count),
        "multi_channel": channel_flag(channel_count),
        "sensor_positions": display(get(facts, "channels", "positions")),
        "multi_position": multiplicity(get(facts, "channels", "positions")),
        "sensor_directions": display(get(facts, "channels", "directions")),
        "multi_direction": multiplicity(get(facts, "channels", "directions")),
        "sensor_mounting": display(get(facts, "acquisition", "sensor_mounting")),
        "position_selection_rationale": display(get(facts, "acquisition", "position_selection_rationale")),
        "position_validation_methods": display(get(facts, "acquisition", "position_validation_methods")),
        "simultaneous_sampling": display(get(facts, "channels", "simultaneous_sampling")),
        "synchronized_acquisition": display(get(facts, "channels", "synchronized_acquisition")),
        "sampling_rates_hz": display(get(facts, "sampling_rates_hz")),
        "rpm_conditions": display(get(facts, "operating_conditions", "rpm")),
        "record_duration_seconds": display(get(facts, "acquisition", "record_duration_seconds")),
        "samples_per_record": display(get(facts, "acquisition", "samples_per_record")),
        "bearing_internal_compound": display(get(facts, "compound_faults", "internal_bearing")),
        "bearing_rotor_compound": display(get(facts, "compound_faults", "bearing_rotor")),
        "bearing_gear_compound": display(get(facts, "compound_faults", "bearing_gear")),
        "multiple_bearing_types": multiplicity(get(facts, "bearing_types")),
        "variable_rpm": display(get(facts, "dataset_mode", "variable_speed")),
        "load_variation": multiplicity(get(facts, "operating_conditions", "load")),
        "artificial_fault": display(get(facts, "fault_generation", "artificial")),
        "natural_fault": display(get(facts, "fault_generation", "natural")),
        "run_to_failure": display(get(facts, "dataset_mode", "run_to_failure")),
        "raw_available": display(get(facts, "raw_data_available")),
        "metadata_available": display(get(facts, "metadata_available")),
        "validation_methods": display(get(facts, "validation_methods")),
        "file_formats": display(get(facts, "file_formats")),
        "official_url": display(get(facts, "official_url")),
        "survey_status": registry.get("survey_status") or "Unknown",
        "verification_status": registry.get("verification_status") or "Unknown",
    }


def build(root: Path) -> list[dict[str, str]]:
    registry_path = root / "survey" / "dataset_registry.csv"
    with registry_path.open(encoding="utf-8", newline="") as handle:
        registry_rows = list(csv.DictReader(handle))
    ordered = sorted(
        enumerate(registry_rows),
        key=lambda item: (PRIORITY_ORDER.get(item[1].get("priority", ""), 99), item[0]),
    )
    rows: list[dict[str, str]] = []
    for _, registry in ordered:
        facts_path = root / "survey" / "datasets" / registry["dataset_id"] / "facts.yaml"
        if facts_path.exists():
            facts = yaml.safe_load(facts_path.read_text(encoding="utf-8")) or {}
        else:
            facts = {"dataset_id": registry["dataset_id"], "dataset_name": registry["dataset_name"]}
        rows.append(row_from_facts(facts, registry))
    return rows


def write_tables(root: Path, rows: list[dict[str, str]]) -> None:
    output_dir = root / "survey" / "synthesis"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "comparison_master.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    md_path = output_dir / "comparison_master.md"
    lines = ["# Dataset Comparison", "", "| " + " | ".join(COLUMNS) + " |",
             "|" + "|".join("---" for _ in COLUMNS) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(row[column].replace("|", "\\|") for column in COLUMNS) + " |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    rows = build(args.root)
    write_tables(args.root, rows)
    print(f"Generated comparison tables with {len(rows)} dataset row(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
