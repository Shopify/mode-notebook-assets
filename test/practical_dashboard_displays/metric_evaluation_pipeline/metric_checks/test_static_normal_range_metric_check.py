from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.\
    metric_check_results import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.\
    static_normal_range_metric_check import StaticNormalRangeMetricCheck

TEST_CONFIGURATION = StaticNormalRangeMetricCheck(
    rolling_periods=4,
)


def test_init_manual_four_threshold_metric_check():
    assert TEST_CONFIGURATION, 'Object should initialize.'


def test_run_check():
    assert isinstance(TEST_CONFIGURATION.run(pd.Series([25, 25, 5, 15, 35, 45])), pd.Series), \
        'Run method should finish executing.'

    _output = StaticNormalRangeMetricCheck(
        rolling_periods=4,
        maximum_learning_differences_quantile=.8,
    ).run(pd.Series([250, 190, 230, 210, 220, 220, 190, 225, 220, 225, 300, 240, 100, 500, 0]))