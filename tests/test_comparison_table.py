import csv
from pathlib import Path

from scripts.build_comparison_table import COLUMNS, build, channel_flag, write_tables


def make_repo(tmp_path: Path) -> Path:
    survey = tmp_path / "survey"
    (survey / "datasets" / "alpha").mkdir(parents=True)
    (survey / "datasets" / "beta").mkdir(parents=True)
    (survey / "synthesis").mkdir()
    (survey / "dataset_registry.csv").write_text(
        "dataset_id,dataset_name,institution,approx_year,priority,comparison_group,"
        "dedicated_dataset_paper,local_sources_ready,survey_status,verification_status,notes\n"
        "alpha,Alpha,Unknown,Unknown,P1,direct,Unknown,No,not_started,unverified,Unknown\n"
        "beta,Beta,Unknown,Unknown,P0,canonical,Unknown,No,not_started,unverified,Unknown\n",
        encoding="utf-8",
    )
    (survey / "datasets" / "alpha" / "facts.yaml").write_text(
        "dataset_id: alpha\ndataset_name: Alpha\n"
        "channels:\n  count: Unknown\n  positions: [housing top]\n"
        "acquisition:\n  sensor_mounting: [stud]\n  record_duration_seconds: [10]\n"
        "sampling_rates_hz: [12000]\noperating_conditions:\n  rpm: [900]\n",
        encoding="utf-8",
    )
    (survey / "datasets" / "beta" / "facts.yaml").write_text(
        "dataset_id: beta\ndataset_name: Beta\n",
        encoding="utf-8",
    )
    return tmp_path


def test_comparison_column_order(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write_tables(root, build(root))
    with (root / "survey" / "synthesis" / "comparison_master.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        assert next(csv.reader(handle)) == COLUMNS


def test_unknown_fallback(tmp_path: Path) -> None:
    rows = build(make_repo(tmp_path))
    alpha = next(row for row in rows if row["dataset_id"] == "alpha")
    assert alpha["institution"] == "Unknown"
    assert alpha["multi_channel"] == "Unknown"
    assert alpha["modalities"] == "Unknown"


def test_acquisition_design_columns(tmp_path: Path) -> None:
    rows = build(make_repo(tmp_path))
    alpha = next(row for row in rows if row["dataset_id"] == "alpha")
    assert alpha["sensor_positions"] == "housing top"
    assert alpha["sensor_mounting"] == "stud"
    assert alpha["sampling_rates_hz"] == "12000"
    assert alpha["rpm_conditions"] == "900"
    assert alpha["record_duration_seconds"] == "10"
    assert alpha["position_selection_rationale"] == "Unknown"


def test_registry_priority_and_relative_order(tmp_path: Path) -> None:
    rows = build(make_repo(tmp_path))
    assert [row["dataset_id"] for row in rows] == ["beta", "alpha"]


def test_multi_channel_for_set_specific_counts() -> None:
    assert channel_flag(["8 in Set 1", "4 in Sets 2 and 3"]) == "Yes"
    assert channel_flag(["1 in Set 1", "4 in Set 2"]) == "Unknown"
