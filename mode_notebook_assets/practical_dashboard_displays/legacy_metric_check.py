from typing import Callable, Any

import numpy as np
import pandas as pd


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
            train_test_breakpoint_index = max(int(len(values) / 2), local_minimum_n_periods)
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
                    (-1 if last_value_less_than_historical_mean else 1) * (
                    .01 + (current_long_run - L1_LONG_RUN_ACTIONABILITY_THRESHOLD) /
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
                'normal_range_rolling_baseline':    mean_of_historical_values,
                'normal_range_rolling_deviation':   mean_of_pop_differences,
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
        'normal_range_rolling_baseline',
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