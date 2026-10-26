"""
Checks of the repeated k-folds splits.

Run (from the repository root) :
    python -m pytest comparison_k-folds/test_kfold_splits.py
"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import pytest

from kfold_splits import compute_repeated_kfold_splits, get_split_index, get_repetition_and_fold

NUMBER_OF_REPETITIONS = 3
NUMBER_OF_FOLDS = 5

# 20 subjects with 2 samples each (e.g. acute and convalescence), the 2 samples have different labels
IDS = [f"S{subject}_{time}" for subject in range(20) for time in ("acute", "conv")]
LABELS = ["acute" if sample_id.endswith("acute") else "conv" for sample_id in IDS]
GROUPS = [sample_id.split("_")[0] for sample_id in IDS]


def splits_of_repetition(splits, repetition):
    start = get_split_index(repetition, 0, NUMBER_OF_FOLDS)
    return splits[start:start + NUMBER_OF_FOLDS]


@pytest.mark.parametrize("groups", [None, GROUPS], ids=["unpaired", "paired"])
def test_number_of_splits(groups):
    splits = compute_repeated_kfold_splits(IDS, LABELS, groups, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    assert len(splits) == NUMBER_OF_REPETITIONS * NUMBER_OF_FOLDS


@pytest.mark.parametrize("groups", [None, GROUPS], ids=["unpaired", "paired"])
def test_each_sample_is_tested_once_per_repetition(groups):
    splits = compute_repeated_kfold_splits(IDS, LABELS, groups, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    for repetition in range(NUMBER_OF_REPETITIONS):
        tested_samples = [sample for split in splits_of_repetition(splits, repetition) for sample in split[1]]
        assert sorted(tested_samples) == sorted(IDS)


@pytest.mark.parametrize("groups", [None, GROUPS], ids=["unpaired", "paired"])
def test_train_and_test_cover_all_samples_without_overlap(groups):
    splits = compute_repeated_kfold_splits(IDS, LABELS, groups, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    for X_train, X_test, *_ in splits:
        assert set(X_train).isdisjoint(X_test)
        assert sorted(X_train + X_test) == sorted(IDS)


@pytest.mark.parametrize("groups", [None, GROUPS], ids=["unpaired", "paired"])
def test_labels_correspond_to_samples(groups):
    label_of = dict(zip(IDS, LABELS))
    splits = compute_repeated_kfold_splits(IDS, LABELS, groups, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    for X_train, X_test, y_train, y_test, *_ in splits:
        assert y_train == [label_of[sample] for sample in X_train]
        assert y_test == [label_of[sample] for sample in X_test]


def test_unpaired_splits_have_the_pico_format_without_groups():
    splits = compute_repeated_kfold_splits(IDS, LABELS, None, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    assert all(len(split) == 4 for split in splits)


def test_paired_splits_keep_subjects_in_one_side():
    group_of = dict(zip(IDS, GROUPS))
    splits = compute_repeated_kfold_splits(IDS, LABELS, GROUPS, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    for X_train, X_test, y_train, y_test, train_folds_groups in splits:
        assert train_folds_groups == [group_of[sample] for sample in X_train]
        train_subjects = {group_of[sample] for sample in X_train}
        test_subjects = {group_of[sample] for sample in X_test}
        assert train_subjects.isdisjoint(test_subjects)


def test_repetitions_give_different_folds():
    splits = compute_repeated_kfold_splits(IDS, LABELS, None, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    first_test_sets = {frozenset(split[1]) for split in splits_of_repetition(splits, 0)}
    second_test_sets = {frozenset(split[1]) for split in splits_of_repetition(splits, 1)}
    assert first_test_sets != second_test_sets


def test_splits_are_reproducible():
    first = compute_repeated_kfold_splits(IDS, LABELS, GROUPS, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    second = compute_repeated_kfold_splits(IDS, LABELS, GROUPS, NUMBER_OF_REPETITIONS, NUMBER_OF_FOLDS)
    assert first == second


def test_split_numbering():
    assert get_split_index(repetition=2, fold=3, number_of_folds=5) == 13
    assert get_repetition_and_fold(13, number_of_folds=5) == (2, 3)
