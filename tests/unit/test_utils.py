from app.utils.utils import (
    _get_categorical_features,
    _normalize_score,
    _score_accompanying_complexity_with_pca,
)
from tests.fixtures.data import *

import numpy as np


def test_get_categorical_features():
    input_df = pd.DataFrame(
        [
            {
                "studentid": 357,
                "school": "MS",
                "sex": "F",
                "age": 17,
                "address": "U",
                "famsize": "LE3",
                "pstatus": "A",
                "medu": 3,
                "fedu": 2,
            }
        ]
    )
    actual_categorical_features_list = _get_categorical_features(input_df)
    expected_categorical_features_list = [
        "school",
        "sex",
        "address",
        "famsize",
        "pstatus",
    ]
    assert actual_categorical_features_list == expected_categorical_features_list


def test_normalize_score():
    input_array = np.array([0, 1, 2, 3, 4, 5])
    actual_array = _normalize_score(input_array)
    expected_array = np.array([0, 20, 40, 60, 80, 100])
    np.testing.assert_array_equal(actual_array, expected_array)


def test_score_accompanying_complexity_with_pca():
    input_df = pd.DataFrame(
        [
            {"studytime": 2, "walc": 2, "absences": 2},
            {
                "studytime": 1,
                "walc": 4,
                "absences": 10,
            },
            {
                "studytime": 2,
                "walc": 1,
                "absences": 0,
            },
        ]
    )
    actual_scores_array = _score_accompanying_complexity_with_pca(input_df)
    expected_scores_array = np.array([18, 100, 0])
    np.testing.assert_array_equal(expected_scores_array, actual_scores_array)
