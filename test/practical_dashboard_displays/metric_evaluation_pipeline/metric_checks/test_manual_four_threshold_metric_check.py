from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
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
    assert isinstance(TEST_CONFIGURATION.run(pd.Series([25, 25, 5, 15, 35, 45])), pd.Series), \
        'Run method should finish executing.'


def test_check_correctness():
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Within the range of normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Within the range of normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
        MetricCheckResult(
            valence_score=-1,
            valence_label='Unusually Bad',
            valence_description='Significantly lower than normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
        MetricCheckResult(
            valence_score=-0.51,
            valence_label='Worse than Normal',
            valence_description='Lower than normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
        MetricCheckResult(
            valence_score=0.51,
            valence_label='Better than Normal',
            valence_description='Higher than normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
        MetricCheckResult(
            valence_score=1,
            valence_label='Unusually Good',
            valence_description='Significantly higher than normal based on manual thresholds.',
            metric_check_label='Manual Four Threshold Check',
        ),
    ])
    actual = TEST_CONFIGURATION.run(pd.Series([25, 25, 5, 15, 35, 45]))

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]
