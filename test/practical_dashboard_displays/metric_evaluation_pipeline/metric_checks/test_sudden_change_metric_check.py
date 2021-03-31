from itertools import permutations

import pytest
import pandas as pd
import numpy as np

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.sudden_change_metric_check import \
    SuddenChangeMetricCheck

TEST_CONFIGURATION = SuddenChangeMetricCheck(
    minimum_periods=2,
    rolling_periods=4
)

TEST_CONFIGURATION_INV = SuddenChangeMetricCheck(
    is_higher_better=False,
    is_lower_better=True,
    minimum_periods=2,
    rolling_periods=4
)


def test_init_sudden_change_metric_check():
    assert TEST_CONFIGURATION, 'Object should initialize.'

def test_run_check():
    test_series = np.ones(13)
    test_series[12] = 10
    assert isinstance(TEST_CONFIGURATION.run(pd.Series(test_series)), pd.Series), \
        'Run method should finish executing.'


def test_check_correctness():
    test_series = np.ones(13)
    test_series[12] = 10
    test_series[4] = -5
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=-1,
            valence_label='Unusually Bad',
            valence_description='Sudden significant drop in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=1,
            valence_label='Unusually Good',
            valence_description='Sudden significant spike in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
    ])
    actual = TEST_CONFIGURATION.run(pd.Series(test_series))

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

def test_check_correctness_soft():
    test_series = np.ones(13)
    test_series[12] = 5
    test_series[4] = -3
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=-0.4464831804281345,
            valence_label='Worse than Normal',
            valence_description='Sudden drop in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0.4464831804281345,
            valence_label='Better than Normal',
            valence_description='Sudden spike in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
    ])
    actual = TEST_CONFIGURATION.run(pd.Series(test_series))

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

def test_check_correctness_inverse():
    test_series = np.ones(13)
    test_series[12] = 5
    test_series[4] = -3
    expected = pd.Series([
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Not enough data to calculate if change in prior period is significant.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0.4464831804281345,
            valence_label='Better than Normal',
            valence_description='Sudden drop in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='No significant change from prior period.',
            metric_check_label='Sudden Change Check',
        ),
        MetricCheckResult(
            valence_score=-0.4464831804281345,
            valence_label='Worse than Normal',
            valence_description='Sudden spike in value over prior period.',
            metric_check_label='Sudden Change Check',
        ),
    ])
    actual = TEST_CONFIGURATION_INV.run(pd.Series(test_series))

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

