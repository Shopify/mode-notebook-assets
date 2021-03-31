from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.manual_four_threshold_metric_check import \
    ManualFourThresholdMetricCheck

def test_annotations():
    expected = pd.Series([
        MetricCheckResult(
            valence_score=1,
            valence_label='In a Normal Range',
            valence_description='Very low due to X',
            is_override=True,
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='In a Normal Range',
            valence_description='Within the range of normal based on manual thresholds.',
            is_override=False,
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='Unusually Good',
            valence_description='Significantly lower than normal based on manual thresholds.',
            is_override=False,
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=1,
            valence_label='Better than Normal',
            valence_description='Very high due to X',
            is_override=True,
            metric_check_label='Annotate And Snooze Metric Check',
        ),
    ])
    actual = AnnotateAndSnoozeMetricCheck().run(pd.Series([5, 15, 35, 45], pd.Series(['Very low due to X', '', '', 'Very high due to X'])))
    for i in range(0, len(actual)):
        assert actual[i] == expected[i]