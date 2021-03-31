from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.compare_to_baseline_metric_check import CompareToBaselineMetricCheck


def test_check_correctness():
    expected = pd.Series([
    MetricCheckResult(
        valence_score=-1, #metric 0
        valence_label='Lower than',
        valence_description='Lower than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=-1, #metric 8.9
        valence_label='Lower than',
        valence_description='Lower than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=0, #metric 9
        valence_label='Within the range of',
        valence_description='Within the range of normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=0, #metric 11
        valence_label='Within the range of',
        valence_description='Within the range of normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=1,  # raw score 11.1
        valence_label='Higher than',
        valence_description='Higher than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=1,  # raw score 9999999
        valence_label='Higher than',
        valence_description='Higher than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    ])

    actual = CompareToBaselineMetricCheck().run(s=pd.Series([0, 8.9, 9, 11, 11.1, 9999999]),
                                                baseline=10,
                                                threshold_pct=0.1,
                                                is_higher_better=True,
                                                is_lower_better=False)

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]


def test_lower_is_better():
    expected = pd.Series([
    MetricCheckResult(
        valence_score=1,  # raw score 0
        valence_label='Higher than',
        valence_description='Higher than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    MetricCheckResult(
        valence_score=-1, #metric 9999999
        valence_label='Lower than',
        valence_description='Lower than normal based on manual thresholds.',
        metric_check_label='Compare to Baseline Metric Check',
    ),
    ])

    actual = CompareToBaselineMetricCheck().run(s=pd.Series([0, 9999999]),
                                                baseline=10,
                                                threshold_pct=0.1,
                                                is_higher_better=False,
                                                is_lower_better=True)

    for i in range(0, len(actual)):
        assert actual[i] == expected[i]
