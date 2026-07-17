from pathlib import Path
import shutil

import yaml

from scripts.check_dataset_cards import validate_dataset_dir


ROOT = Path(__file__).resolve().parents[1]


def copy_valid_card(tmp_path: Path) -> Path:
    target = tmp_path / "example"
    shutil.copytree(ROOT / "survey" / "datasets" / "uos_v1", target)
    return target


def test_valid_template_passes(tmp_path: Path) -> None:
    target = copy_valid_card(tmp_path)
    errors, _warnings = validate_dataset_dir(target)
    assert errors == []


def test_invalid_boolean_state_fails(tmp_path: Path) -> None:
    target = copy_valid_card(tmp_path)
    facts_path = target / "facts.yaml"
    facts = yaml.safe_load(facts_path.read_text(encoding="utf-8"))
    facts["raw_data_available"] = "Maybe"
    facts_path.write_text(yaml.safe_dump(facts, sort_keys=False), encoding="utf-8")
    errors, _warnings = validate_dataset_dir(target)
    assert any("invalid Yes/No state" in error for error in errors)


def test_missing_file_is_detected(tmp_path: Path) -> None:
    target = copy_valid_card(tmp_path)
    (target / "evidence.md").unlink()
    errors, _warnings = validate_dataset_dir(target)
    assert any("evidence.md" in error for error in errors)
