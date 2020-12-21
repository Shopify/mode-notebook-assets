from typing import Any, Callable

from dataclasses import dataclass

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px


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


def create_output_column_for_rolling_period(func: Callable[[pd.Series, int], dict],
                                            df: pd.DataFrame,
                                            derived_colname: str,
                                            minimum_periods: int,
                                            rolling_calculation_periods: Any,
                                            apply_to_colname='period_value'):
    '''
    Performs a rolling or expanding calculation window calculation (func) based on
    minimum_periods and rolling_calculation_periods.

    Creates column "derived_colname" which must be a key to a dictionary output by func.

    Side effects: Mutates df.
    '''
    _apply_function = lambda x: func(x, minimum_periods)[derived_colname]
    _apply_to_series = df[apply_to_colname]

    if rolling_calculation_periods is not None:
        _runtime_rolling_calculation_periods = min(len(_apply_to_series), rolling_calculation_periods)

        df[derived_colname] = _apply_to_series.rolling(_runtime_rolling_calculation_periods).apply(
            _apply_function,
            raw=False,
        )

    else:
        df[derived_colname] = _apply_to_series.expanding(minimum_periods).apply(
            _apply_function,
            raw=False,
        )


def change_in_steady_state_long(s: pd.Series, minimum_periods=14) -> pd.DataFrame:
    '''
    Assumptions: 14 periods or more, 50/50 split between historical series (baseline) and
                 evaluation series (testing)
    '''

    def _change_in_steady_state_long_point_in_time(values: pd.Series, local_minimum_n_periods: int):
        values_series = values
        L1_LONG_RUN_ACTIONABILITY_THRESHOLD = 7
        L2_LONG_RUN_ACTIONABILITY_THRESHOLD = 9

        if len(values) >= local_minimum_n_periods:
            train_test_breakpoint_index = int(len(values) / 2)
            training_series = values_series[:train_test_breakpoint_index]
            testing_series = values_series[train_test_breakpoint_index:]

            mean_of_historical_training_values = training_series.mean()

            current_long_run = 0
            last_value_greater_than_historical_mean = False
            last_value_less_than_historical_mean = False
            for x in testing_series:
                current_value_greater_than_historical_mean = x > mean_of_historical_training_values
                current_value_less_than_historical_mean = x < mean_of_historical_training_values

                increment_long_run_check = (
                        current_value_greater_than_historical_mean == last_value_greater_than_historical_mean
                        and current_value_less_than_historical_mean == last_value_less_than_historical_mean
                        and x != mean_of_historical_training_values
                )

                if increment_long_run_check:
                    current_long_run = current_long_run + 1
                else:
                    current_long_run = 0

                last_value_greater_than_historical_mean = current_value_greater_than_historical_mean
                last_value_less_than_historical_mean = current_value_less_than_historical_mean

            change_in_steady_state_long_actionability_score = 0 if current_long_run < L1_LONG_RUN_ACTIONABILITY_THRESHOLD else (
                    .01 + (-1 if last_value_less_than_historical_mean else 1) * (
                    (current_long_run - L1_LONG_RUN_ACTIONABILITY_THRESHOLD) /
                    (L2_LONG_RUN_ACTIONABILITY_THRESHOLD - L1_LONG_RUN_ACTIONABILITY_THRESHOLD))
            )

            return {
                # Actionability
                'change_in_steady_state_long_actionability_score': change_in_steady_state_long_actionability_score,

                # Threshold
                'mean_of_historical_training_values':              mean_of_historical_training_values,

                # Intermediate Values
                'current_long_run':                                current_long_run,
            }

        else:
            return {
                'change_in_steady_state_long_actionability_score': None,
                'mean_of_historical_training_values':              None,
                'current_long_run':                                None,
            }

    _t = pd.DataFrame(s)

    output_columns = [
        'change_in_steady_state_long_actionability_score',
        'mean_of_historical_training_values',
        'current_long_run',
    ]

    _t['period_value'] = s

    for colname in output_columns:
        create_output_column_for_rolling_period(
            _change_in_steady_state_long_point_in_time,
            _t,
            colname,
            minimum_periods=minimum_periods,
            rolling_calculation_periods=None
        )

    return _t


