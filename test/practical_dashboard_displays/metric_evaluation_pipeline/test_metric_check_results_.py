import pytest

from mode_notebook_assets.practical_dashboard_displays.helper_functions import functional_setattr
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScore


def ignore_child_metric_check_results(mcr: ValenceScore) -> ValenceScore:
    return functional_setattr(mcr, 'child_metric_check_results', [])


def test_init_metric_check_result():
    assert ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )


def test_priority_preference():
    priority_1 = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
        priority_score=1,
    )
    priority_2a = ValenceScore(
        valence_score=1.2,
        valence_label='Higher',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    expected = ignore_child_metric_check_results(
        ValenceScore(
            valence_score=0,
            valence_label='Normal',
            valence_description='Nothing to see here',
            priority_score=1,
        )
    )
    assert priority_1 + priority_2a == expected


def test_priority_preference_tie():
    priority_2a = ValenceScore(
        valence_score=1.2,
        valence_label='Higher',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    priority_2b = ValenceScore(
        valence_score=1,
        valence_label='High',
        valence_description='Nothing to see here',
        priority_score=2,
    )
    expected = ignore_child_metric_check_results(
        ValenceScore(
            valence_score=1.2,
            valence_label='Higher',
            valence_description='Nothing to see here',
            priority_score=2,
            metric_check_label='Combined Metric Check',
        )
    )
    assert priority_2a + priority_2b == expected


def test_override_preference():
    override = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
        is_override=True,
    )
    not_override = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )
    expected = ignore_child_metric_check_results(
        ValenceScore(
            valence_score=0,
            valence_label='Normal',
            valence_description='Nothing to see here',
            is_override=True,
        )
    )

    assert override + not_override == expected
