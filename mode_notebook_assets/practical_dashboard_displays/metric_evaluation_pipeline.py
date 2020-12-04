from dataclasses import dataclass

import pandas as pd
import numpy as np

import plotly.graph_objects as go

from mode_notebook_assets.practical_dashboard_displays.helper_functions import map_actionability_score_to_color, \
    map_actionability_score_to_description, map_threshold_labels_to_name_by_configuration
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_statistics import change_in_steady_state_long, \
    sudden_change, outside_of_normal_range


@dataclass
class MetricEvaluationPipeline:
    s: pd.Series

    check_outside_of_normal_range = True
    outside_of_normal_range_minimum_periods = 8
    outside_of_normal_range_rolling_calculation_periods = None

    check_sudden_change = True
    sudden_change_minimum_periods = 7
    sudden_change_rolling_calculation_periods = None

    check_change_in_steady_state_long = True
    change_in_steady_state_long_minimum_periods = 14

    def __post_init__(self):
        _outside_of_normal_range_results = outside_of_normal_range(
            self.s,
            minimum_periods=self.outside_of_normal_range_minimum_periods,
            rolling_calculation_periods=self.outside_of_normal_range_rolling_calculation_periods
        ) if self.check_outside_of_normal_range else None

        _sudden_change_results = sudden_change(
            self.s,
            minimum_periods=self.sudden_change_minimum_periods,
            rolling_calculation_periods=self.sudden_change_rolling_calculation_periods
        ) if self.check_sudden_change else None

        _change_in_steady_state_long_results = change_in_steady_state_long(
            self.s,
            minimum_periods=self.change_in_steady_state_long_minimum_periods
        ) if self.check_change_in_steady_state_long else None

        _results = pd.concat(
            [df for df in
             [_outside_of_normal_range_results, _sudden_change_results, _change_in_steady_state_long_results] if
             df is not None],
            axis=1
        )

        _results = _results.loc[:, ~_results.columns.duplicated()]

        self._actionability_score_columns = [s for s in [
            'normal_range_actionability_score' if self.check_outside_of_normal_range else None,
            'sudden_change_actionability_score' if self.check_sudden_change else None,
            'change_in_steady_state_long_actionability_score' if self.check_change_in_steady_state_long else None,
        ] if s is not None
                                             ]

        self.results = pd.concat([
            _results,
            pd.DataFrame.from_records(
                [self.combine_actionability_scores(r) for r in
                 _results[self._actionability_score_columns].to_dict(orient='records')],
                index=_results.index,
            ),
        ],
            axis=1,
        )

    def combine_actionability_scores(self, record: dict):
        return {
            # Take the actionability score farthest from zero
            'general_actionability_score': max(record.values(), key=np.abs),

            # Valence is considered ambiguous if at least two actionability scores have different signs
            'is_valence_ambiguous':        len(set(np.sign(x) for x in record.values() if pd.notna(x) and x != 0)) > 1,
        }

    def write_actionability_summary(self, record: dict, is_higher_good=True, is_lower_good=False):

        _description = '<b>' + map_actionability_score_to_description(
            record['general_actionability_score'],
            is_valence_ambiguous=record['is_valence_ambiguous'],
            is_higher_good=is_higher_good,
            is_lower_good=is_lower_good
        ) + '</b>'

        _normal_range_sign = np.sign(record["normal_range_actionability_score"])
        _sudden_change_sign = np.sign(record["normal_range_actionability_score"])
        _change_in_steady_state_long_sign = np.sign(record["change_in_steady_state_long_actionability_score"])

        _high_or_low = (
                ("<b>high</b>" if record["normal_range_actionability_score"] > 0 else "<b>low</b>") +\
                " compared with historical ranges"
        )
        _within_normal_str = "within a <b>normal</b> range based on historical values"
        _normal_range_summary = (
            f'Metric is {_within_normal_str if record["normal_range_actionability_score"] == 0 else (_high_or_low)}.')

        _sudden_dip_or_spike_summary = (
            None if _sudden_change_sign == 0
            else f'Metric <b>{"increased" if _sudden_change_sign == 1 else "decreased"} '
                 f'suddenly</b> compared to historical values.'
        )

        _change_in_steady_state_long_summary = (
            None if _change_in_steady_state_long_sign == 0
            else f'Metric has been <b>{"above" if _change_in_steady_state_long_sign == 1 else "below"}</b> the '
                 f'historical average for {int(record["current_long_run"])} consecutive periods.'
        )
        _text = "<br>".join([s for s in [_description, _normal_range_summary, _sudden_dip_or_spike_summary,
                                         _change_in_steady_state_long_summary] if s])

        return _text

    def display_actionability_time_series(self, title=None, metric_name=None, display_last_n_valence_periods=4,
                                          is_higher_good=True, is_lower_good=False, good_palette=None, bad_palette=None,
                                          ambiguous_palette=None):
        df = self.results.dropna()

        fig = go.Figure(
            layout=go.Layout(
                title=title,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode='x',
            )
        )

        # plot thresholds
        threshold_value_list = [
            'high_l2_threshold_value',
            'high_l1_threshold_value',
            'low_l1_threshold_value',
            'low_l2_threshold_value',
        ]

        for colname in threshold_value_list:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[colname],
                    mode='lines',
                    name=map_threshold_labels_to_name_by_configuration(
                        colname,
                        is_higher_good=is_higher_good,
                        is_lower_good=is_lower_good,
                    ),
                    line=dict(color=('lightgray' if 'l1' in colname else 'darkgray'), dash='dash'),
                    hoverinfo='skip',
                    showlegend=False,
                )
            )

        # plot actionable periods
        actionable_periods_df = df.query('general_actionability_score != 0')
        fig.add_trace(
            go.Scatter(
                x=actionable_periods_df.index,
                y=actionable_periods_df.period_value,
                mode='markers',
                name='Actionability',
                hovertext=[
                    self.write_actionability_summary(
                        record,
                        is_higher_good=is_higher_good,
                        is_lower_good=is_lower_good,
                    ) for record in actionable_periods_df.to_records()],
                hoverinfo="text",
                marker=dict(
                    size=10,
                    color=[
                        map_actionability_score_to_color(
                            score,
                            is_valence_ambiguous=is_valence_ambiguous,
                            is_higher_good=is_higher_good,
                            is_lower_good=is_lower_good,
                            good_palette=good_palette,
                            bad_palette=bad_palette,
                            ambiguous_palette=ambiguous_palette,
                        ) for period, score, is_valence_ambiguous in
                        actionable_periods_df[['general_actionability_score', 'is_valence_ambiguous']].to_records()
                    ]
                ),
                showlegend=False,
            )
        )

        # Cover up past actionable periods with neutral color
        if display_last_n_valence_periods is not None:
            historical_actionable_periods_df = df.head(len(df.index) - display_last_n_valence_periods).query(
                'general_actionability_score != 0')
            fig.add_trace(
                go.Scatter(
                    x=historical_actionable_periods_df.index,
                    y=historical_actionable_periods_df.period_value,
                    mode='markers',
                    name='Historical Alerts',
                    hoverinfo="skip",
                    marker=dict(
                        size=10,
                        color=['lightgray'] * len(historical_actionable_periods_df.period_value),
                    ),
                    showlegend=False,
                )
            )

        # plot period values
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.period_value,
                mode='lines',
                name=metric_name or 'Period Value',
                line=dict(color='gray', width=4),
                showlegend=False,
            )
        )

        return fig