def sudden_change(s: pd.Series, minimum_periods=7, rolling_calculation_periods=None) -> pd.DataFrame:
    def _sudden_change_point_in_time(values: pd.Series, local_minimum_n_periods: int):
        L1_SUDDEN_CHANGE_CONSTANT = 3.27
        L2_SUDDEN_CHANGE_CONSTANT = 4.905

        values_series = values

        if len(values) >= local_minimum_n_periods:
            mean_of_historical_values = values_series.mean()
            mean_of_pop_differences = abs(values_series - values_series.shift(1)).mean()
            most_recent_period_change = values_series[-1] - values_series[-2]

            is_actionable = np.abs(most_recent_period_change) >= L1_SUDDEN_CHANGE_CONSTANT * mean_of_pop_differences

            sudden_change_l1_threshold_value = L1_SUDDEN_CHANGE_CONSTANT * mean_of_pop_differences
            sudden_change_l2_threshold_value = L2_SUDDEN_CHANGE_CONSTANT * mean_of_pop_differences

            sudden_change_actionability_score = 0 if not is_actionable else (
                    (abs(most_recent_period_change) - sudden_change_l1_threshold_value)
                    / (sudden_change_l2_threshold_value - sudden_change_l1_threshold_value)
                    * np.sign(most_recent_period_change)
            )

            return {
                # Actionability
                'sudden_change_actionability_score': sudden_change_actionability_score,

                # Thresholds
                'sudden_change_l1_threshold_value':  sudden_change_l1_threshold_value,
                'sudden_change_l2_threshold_value':  sudden_change_l2_threshold_value,

                # Intermediate Values
                'most_recent_period_change':         most_recent_period_change,
            }

        else:
            return {
                'sudden_change_actionability_score': None,
                'sudden_change_l1_threshold_value':  None,
                'sudden_change_l2_threshold_value':  None,
                'most_recent_period_change':         None,
            }

    _t = pd.DataFrame(s)

    output_columns = [
        'sudden_change_actionability_score',
        'sudden_change_l1_threshold_value',
        'sudden_change_l2_threshold_value',
        'most_recent_period_change',
    ]

    _t['period_value'] = s

    for colname in output_columns:
        create_output_column_for_rolling_period(
            _sudden_change_point_in_time,
            _t,
            colname,
            minimum_periods=minimum_periods,
            rolling_calculation_periods=rolling_calculation_periods
        )

    return _t


