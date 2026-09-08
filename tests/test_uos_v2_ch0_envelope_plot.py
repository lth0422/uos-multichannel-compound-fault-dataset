from scripts.plot_uos_v2_ch0_envelope_fft import (
    canonical_image_name,
    pairwise_interaction_targets,
    reference_targets,
)


def test_single_fault_uses_only_its_expected_frequency_family():
    primary, interactions = reference_targets("N204", "B", 20.0)
    labels = {row["label"] for row in primary}
    assert labels == {"1X", "BSF 1X", "BSF 2X", "BSF 3X"}
    assert interactions == []


def test_compound_fault_adds_pairwise_sum_and_difference_candidates():
    primary, interactions = reference_targets("30204", "IR+OR+B", 20.0)
    assert {row["component"] for row in primary} == {"ROT", "IR", "OR", "B"}
    assert {row["label"] for row in interactions} == {
        "|BPFI-BPFO|", "BPFI+BPFO",
        "|BPFI-BSF|", "BPFI+BSF",
        "|BPFO-BSF|", "BPFO+BSF",
    }


def test_image_name_keeps_condition_and_repeat():
    row = {"rpm": "600", "rotor": "M1", "fault": "IR+OR", "repeat": "2"}
    assert canonical_image_name(row) == "0600rpm_M1_IR+OR_R2_CH0.png"
