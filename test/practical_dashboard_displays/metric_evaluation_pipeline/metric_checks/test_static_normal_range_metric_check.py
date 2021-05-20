from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.\
    static_normal_range_metric_check import StaticNormalRangeMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries

TEST_CONFIGURATION = StaticNormalRangeMetricCheck(
    rolling_periods=4,
)


def test_static_normal_range_metric_check_initializes():
    assert TEST_CONFIGURATION, 'Object should initialize.'


def test_static_normal_range_metric_check_apply_finishes():
    assert isinstance(TEST_CONFIGURATION.apply(pd.Series([25, 25, 5, 15, 35, 45])), ValenceScoreSeries), \
        'Apply method should finish executing.'


def test_static_normal_range_metric_check_example():
    _output = StaticNormalRangeMetricCheck(
        rolling_periods=8,
        maximum_learning_differences_quantile=.8,
    ).apply(pd.Series([250, 190, 230, 210, 220, 220, 190, 225, 220, 225, 300, 240, 100, 500, 0]))

    assert [v.valence_score for v in _output._score_series] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, -1, 1, -1]