def outside_of_normal_range(s: pd.Series, minimum_periods=8, rolling_calculation_periods=None) -> pd.DataFrame:
    def _outside_of_normal_range_point_in_time(values: pd.Series, local_minimum_n_periods: int):
        '''
        Calculates Outside of Normal Range check, including thresholds, for a point in time.
        This function is applied to a rolling time series
        '''
        # Statistical process control constants
        L1_NORMAL_RANGE_CONSTANT = 2.66
        L2_NORMAL_RANGE_CONSTANT = 3.99

        values_series = values

        if len(values) >= local_minimum_n_periods:
            mean_of_historical_values = values_series.mean()
            mean_of_pop_differences = abs(values_series - values_series.shift(1)).mean()
            most_recent_value = values_series[-1]
            most_recent_value_deviation = most_recent_value - mean_of_historical_values
            is_actionable = np.abs(most_recent_value_deviation) >= L1_NORMAL_RANGE_CONSTANT * mean_of_pop_differences

            low_l2_threshold_value = mean_of_historical_values - L2_NORMAL_RANGE_CONSTANT * mean_of_pop_differences
            low_l1_threshold_value = mean_of_historical_values - L1_NORMAL_RANGE_CONSTANT * mean_of_pop_differences
            high_l1_threshold_value = mean_of_historical_values + L1_NORMAL_RANGE_CONSTANT * mean_of_pop_differences
            high_l2_threshold_value = mean_of_historical_values + L2_NORMAL_RANGE_CONSTANT * mean_of_pop_differences

            normal_range_actionability_score = 0 if not is_actionable else (
                    (abs(most_recent_value_deviation) - mean_of_pop_differences * L1_NORMAL_RANGE_CONSTANT)
                    / (
                            mean_of_pop_differences * L2_NORMAL_RANGE_CONSTANT - mean_of_pop_differences * L1_NORMAL_RANGE_CONSTANT)
                    * np.sign(most_recent_value_deviation)
            )

            return {
                # Actionability
                'normal_range_actionability_score': normal_range_actionability_score,

                # Thresholds
                'low_l2_threshold_value':           low_l2_threshold_value,
                'low_l1_threshold_value':           low_l1_threshold_value,
                'high_l1_threshold_value':          high_l1_threshold_value,
                'high_l2_threshold_value':          high_l2_threshold_value,

                # Intermediate Calculations
                'mean_of_historical_values':        mean_of_historical_values,
                'mean_of_pop_differences':          mean_of_pop_differences,
            }

        else:
            return {
                'normal_range_actionability_score': None,
                'low_l2_threshold_value':           None,
                'low_l1_threshold_value':           None,
                'high_l1_threshold_value':          None,
                'high_l2_threshold_value':          None,
                'mean_of_historical_values':        None,
                'mean_of_pop_differences':          None,
            }

    _t = pd.DataFrame(s)

    output_columns = [
        'normal_range_actionability_score',
        'low_l2_threshold_value',
        'low_l1_threshold_value',
        'high_l1_threshold_value',
        'high_l2_threshold_value',
    ]

    _t['period_value'] = s

    for colname in output_columns:
        # TODO: This is very inefficient. For this to scale, especially scanning
        #       many time series, shouldn't re-do each ts calculation five times
        #       unnecessarily!
        create_output_column_for_rolling_period(
            _outside_of_normal_range_point_in_time,
            _t,
            colname,
            minimum_periods=minimum_periods,
            rolling_calculation_periods=rolling_calculation_periods
        )

    return _t


def map_actionability_score_to_color(x: float, is_valence_ambiguous=False, is_higher_good=True, is_lower_good=False,
                                     good_palette=None, bad_palette=None, ambiguous_palette=None):
    _good_palette = list(good_palette or px.colors.sequential.Greens[3:-2])
    _bad_palette = list(bad_palette or px.colors.sequential.Reds[3:-2])
    _ambiguous_palette = list(ambiguous_palette or ['rgb(255,174,66)'])

    if x == 0:
        return 'rgb(0,0,0)'
    elif is_valence_ambiguous:
        return _ambiguous_palette[
            int(min(np.floor(np.abs(x) * (len(_ambiguous_palette) - 1)), len(_ambiguous_palette) - 1))]
    else:
        _is_good = (is_higher_good and x > 0) or (is_lower_good and x < 0)
        if _is_good:
            return _good_palette[int(min(np.floor(np.abs(x) * (len(_good_palette) - 1)), len(_good_palette) - 1))]
        else:
            return _bad_palette[int(min(np.floor(np.abs(x) * (len(_bad_palette) - 1)), len(_bad_palette) - 1))]


def map_actionability_score_to_description(x: float, is_valence_ambiguous=False, is_higher_good=True,
                                           is_lower_good=False):
    if x == 0:
        return 'Within a Normal Range'
    elif is_valence_ambiguous:
        return 'Ambiguous'
    else:
        _is_good = (is_higher_good and x > 0) or (is_lower_good and x < 0)
        if _is_good:
            if np.abs(x) > 1:
                return 'Extraordinary'
            else:
                return 'Actionably Good'
        else:
            if np.abs(x) > 1:
                return 'Crisis'
            else:
                return 'Actionably Bad'


def map_threshold_labels_to_name_by_configuration(label: str, is_higher_good=True, is_lower_good=False):
    is_high = 'high' in label
    is_low = 'low' in label
    is_l1 = 'l1' in label
    is_l2 = 'l2' in label

    if is_high and is_l2:
        return 'Extraordinary' if is_higher_good else 'Crisis'
    elif is_high and is_l1:
        return 'Actionably Good' if is_higher_good else 'Actionably Bad'
    elif is_low and is_l1:
        return 'Actionably Good' if is_lower_good else 'Actionably Bad'
    elif is_low and is_l2:
        return 'Extraordinary' if is_lower_good else 'Crisis'
    else:
        return label