import pytest

from mode_notebook_assets.practical_dashboard_displays.helper_functions import functional_setattr
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult


def ignore_child_metric_check_results(mcr: MetricCheckResult) -> MetricCheckResult:
    return functional_setattr(mcr, 'child_metric_check_results', [])


def test_init_metric_check_result():
    assert MetricCheckResult(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )


def test_priority_preference():
    priority_1 = MetricCheckResult(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
        priority_score=1,
    )
    priority_2a = MetricCheckResult(
        valence_score=1.2,
        valence_label='Higher',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    expected = ignore_child_metric_check_results(
        MetricCheckResult(
            valence_score=0,
            valence_label='Normal',
            valence_description='Nothing to see here',
            priority_score=1,
        )
    )
    assert priority_1 + priority_2a == expected


def test_priority_preference_tie():
    priority_2a = MetricCheckResult(
        valence_score=1.2,
        valence_label='Higher',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    priority_2b = MetricCheckResult(
        valence_score=1,
        valence_label='High',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    expected = ignore_child_metric_check_results(
        MetricCheckResult(
            valence_score=1.2,
            valence_label='Higher',
            valence_description='Nothing to see here',
            priority_score=2,
            metric_check_label='Combined Metric Check',
        )
    )
    assert priority_2a + priority_2b == expected


def test_override_preference():
    override = MetricCheckResult(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
        is_override=True,
    )
    not_override = MetricCheckResult(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )
    expected = ignore_child_metric_check_results(
        MetricCheckResult(
            valence_score=0,
            valence_label='Normal',
            valence_description='Nothing to see here',
            is_override=True,
        )
    )

    assert override + not_override == expected
