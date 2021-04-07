from dataclasses import dataclass
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

@dataclass
class RecentPeriodDriverAnalysis:
    """
    This class implements metrics and visualizations
    for analyzing how a particular category is driving
    changes in a higher level metric.

    For example, we might want to look at which lead
    sources are driving changes in opportunity
    creation.
    """
    data_frame: pd.DataFrame
    date_column: str
    metric_column: str
    grouping_column: str
    period_type: str
    rolling_comparison_periods: int
    display_top_n_groups: int
    title: str

    @staticmethod
    def _make_metric_df(ts, rolling_periods):
        return pd.DataFrame(ts).assign(
            rolling_avg_ts=lambda df: df[ts.name].rolling(rolling_periods).mean(),
            vs_rolling_avg_absolute=lambda df: df[ts.name] - df['rolling_avg_ts'],
            vs_rolling_avg_relative=lambda df: df['vs_rolling_avg_absolute'] / df['rolling_avg_ts'],
        ).rename({ts.name: 'period_value'})

    def _add_top_groups_column(self):
        top_groups = self.data_frame \
            .groupby(self.grouping_column) \
            .sum()[self.metric_column] \
            .sort_values() \
            .tail(self.display_top_n_groups).index

        return self.data_frame.assign(
            top_groups=self.data_frame[self.grouping_column].apply(lambda s: s if s in top_groups else 'Other')
        )

    def __post_init__(self):
        self.data_frame = self._add_top_groups_column()

        _groups = self.data_frame.set_index(
            pd.to_datetime(self.data_frame[self.date_column])
        ).groupby('top_groups')

        group_dfs = {}

        for source, _df in _groups:
            group_dfs[source] = self._make_metric_df(
                _df.groupby(pd.Grouper(freq=self.period_type)).sum()[self.metric_column],
                rolling_periods=self.rolling_comparison_periods,
            ).reset_index().to_dict(orient='records')[-1]

        self.group_dfs = group_dfs
        self.group_deviations_df = pd.DataFrame.from_dict(
            self.group_dfs,
            orient='index',
        )

    def plot_period_deviations(self) -> go.Figure:
        """
        Creates a plot comparing absolute deviation from the
        rolling average vs. the relative deviation from the
        rolling average. Larger absolute deviations are bigger
        drivers of top-line trends, whereas larger relative
        deviations represent bigger deviations from normal.

        This visualization helps identify drivers and anomalies
        and put them into perspective based on impact.

        Returns
        -------
        Plotly Figure
        """

        _axis_scale_factor = 1.2
        _y_axis_range_base = _axis_scale_factor * max(np.abs(self.group_deviations_df['vs_rolling_avg_relative']))
        _x_axis_range_base = _axis_scale_factor * max(np.abs(self.group_deviations_df['vs_rolling_avg_absolute']))

        return px.scatter(
            data_frame=self.group_deviations_df.reset_index(),
            x='vs_rolling_avg_absolute',
            y='vs_rolling_avg_relative',
            text='index',
            title='Retail SQL Driver Analysis: Retail SQLs (March 2021)',
            labels=dict(
                index=self.grouping_column.replace('_', ' ').title(),
                vs_rolling_avg_absolute='Actual Difference vs. Rolling Average',
                vs_rolling_avg_relative='Relative Difference vs. Rolling Average'
            ),
            template='plotly_white',
        ).update_layout({
            'yaxis': {
                'tickformat': ',.0%',
                'range': (-1 * _y_axis_range_base, _y_axis_range_base),
                'zerolinecolor': '#a0a9b8',
            },
            'xaxis': {
                'range': (-1 * _x_axis_range_base, _x_axis_range_base),
                'zerolinecolor': '#a0a9b8',
            },
        })

