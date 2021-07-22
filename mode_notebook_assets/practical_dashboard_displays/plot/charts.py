from copy import copy
from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from IPython.core.display import HTML

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries, ValenceScore
from mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration import PlotConfiguration


@dataclass
class ValenceChart:
    time_series: pd.Series
    valence_score_series: ValenceScoreSeries
    reference_series_list: List[pd.Series] = None
    config: PlotConfiguration = None
    layout: go.Layout = None

    def __post_init__(self):
        self.reference_series_list = self.reference_series_list or []
        self.config = self.config or PlotConfiguration()
        self.layout = self.layout or go.Layout()

    def _build_figure(self) -> go.Figure:
        fig = go.Figure(
            layout=self.layout,
        ).update_layout(
            template=self.config.plotly_template,
        )
        for series in self.reference_series_list:
            fig.add_trace(
                self.config.secondary_chart_trace_template.update(
                    x=series.index,
                    y=series.values,
                    name=series.name,
                )
            )

        # Add the main metric trace
        fig.add_trace(
            self.config.primary_chart_trace_template.update(
                x=self.time_series.index,
                y=self.time_series.values,
                name=self.time_series.name,
            )
        )

        # Add color dots with mouseover text for past valence scores
        fig.add_trace(
            self.config.valence_chart_trace_template.update(
                x=self.time_series.index,
                y=self.time_series.values,
                text=self.valence_score_series.score_series.apply(
                    lambda v: f'<b>{v.valence_label}</b><br>{v.valence_description}'
                ),
                marker=self.config.valence_chart_trace_template.marker.update(
                    color=[
                        self.config.map_valence_score_to_color(score)
                        for score in self.valence_score_series.score_series
                    ]
                )
            )
        )

        # Cover up past valence with a neutral color
        fig.add_trace(
            self.config.valence_chart_trace_template.update(
                x=self.time_series.index[0:-1],
                y=self.time_series.values[0:-1],
                marker=self.config.valence_chart_trace_template.marker.update(
                    color=[
                        self.config.map_past_valence_scores_to_color(score)
                        for score in self.valence_score_series.score_series[0:-1]
                    ]
                )
            )
        )

        return fig

    def to_html(self) -> HTML:
        return self._build_figure().to_html()

    def to_plotly_figure(self) -> go.Figure:
        return self._build_figure()


@dataclass
class TimeSeriesValenceLineChart:
    result: MetricEvaluationResult
    title: str = None
    metric_name: str = None
    config: PlotConfiguration = None

    def __post_init__(self):
        self.config = self.config or PlotConfiguration()

    def to_html(self) -> HTML:
        return HTML(self.to_plotly_figure().to_html())

    def to_plotly_figure(self) -> go.Figure:
        return ValenceChart(
            time_series=self.result.data.rename(self.metric_name),
            valence_score_series=self.result.valence_score_series,
            config=self.config,
            layout=go.Layout(title=self.title)
        ).to_plotly_figure()


