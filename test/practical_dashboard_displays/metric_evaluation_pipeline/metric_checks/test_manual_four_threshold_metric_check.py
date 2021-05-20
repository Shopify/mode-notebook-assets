from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScore, ValenceScoreSeries
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.manual_four_threshold_metric_check import \
    ManualFourThresholdMetricCheck

TEST_CONFIGURATION = ManualFourThresholdMetricCheck(
    threshold_1=10,
    threshold_2=20,
    threshold_3=30,
    threshold_4=40,
)


def test_init_manual_four_threshold_metric_check():
    assert TEST_CONFIGURATION, 'Object should initialize.'


def test_invalid_configuration():
    # Initialization should fail if the thresholds
    # aren't in sorted order.
    with pytest.raises(AssertionError):
        for _theshold_permutations in permutations([10, 20, 30, 40], r=4):
            if _theshold_permutations != sorted(_theshold_permutations):
                assert ManualFourThresholdMetricCheck(
                    threshold_1=_theshold_permutations[0],
                    threshold_2=_theshold_permutations[1],
                    threshold_3=_theshold_permutations[2],
                    threshold_4=_theshold_permutations[3],
                )


def test_run_check():
    assert isinstance(TEST_CONFIGURATION.apply(pd.Series([25, 25, 5, 15, 35, 45])), ValenceScoreSeries), \
        'Run method should finish executing.'


def test_check_correctness():
    expected = ValenceScoreSeries(
        pd.Series([
            ValenceScore(
                valence_score=0,
                valence_label='In a Normal Range',
                valence_description='Within the range of normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=0,
                valence_label='In a Normal Range',
                valence_description='Within the range of normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=-1,
                valence_label='Unusually Bad',
                valence_description='Significantly lower than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=-0.51,
                valence_label='Worse than Normal',
                valence_description='Lower than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=0.51,
                valence_label='Better than Normal',
                valence_description='Higher than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=1,
                valence_label='Unusually Good',
                valence_description='Significantly higher than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
        ])
    )
    actual = TEST_CONFIGURATION.apply(pd.Series([25, 25, 5, 15, 35, 45]))

    for i in range(0, len(actual._score_series)):
        assert actual._score_series[i] == expected._score_series[i]


def test_reconfigured_directionality():
    expected = ValenceScoreSeries(
        pd.Series([
            ValenceScore(
                valence_score=0,
                valence_label='In a Normal Range',
                valence_description='Within the range of normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=0,
                valence_label='In a Normal Range',
                valence_description='Within the range of normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=1,
                valence_label='Unusually Good',
                valence_description='Significantly lower than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=0.51,
                valence_label='Better than Normal',
                valence_description='Lower than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=-0.51,
                valence_label='Worse than Normal',
                valence_description='Higher than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
            ValenceScore(
                valence_score=-1,
                valence_label='Unusually Bad',
                valence_description='Significantly higher than normal based on manual thresholds.',
                metric_check_label='Manual Four Threshold Check',
            ),
        ])
    )
    actual = ManualFourThresholdMetricCheck(
        threshold_1=10,
        threshold_2=20,
        threshold_3=30,
        threshold_4=40,
        is_higher_better=False,
        is_lower_better=True,
    ).apply(pd.Series([25, 25, 5, 15, 35, 45]))

    for i in range(0, len(actual._score_series)):
        assert actual._score_series[i] == expected._score_series[i]
