from dataclasses import dataclass

import numpy as np
import pandas as pd
from plotly import express as px, graph_objects as go

from mode_notebook_assets.practical_dashboard_displays.legacy_helper_functions import map_actionability_score_to_color, \
    dot, sparkline, map_actionability_score_to_description, map_threshold_labels_to_name_by_configuration
from mode_notebook_assets.practical_dashboard_displays.legacy_metric_check import outside_of_normal_range, \
    sudden_change, change_in_steady_state_long


@dataclass
class LegacyMetricEvaluationPipeline:
    s: pd.Series

    metric_name: str = None
    measure_name: str = None

    check_outside_of_normal_range: bool = True
    outside_of_normal_range_minimum_periods: int = 8
    outside_of_normal_range_rolling_calculation_periods: int = None

    check_sudden_change: bool = True
    sudden_change_minimum_periods: int = 7
    sudden_change_rolling_calculation_periods: int = None

    check_change_in_steady_state_long: bool = False
    change_in_steady_state_long_minimum_periods: int = 14

    disable_warnings: bool = False

    is_higher_good: bool = True
    is_lower_good: bool = False
    good_palette: list = None
    bad_palette: list = None
    ambiguous_palette: list = None
    annotations_color=px.colors.sequential.Blues[3],

    def __post_init__(self):

        if self.check_change_in_steady_state_long and not self.disable_warnings:
            raise Warning(
                'The steady_state_long actionability check is an alpha feature and not recommended'
                'for actual use. The current method of a rolling train/test window causes unexpected'
                'results, such as the long run index changing unexpectedly due to the changing historical'
                'average. If you wish to proceed, set the disable_warnings argument to True'
            )

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

        self._actionability_score_columns = [
            s for s in [
                'normal_range_actionability_score' if self.check_outside_of_normal_range else None,
                'sudden_change_actionability_score' if self.check_sudden_change else None,
                'change_in_steady_state_long_actionability_score' if self.check_change_in_steady_state_long else None,
            ] if s is not None
        ]

        if len(self._actionability_score_columns) > 0:
            _results = pd.concat(
                [df for df in
                 [_outside_of_normal_range_results, _sudden_change_results, _change_in_steady_state_long_results] if
                 df is not None],
                axis=1
            )

            _results = _results.loc[:, ~_results.columns.duplicated()]

            self.results = pd.concat([
                _results,
                pd.DataFrame.from_records(
                    [self.combine_actionability_scores(r) for r in
                     _results[self._actionability_score_columns].to_dict(orient='records')],
                    index=_results.index,
                )
            ], axis=1,)
        else:
            _results = pd.DataFrame(self.s)
            _results['period_value'] = self.s
            self.results = _results.assign(general_actionability_score=0, is_valence_ambiguous=False)

    @staticmethod
    def combine_actionability_scores(record: dict):
        return {
            # Take the actionability score farthest from zero
            'general_actionability_score': max(record.values(), key=np.abs),

            # Valence is considered ambiguous if at least two actionability scores have different signs
            'is_valence_ambiguous':        len(set(np.sign(x) for x in record.values() if pd.notna(x) and x != 0)) > 1,
        }

    def get_current_record(self):
        return self.results.to_dict(orient='records')[-1]

    def get_current_actionability_status(self):
        return self.get_current_record()['general_actionability_score']

    def is_current_actionability_ambiguous(self):
        return self.get_current_record()['is_valence_ambiguous']

    def get_current_actionability_status_dot(self):
        _color = map_actionability_score_to_color(
            x=self.get_current_actionability_status(),
            is_valence_ambiguous=self.is_current_actionability_ambiguous(),
            is_higher_good=self.is_higher_good,
            is_lower_good=self.is_lower_good,
            good_palette=self.good_palette,
            bad_palette=self.bad_palette,
            ambiguous_palette=self.ambiguous_palette
        )

        _hex_color = '#%02x%02x%02x' % tuple(
            int(s) for s in _color.replace('rgb(', '').replace(')', '').split(',')
        )

        _mouse_over_text = self.write_actionability_summary(self.get_current_record(), format_html_text=False)

        return dot(_hex_color, title_text=_mouse_over_text)

    def get_current_sparkline(self, periods=20, sparkline_width=2, sparkline_height=.25):
        return sparkline(self.results.tail(periods)['period_value'], figsize=(sparkline_width, sparkline_height))

    def get_current_display_record(self, sparkline=True, sparkline_periods=20, sparkline_width=2, sparkline_height=.25):

        _output = {'Metric': self.metric_name} if self.metric_name else {}

        _output['Current Value'] = self.get_current_record()['period_value']
        _output['Actionability Score'] = self.get_current_actionability_status()
        _output['Status Dot'] = self.get_current_actionability_status_dot()

        if sparkline:
            _output['Sparkline'] = self.get_current_sparkline(
                periods=sparkline_periods,
                sparkline_width=sparkline_width,
                sparkline_height=sparkline_height,
            )

        return _output

    def write_actionability_summary(self, record: dict, is_higher_good=True, is_lower_good=False,
                                    format_html_text=True):
        """
        Method turns a row from self._results into a written summary explaining the actionability status
        of that period. Actionability checks are a single sentence. Summaries might be formatted for HTML
        rendering (i.e. for Plotly tooltips) or plain text display (i.e. title-tag mouseover tooltips) and
        formatting is conditional on these two states.

        Parameters
        ----------
        record: A row from self._results
        is_higher_good: boolean valence metadata for metric interpretation
        is_lower_good: boolean valence metadata for metric interpretation
        format_html_text: if true, apply HTML formatting and punctuation, else format for plain text display

        Returns
        -------
        Textual summary of enabled metric checks for the given period value.
        """
        _bold_start_tag = '<b>' if format_html_text else ''
        _bold_end_tag = '</b>' if format_html_text else ''
        _line_break_tag = '<br>' if format_html_text else ' - '
        _sentence_end_punctuation = '.' if format_html_text else ''

        def _bold_string(s):
            return _bold_start_tag + s + _bold_end_tag

        _description = _bold_start_tag + map_actionability_score_to_description(
            record['general_actionability_score'],
            is_valence_ambiguous=record['is_valence_ambiguous'],
            is_higher_good=is_higher_good,
            is_lower_good=is_lower_good
        ) + _bold_end_tag

        if self.check_outside_of_normal_range:
            _normal_range_sign = np.sign(record["normal_range_actionability_score"])
            _high_or_low = (
                    (_bold_string("high") if record["normal_range_actionability_score"] > 0 else _bold_string("low")) + \
                    " compared with historical ranges"
            )
            _within_normal_str = f"within a {_bold_string('normal')} range based on historical values"
            _is_in_normal_range = record["normal_range_actionability_score"] == 0
            _normal_range_summary = (
                f'Metric is {_within_normal_str if _is_in_normal_range else (_high_or_low)}{_sentence_end_punctuation}'
            )
        else:
            _normal_range_summary = None

        if self.check_sudden_change:
            _sudden_change_sign = np.sign(record["sudden_change_actionability_score"])
            _sudden_dip_or_spike_summary = (
                None if _sudden_change_sign == 0
                else f'Metric {_bold_start_tag}{"increased" if _sudden_change_sign == 1 else "decreased"} '
                     f'suddenly{_bold_end_tag} compared to historical values{_sentence_end_punctuation}'
            )
        else:
            _sudden_dip_or_spike_summary = None

        if self.check_change_in_steady_state_long:
            _change_in_steady_state_long_sign = np.sign(record["change_in_steady_state_long_actionability_score"])
            _change_in_steady_state_long_summary = (
                None if _change_in_steady_state_long_sign == 0
                else f'Metric has been {_bold_string("above" if _change_in_steady_state_long_sign == 1 else "below")}'
                     f'the historical average for {int(record["current_long_run"])} '
                     f'consecutive periods{_sentence_end_punctuation}'
            )
        else:
            _change_in_steady_state_long_summary = None

        _text = _line_break_tag.join([s for s in [_description, _normal_range_summary, _sudden_dip_or_spike_summary,
                                                  _change_in_steady_state_long_summary] if s])

        return _text

    def display_actionability_time_series(self, title=None, metric_name=None,
                                          reference_series: pd.Series = None,
                                          reference_series_name=None,
                                          annotations: dict = None,
                                          display_last_n_valence_periods=1,
                                          show_legend=False, show_normal_range_thresholds=True,
                                          high_detail_range_thresholds=True,
                                          enforce_non_negative_yaxis=True, return_html=True,):

        if reference_series is not None:
            _reference_series = reference_series.copy()
            _reference_series.name = 'reference_series'
            df = pd.concat([self.results, _reference_series], axis=1).dropna()
        else:
            df = self.results.dropna()

        fig = go.Figure(
            layout=go.Layout(
                title=title,
                paper_bgcolor='white',
                plot_bgcolor='white',
                hovermode='x',
            )
        )
        if self.check_outside_of_normal_range:
            # plot thresholds
            if high_detail_range_thresholds:
                threshold_value_list = [
                    'high_l2_threshold_value',
                    'high_l1_threshold_value',
                    'normal_range_rolling_baseline',
                    'low_l1_threshold_value',
                    'low_l2_threshold_value',
                ]
            else:
                threshold_value_list = [
                    'high_l1_threshold_value',
                    'low_l1_threshold_value',
                ]

            for colname in threshold_value_list:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[colname],
                        mode='lines',
                        name=map_threshold_labels_to_name_by_configuration(
                            colname,
                            is_higher_good=self.is_higher_good,
                            is_lower_good=self.is_lower_good,
                        ),
                        line=dict(
                            # This is a bit hacky - fix actionability flag indexing
                            # and move toggle to trace level
                            color='lightgray' if show_normal_range_thresholds else 'white',
                            dash='dash'
                        ),
                        hoverinfo='skip',
                        showlegend=show_legend,
                    )
                )

        # plot actionable periods
        _annotated_indices = annotations.keys() if annotations is not None else []
        actionable_periods_df = df.loc[(df['general_actionability_score'] != 0).values & (~df.index.isin(_annotated_indices))]

        fig.add_trace(
            go.Scatter(
                x=actionable_periods_df.index,
                y=actionable_periods_df.period_value,
                mode='markers',
                name='Actionability',
                hovertext=[
                    self.write_actionability_summary(
                        record,
                        is_higher_good=self.is_higher_good,
                        is_lower_good=self.is_lower_good,
                    ) for record in actionable_periods_df.to_records()],
                hoverinfo="x+text",
                marker=dict(
                    size=10,
                    color=[
                        map_actionability_score_to_color(
                            score,
                            is_valence_ambiguous=is_valence_ambiguous,
                            is_higher_good=self.is_higher_good,
                            is_lower_good=self.is_lower_good,
                            good_palette=self.good_palette,
                            bad_palette=self.bad_palette,
                            ambiguous_palette=self.ambiguous_palette,
                        ) for period, score, is_valence_ambiguous in
                        actionable_periods_df[['general_actionability_score', 'is_valence_ambiguous']].to_records()
                    ]
                ),
                showlegend=show_legend,
            )
        )

        if annotations is not None:
            # plot annotated periods
            _annotated_indices = annotations.keys() if annotations is not None else []
            annotated_periods_df = df.loc[df.index.isin(_annotated_indices)]

            fig.add_trace(
                go.Scatter(
                    x=annotated_periods_df.index,
                    y=annotated_periods_df.period_value,
                    mode='markers',
                    name='Context',
                    hovertext=[f'<b>Context</b><br>{s}' for s in list(annotations.values())],
                    hoverinfo="x+text",
                    marker=dict(
                        color='#0080FF',
                        size=10,
                    ),
                    showlegend=show_legend,
                )
            )

        # Cover up past actionable periods with neutral color
        if display_last_n_valence_periods is not None:

            _df_head = df.head(len(df.index) - display_last_n_valence_periods)
            historical_actionable_periods_df = _df_head.loc[
                (_df_head['general_actionability_score'] != 0).values | (_df_head.index.isin(_annotated_indices))
                ]
            historical_actionable_periods_df = historical_actionable_periods_df.assign(
                overlay_color=[
                    '#D7D7F3' if b else 'lightgray'
                    for b in historical_actionable_periods_df.index.isin(_annotated_indices)
                ]
            )
            fig.add_trace(
                go.Scatter(
                    x=historical_actionable_periods_df.index,
                    y=historical_actionable_periods_df.period_value,
                    mode='markers',
                    name='Historical Alerts',
                    hoverinfo="skip",
                    marker=dict(
                        size=10,
                        color=historical_actionable_periods_df.overlay_color,
                    ),
                    showlegend=show_legend,
                )
            )

        if reference_series is not None:
            # plot reference series
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df.reference_series,
                    mode='lines',
                    name=reference_series_name or 'Reference Value',
                    line=dict(color='lightgrey', width=4),
                    showlegend=show_legend,
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
                showlegend=show_legend,
            )
        )

        if enforce_non_negative_yaxis:
            fig.update_yaxes(rangemode='nonnegative')

        if return_html:
            return fig.to_html()
        else:
            return fig