@dataclass
class CumulativeTargetAttainmentValenceChart:
    """
    Class for creating a cumulative target attainment display.
    It answers the question "how are we pacing against our end
    of period target"? Valence indicators are based on whether
    we are pacing towards our end of period goal.

    Input series are non-cumulative, but will be transformed
    to cumulative series for calculation and display.

    Parameters
    ----------
    actual: Non-cumulative time series of actual values (pd.Series)
    target_total: The total target for the given period (int)
    target_period_index: A pd.DatetimeIndex representing the target period; to get started, try out pd.date_range
    """

    actual: pd.Series
    target_total: int
    period_start_date: str
    period_end_date: str

    metric_name: str = None

    minor_attainment_deviation: float = 0
    major_attainment_deviation: float = .20

    is_higher_good: bool = True
    is_lower_good: bool = False

    config: PlotConfiguration = None

    def __post_init__(self):
        self.config = self.config or PlotConfiguration(
            neutral_valence_color='rgba(0,0,0,0)'
        )

        self.target_period_index = pd.date_range(start=self.period_start_date, end=self.period_end_date)

        self._cleaned_actual = pd.Series(
            data=self.actual.values,
            index=pd.to_datetime(self.actual.index),
        ).reindex(
            index=pd.date_range(self.period_start_date, max(self.actual.index)),
            fill_value=0,
        )

        # generate target series
        number_of_periods = len(self.target_period_index)
        interpolated_period_target = round(self.target_total / number_of_periods)
        period_target_remainder = self.target_total - (interpolated_period_target * number_of_periods)

        current_period = max(self._cleaned_actual.index)
        current_period_index = self._cleaned_actual.index.get_loc(current_period)

        self.target_attainment_df = pd.DataFrame(index=self.target_period_index).assign(
            is_current_period=pd.Series([False] * (len(self._cleaned_actual) - 1) + [True],
                                        index=self._cleaned_actual.index),
            actual=self._cleaned_actual,
            actual_cumulative=self._cleaned_actual.cumsum(),
            target_interpolated=interpolated_period_target,
            target_cumulative=lambda df: df.target_interpolated.cumsum() + period_target_remainder,
            actionability_scores=(
                lambda df: df.apply(
                    lambda r: self._calculate_target_attainment_valence(
                        actual_value=r['actual_cumulative'],
                        target_value=r['target_cumulative'],
                    ) if r['is_current_period'] else ValenceScore(
                        valence_score=0,
                        valence_label='Inside Target Range',
                        valence_description='The actual attainment has not deviated far enough '
                                            'from target to be actionably good or bad.',
                    ),
                    axis=1
                )
            ),
            actionability_actuals=lambda df: df.actual_cumulative,
            # initialize as empty; only last period will be calculated
        )

        self.target_attainment_df.actionability_scores[
            current_period_index] = self._calculate_target_attainment_valence(
            actual_value=self.target_attainment_df.actual_cumulative[current_period_index],
            target_value=self.target_attainment_df.target_cumulative[current_period_index],
        )

    def _calculate_target_attainment_valence(self, actual_value, target_value):

        target_deviation = (actual_value - target_value) / target_value
        try:
            if np.abs(target_deviation) < self.minor_attainment_deviation:
                return ValenceScore(
                    valence_score=0,
                    valence_label='Inside Target Range',
                    valence_description='The actual attainment has not deviated far enough '
                                        'from target to be actionably good or bad.',
                )
            else:
                # The minimum actionable score is 0.01 (minor deviation) and the
                # "soft maximum" is 1 (major deviation). Actionability score is based on
                # where the deviation occurs between the minor and major deviation thresholds.
                # Scores above 1 are allowed but do not change the output.
                pacing_proportion = actual_value / target_value
                return ValenceScore(
                    valence_score=np.sign(target_deviation) * (
                            0.01 + (
                            (np.abs(target_deviation) - self.minor_attainment_deviation)
                            / (self.major_attainment_deviation - self.minor_attainment_deviation)
                    )),
                    valence_label=f'{"Behind" if np.abs(target_deviation) < 0 else "Ahead of"} Target',
                    valence_description='Pacing to {}% of target.'.format(
                        int(100 * pacing_proportion)
                    )
                )
        except:
            return ValenceScore(
                valence_score=1,
                valence_label='Error',
                valence_description='Something went wrong calculating target attainment.',
            )

    def to_html(self) -> HTML:
        return HTML(self.to_plotly_figure().to_html())

    def to_plotly_figure(self) -> go.Figure:
        return ValenceChart(
            time_series=self.target_attainment_df.actual_cumulative.rename('Actual'),
            valence_score_series=ValenceScoreSeries(
                s=self.target_attainment_df.actionability_scores
            ),
            reference_series_list=[self.target_attainment_df.target_cumulative.rename('Target')],
            config=self.config,
        ).to_plotly_figure()
