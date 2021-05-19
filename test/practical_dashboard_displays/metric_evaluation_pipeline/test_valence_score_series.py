import pytest

import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScore
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score_series import \
    ValenceScoreSeries

GOOD_VALENCE_SCORE = ValenceScore(
    valence_score=1,
    valence_label='Good',
    valence_description='Good',
)

BAD_VALENCE_SCORE = ValenceScore(
    valence_score=-1,
    valence_label='Bad',
    valence_description='Bad',
)

NEUTRAL_VALENCE_SCORE = ValenceScore(
    valence_score=0,
    valence_label='Normal',
    valence_description='Nothing to see here',
)

EXAMPLE_INDEX = [
    '2050-01-01',
    '2050-01-02',
    '2050-01-03',
]


def test_init_valence_score_series():
    assert ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
            ],
            index=[
                '2050-01-01',
                '2050-01-02',
                '2050-01-03',
            ]
        )
    )


def test_repr_valence_score_series():
    assert ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
            ],
            index=[
                '2050-01-01',
                '2050-01-02',
                '2050-01-03',
            ]
        )
    ).__repr__()


def test_combine_valence_score_series():
    s1 = ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                GOOD_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
            ],
            index=EXAMPLE_INDEX
        )
    )

    s2 = ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
                BAD_VALENCE_SCORE,
            ],
            index=EXAMPLE_INDEX
        )
    )

    expected = ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                GOOD_VALENCE_SCORE,
                BAD_VALENCE_SCORE,
            ],
            index=EXAMPLE_INDEX
        )
    )

    actual = s1 + s2
    assert (
        actual._score_series.apply(lambda v: v.valence_score)
        == expected._score_series.apply(lambda v: v.valence_score)
    ).all()


def test_last_record():
    s1 = ValenceScoreSeries(
        pd.Series(
            data=[
                NEUTRAL_VALENCE_SCORE,
                NEUTRAL_VALENCE_SCORE,
                GOOD_VALENCE_SCORE,
            ],
            index=EXAMPLE_INDEX
        )
    )

    assert s1.last_record() == GOOD_VALENCE_SCORE


def test_only_combine_identical_index_assertion():
    with pytest.raises(AssertionError):
        s1 = ValenceScoreSeries(
            pd.Series(
                data=[
                    NEUTRAL_VALENCE_SCORE,
                    NEUTRAL_VALENCE_SCORE,
                    NEUTRAL_VALENCE_SCORE,
                ],
                index=EXAMPLE_INDEX
            )
        )

        s2 = ValenceScoreSeries(
            pd.Series(
                data=[
                    NEUTRAL_VALENCE_SCORE,
                    NEUTRAL_VALENCE_SCORE,
                    NEUTRAL_VALENCE_SCORE,
                ],
                index=[
                    '1999-01-01',
                    '1999-01-02',
                    '1999-01-03',
                ]
            )
        )

        # This combination should fail
        s1 + s2


def test_require_valence_score_series_assertion():
    with pytest.raises(AssertionError):
        s1 = ValenceScoreSeries(
            pd.Series(
                data=[
                    NEUTRAL_VALENCE_SCORE,
                    1,
                    NEUTRAL_VALENCE_SCORE,
                ],
                index=EXAMPLE_INDEX
            )
        )
