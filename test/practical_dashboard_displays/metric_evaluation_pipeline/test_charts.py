import pytest

import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScore, ValenceScoreSeries
from mode_notebook_assets.practical_dashboard_displays.plot.charts import CumulativeTargetAttainmentValenceChart, \
    TimeSeriesValenceLineChart


def test_target_chart():
    # read test series
    _start = '2021-01-01'
    _end = '2021-02-01'
    _target_date_range = pd.date_range(
        start=_start,
        end=_end,
        freq='D',
        closed='left',
    )
    _target_index = pd.DatetimeIndex(_target_date_range)
    _actual_periods = 20
    _actual_date_range = _target_date_range[:20]
    _actual_series = pd.Series(
        data=[10]*_actual_periods,
        index=pd.DatetimeIndex(_actual_date_range)
    )

    CumulativeTargetAttainmentValenceChart(
        actual=_actual_series,
        target_total=11000,
        period_start_date=_start,
        period_end_date=_end,
    ).to_plotly_figure()


def test_valence_time_series_chart():
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
        '2050-01-04',
        '2050-01-05',
        '2050-01-06',
    ]

    TimeSeriesValenceLineChart(
        result=MetricEvaluationResult(
            data=pd.Series(
                data=[100, 100, 50, 100, 100, 200],
                index=EXAMPLE_INDEX,
            ),
            valence_score_series=ValenceScoreSeries(
                s=pd.Series(
                    data=[
                        NEUTRAL_VALENCE_SCORE,
                        NEUTRAL_VALENCE_SCORE,
                        BAD_VALENCE_SCORE,
                        NEUTRAL_VALENCE_SCORE,
                        NEUTRAL_VALENCE_SCORE,
                        GOOD_VALENCE_SCORE,
                    ],
                    index=EXAMPLE_INDEX
                )
            )
        ),
        title='Test Chart',
        metric_name='Volume',
    ).to_plotly_figure()
