from itertools import permutations

import pytest
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.realistic_range_metric_check import \
    RealisticRangeMetricCheck

def test_annotations():

    expected = pd.Series([
        MetricCheckResult(
            valence_score=-1,
            valence_label='Below lower Bound',
            is_ambiguous= False,
            valence_description='Result is below lower bound',
            metric_check_label='Realistic Range Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='',
            is_ambiguous= True,
            valence_description='Result is between bounds',
            metric_check_label='Realistic Range Metric Check',
        ),
        MetricCheckResult(
            valence_score=0,
            valence_label='',
            is_ambiguous= True,
            valence_description='Result is between bounds',
            metric_check_label='Realistic Range Metric Check',
        ),
        MetricCheckResult(
            valence_score=1,
            valence_label='Above Upper Bound',
            is_ambiguous= False,
            valence_description='Result is above upper bound',
            metric_check_label='Realistic Range Metric Check',
        ),
    ])


    actual = RealisticRangeMetricCheck(
        upper_bound=10,
        lower_bound=2
        ).run(pd.Series([1,3,5,11]))


    for i in range(0, len(actual)):
        assert actual[i] == expected[i]