import pytest
import pandas as pd
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries, ValenceScore

LIST_ONE = [1, 2, 3, 4, 5]
LIST_TWO = [6, 7, 8, 9, 10]
TEST_SERIES = pd.Series(data=LIST_ONE, index=LIST_ONE)

TEST_VALENCE_SCORE = ValenceScore(
    valence_score=0,
    valence_label='Normal',
    valence_description='Normal'
)

TEST_VALENCE_SCORE_SERIES = ValenceScoreSeries(
    s=pd.Series(
        data=[
            TEST_VALENCE_SCORE,
            TEST_VALENCE_SCORE,
            TEST_VALENCE_SCORE,
            TEST_VALENCE_SCORE,
            TEST_VALENCE_SCORE,
        ],
        index=LIST_ONE
    )
)


def test_metric_evaluation_result_initialize():
    assert MetricEvaluationResult(
        data=TEST_SERIES,
        valence_score_series=TEST_VALENCE_SCORE_SERIES,
    )


def test_metric_evaluation_result_to_dataframe():
    assert isinstance(
        MetricEvaluationResult(
            data=TEST_SERIES,
            valence_score_series=TEST_VALENCE_SCORE_SERIES,
        ).to_dataframe(),
        pd.DataFrame
    )


def test_metric_evaluation_result_to_dataframe_schema():
    actual_keys = MetricEvaluationResult(
        data=TEST_SERIES,
        valence_score_series=TEST_VALENCE_SCORE_SERIES,
    ).to_dataframe().columns

    expected_keys = [
        'Period Value',
        'Valence Score',
        'ValenceScore Object',
        'Valence Label',
        'Valence Description',
        'Priority Score',
        'Is Override?',
        'Is Ambiguous?',
        'Metric Check Label',
    ]

    assert sorted(actual_keys) == sorted(expected_keys)


def test_metric_evaluation_result_validate_index():
    with pytest.raises(AssertionError):
        MetricEvaluationResult(
            data=pd.Series(
                data=LIST_ONE,
                index=LIST_TWO,
            ),
            valence_score_series=TEST_VALENCE_SCORE_SERIES,
        )
