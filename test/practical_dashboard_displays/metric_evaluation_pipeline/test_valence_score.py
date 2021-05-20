import pytest

from mode_notebook_assets.practical_dashboard_displays.helper_functions import functional_setattr
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScore


def ignore_child_valence_scores(mcr: ValenceScore) -> ValenceScore:
    return functional_setattr(mcr, 'child_valence_scores', [])


def test_init_valence_score():
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
    expected = ignore_child_valence_scores(
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
    expected = ignore_child_valence_scores(
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
    expected = ignore_child_valence_scores(
        ValenceScore(
            valence_score=0,
            valence_label='Normal',
            valence_description='Nothing to see here',
            is_override=True,
        )
    )

    assert override + not_override == expected


def test_positive_valence_magnitude_preference():
    neutral_score = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )
    actionable_score = ValenceScore(
        valence_score=1.2,
        valence_label='Higher',
        valence_description='Nothing to see here',
    )
    expected = ignore_child_valence_scores(
        ValenceScore(
            valence_score=1.2,
            valence_label='Higher',
            valence_description='Nothing to see here',
        )
    )
    assert (neutral_score + actionable_score).valence_score == expected.valence_score


def test_negative_valence_magnitude_preference():
    neutral_score = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )
    actionable_score = ValenceScore(
        valence_score=-1.2,
        valence_label='Lower',
        valence_description='Nothing to see here',
    )
    expected = ignore_child_valence_scores(
        ValenceScore(
            valence_score=-1.2,
            valence_label='Lower',
            valence_description='Nothing to see here',
        )
    )
    assert (neutral_score + actionable_score).valence_score == expected.valence_score


def test_ambiguous_valence_score():
    neutral_score = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
    )
    negative_score = ValenceScore(
        valence_score=-1.2,
        valence_label='Lower',
        valence_description='Nothing to see here',
    )
    positive_score = ValenceScore(
        valence_score=1.2,
        valence_label='Lower',
        valence_description='Nothing to see here',
    )

    assert not (neutral_score + negative_score).is_ambiguous
    assert not (neutral_score + positive_score).is_ambiguous
    assert (positive_score + negative_score).is_ambiguous


def test_high_priority_neutral_check_ignored():
    high_priority_neutral_score = ValenceScore(
        valence_score=0,
        valence_label='Normal',
        valence_description='Nothing to see here',
        priority_score=1
    )

    default_priority_negative_score = ValenceScore(
        valence_score=-1,
        valence_label='Lower',
        valence_description='Nothing to see here',
    )

    assert (high_priority_neutral_score + default_priority_negative_score).valence_score == -1
