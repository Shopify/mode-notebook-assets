from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.annotate_and_snooze_metric_check import \
    AnnotateAndSnoozeMetricCheck

def test_annotations():
    expected = pd.Series([
        MetricCheckResult(
            valence_score=1,
            is_override=True,
            valence_label='Annotation',
            valence_description='Very low due to X',
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='Annotation',
            valence_description='',
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='Annotation',
            valence_description='',
            metric_check_label='Annotate And Snooze Metric Check',
        ),
        MetricCheckResult(
            valence_score=1,
            is_override=True,
            valence_label='Annotation',
            valence_description='Very high due to X',
            metric_check_label='Annotate And Snooze Metric Check',
        ),
    ])
    actual = AnnotateAndSnoozeMetricCheck().run(pd.Series(['Very low due to X', '', '', 'Very high due to X']))
    for i in range(0, len(actual)):
        assert actual[i] == expected[i]

