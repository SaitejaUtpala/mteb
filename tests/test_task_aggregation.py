from __future__ import annotations

import mteb
import mteb.task_aggregation as task_aggregation

# define some test data
bitext1_1 = mteb.MTEBResults(
    dataset_revision="test_rev",
    task_name="BornholmBitextMining",
    mteb_version="test_version",
    evaluation_time=1,
    scores={"test": [{"main_score": 1, "hf_subset": "NaN", "languages": ["eng-Latn"]}]},
)

bitext1_2 = mteb.MTEBResults(
    dataset_revision="test_rev",
    task_name="BornholmBitextMining",
    mteb_version="test_version",
    evaluation_time=1,
    scores={"test": [{"main_score": 2, "hf_subset": "NaN", "languages": ["eng-Latn"]}]},
)

classification1_1 = mteb.MTEBResults(
    dataset_revision="test_rev",
    task_name="Banking77Classification",
    mteb_version="test_version",
    evaluation_time=1,
    scores={"test": [{"main_score": 1, "hf_subset": "NaN", "languages": ["eng-Latn"]}]},
)

classification1_2 = mteb.MTEBResults(
    dataset_revision="test_rev",
    task_name="Banking77Classification",
    mteb_version="test_version",
    evaluation_time=1,
    scores={"test": [{"main_score": 2, "hf_subset": "NaN", "languages": ["eng-Latn"]}]},
)

classification2_1 = mteb.MTEBResults(
    dataset_revision="test_rev",
    task_name="AfriSentiClassification",
    mteb_version="test_version",
    evaluation_time=1,
    scores={"test": [{"main_score": 1, "hf_subset": "NaN", "languages": ["eng-Latn"]}]},
)

mteb_results = {
    "model1": {
        "rev1": [bitext1_1, classification1_2, classification2_1],
        "rev2": [bitext1_1, classification1_1, classification2_1],
    },
    "model2": {
        "rev1": [bitext1_2, classification1_2, classification2_1],
        "rev2": [bitext1_2, classification1_1, classification2_1],
    },
}


def test_mean():
    expected = {
        "model1": {
            "rev1": 4 / 3,  # (1 + 2 + 1) / 3
            "rev2": 1,  # (1 + 1 + 1) / 3
        },
        "model2": {
            "rev1": 5 / 3,  # (2 + 2 + 1) / 3
            "rev2": 4 / 3,  # (2 + 1 + 1) / 3
        },
    }

    assert task_aggregation.mean(mteb_results) == expected


def test_task_category_weighted_mean():
    expected = {
        "model1": {
            "rev1": 1.25,  # ( 1/1 + (2 + 1) / 2 ) / 2
            "rev2": 1,  # ( 1/1 + (1 + 1) / 2 ) / 2
        },
        "model2": {
            "rev1": 1.75,  # ( 2/1 + (2 + 1) / 2 ) / 2
            "rev2": 1.5,  # ( 2/1 + (1 + 1) / 2 ) / 2
        },
    }

    assert task_aggregation.task_category_weighted_mean(mteb_results) == expected


def test_borda_count_simple():
    mteb_results_simple = {
        "model1": {
            "rev1": [bitext1_1],
        },
        "model2": {
            "rev2": [bitext1_2],
        },
    }
    expected = {
        "model1": {
            "rev1": 0,
        },
        "model2": {
            "rev2": 1,
        },
    }
    assert task_aggregation.borda_count(mteb_results_simple) == expected


def test_borda_count_simple_with_tie():
    mteb_results_simple_with_tie = {
        "model1": {
            "rev1": [bitext1_1],
            "rev2": [bitext1_1],
        },
        "model2": {
            "rev1": [bitext1_2],
            "rev2": [bitext1_2],
        },
    }
    expected = {
        "model1": {
            "rev1": 0.5,
            "rev2": 0.5,
        },
        "model2": {
            "rev1": 2.5,
            "rev2": 2.5,
        },
    }
    assert task_aggregation.borda_count(mteb_results_simple_with_tie) == expected


def test_borda_count_multiple_task_and_ties():
    # task 1: model1/rev1 == model2/rev1 > model1/rev2 == model2/rev2
    # task 2: model1/rev1 == model2/rev1 > model1/rev2 == model2/rev2
    # task 3: model1/rev1 == model2/rev1 == model1/rev2 == model2/rev2
    # given there is 4 candidates the max score is 3 (4 - 1)
    # we use tournament borda count so shared ranks get the average of the ranks they would have gotten

    expected = {
        "model1": {
            "rev1": 0.5 + 2.5 + (6 / 4),
            "rev2": 0.5 + 0.5 + (6 / 4),
        },
        "model2": {
            "rev1": 2.5 + 2.5 + (6 / 4),
            "rev2": 2.5 + 0.5 + (6 / 4),
        },
    }

    assert task_aggregation.borda_count(mteb_results) == expected