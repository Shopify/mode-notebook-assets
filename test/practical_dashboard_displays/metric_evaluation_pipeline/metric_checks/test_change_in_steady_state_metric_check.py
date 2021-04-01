from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.change_in_steady_state_metric_check import \
    ChangeInSteadyStateMetricCheck

TEST_CONFIGURATION = ChangeInSteadyStateMetricCheck(
    l1_threshold=7,
    l2_threshold=9,
)

TEST_CONFIGURATION_INVERSE = ChangeInSteadyStateMetricCheck(
    is_higher_better=False,
    is_lower_better=True,
    l1_threshold=7,
    l2_threshold=9,
)

TEST_CONFIGURATION_EXPANDING = ChangeInSteadyStateMetricCheck(
    l1_threshold=7,
    l2_threshold=9,
    is_rolling_window=False
)

TEST_CONFIGURATION_MIN_PERIODS = ChangeInSteadyStateMetricCheck(
    l1_threshold=7,
    l2_threshold=9,
    _min_periods=3
)

def test_init_manual_four_threshold_metric_check():
    assert TEST_CONFIGURATION, 'Object should initialize.'


def test_invalid_configuration():
    # Initialization should fail if the l1 threshold is greater
    # than the l2 threshold
    with pytest.raises(AssertionError):
        assert ChangeInSteadyStateMetricCheck(
            l1_threshold=9,
            l2_threshold=7
        )


def test_run_check():
    assert isinstance(TEST_CONFIGURATION.run(pd.Series([3,5,6,7,1,3,4,5,6,7,4,7,6,2,8,8,9,10,15,20,20,30,28,29,25,21,16,13,12,10,9,13,8,10,10,11,10,9,7,8,9])), pd.Series), \
        'Run method should finish executing.'


def test_check_correctness():

    test_series = pd.Series([3,5,6,7,1,3,4,5,6,7,4,70,80,100,80,81,91,100,105,120,130])
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.01,
            valence_label='Better than Normal',
            valence_description='Rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.51,
            valence_label='Better than Normal',
            valence_description='Rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=1.0,
            valence_label='Unusually Good',
            valence_description='Significant rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=1.0,
            valence_label='Unusually Good',
            valence_description='Significant rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
    ])
    actual = TEST_CONFIGURATION.run(test_series)

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

def test_check_correctness_inverse():

    test_series = pd.Series([3,5,6,7,1,3,4,5,6,7,4,70,80,100,80,81,91,100,105,120,130])
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-0.01,
            valence_label='Worse than Normal',
            valence_description='Rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-0.51,
            valence_label='Worse than Normal',
            valence_description='Rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-1.0,
            valence_label='Unusually Bad',
            valence_description='Significant rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-1.0,
            valence_label='Unusually Bad',
            valence_description='Significant rise in steady state above historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
    ])
    actual = TEST_CONFIGURATION_INVERSE.run(test_series)

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

def test_check_correctness_expanding():

    test_series = pd.Series([4,5,6,5,4,5,6,-1,-2,-1,-3,-2,-4,-10,-30])
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-0.01,
            valence_label='Worse than Normal',
            valence_description='Drop in steady state below historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
        MetricCheckResult(
            valence_score=-0.51,
            valence_label='Worse than Normal',
            valence_description='Drop in steady state below historical mean.',
            metric_check_label='Change in Steady State Check',
        ),
    ])
    actual = TEST_CONFIGURATION_EXPANDING.run(test_series)

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

def test_check_correctness_min_periods():

    test_series = pd.Series([4,5,6,5,4,5,6,-1,-2,-1,-3,-2,-4,-10,-30])
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=0.0,
            valence_label='In a Normal Range',
            valence_description='No significant change from historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=-0.01,
            valence_label='Worse than Normal',
            valence_description='Drop in steady state below historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
        MetricCheckResult(
            valence_score=-0.51,
            valence_label='Worse than Normal',
            valence_description='Drop in steady state below historical mean.',
            metric_check_label='Change in Steady State Check'
        ),
    ])
    actual = TEST_CONFIGURATION_MIN_PERIODS.run(test_series)

    print([a.__dict__ for a in actual], file=open("test_output.txt", "a"))

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]
