from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.\
    metric_check_results import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.\
    static_normal_range_metric_check import StaticNormalRangeMetricCheck

TEST_CONFIGURATION = StaticNormalRangeMetricCheck(
    rolling_periods=2,
)


def test_init_manual_four_threshold_metric_check():
    assert TEST_CONFIGURATION, 'Object should initialize.'


def test_run_check():
    assert isinstance(TEST_CONFIGURATION.run(pd.Series([25, 25, 5, 15, 35, 45])), pd.Series), \
        'Run method should finish executing.'
