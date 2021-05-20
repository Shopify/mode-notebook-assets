from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import numpy as np

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score_series import \
    ValenceScoreSeries


@dataclass
class StaticNormalRangeMetricCheck(AbstractMetricCheck):
    """
    This class implements the static "within a normal range" metric check.
    This check assumes that the metric is more or less static within
    the training window. For use on metric that have a long term trend,
    use the "dynamic normal range" metric check.
    """
    is_higher_better: bool = True
    is_lower_better: bool = False
    is_rolling_window: bool = True
    rolling_periods: int = 12
    l1_normal_range_constant: float = 2.66
    l2_normal_range_constant: float = 3.99
    maximum_learning_differences_quantile: float = 1

    # "Private" class attributes
    _metric_check_label: str = 'Static Normal Range Check'

    def _calculate_central_measure(self, s: pd.Series) -> pd.Series:
        """
        Calculate a central measure e.g. rolling average or a linear trend.
        In this case I'm using a rolling average as a default.
        """
        if self.is_rolling_window:
            return s.rolling(self.rolling_periods).mean()
        else:
            return s.expanding().mean()

    def _calculate_rolling_mean_of_period_over_period_differences(self, s: pd.Series) -> pd.Series:
        """
        Calculate the period over period differences for use
        in statistical process control calculations.
        """
        # TODO: This was originally _differences_series = abs(s - s.shift(1))
        _differences_series = abs(s.shift(1) - s.shift(2))

        if self.is_rolling_window:
            _median_window = _differences_series.rolling(self.rolling_periods)
        else:
            _median_window = _differences_series.expanding()

        _windowed_quantile_series = _median_window.quantile(self.maximum_learning_differences_quantile, interpolation='higher')

        _learning_differences_series = _differences_series.combine(_windowed_quantile_series, min)

        if self.is_rolling_window:
            _learning_window = _learning_differences_series.rolling(self.rolling_periods)
        else:
            _learning_window = _learning_differences_series.expanding()

        return _learning_window.mean()

    def _calculate_thresholds_and_scores(self, s: pd.Series, central_measure: pd.Series,
                                         mean_differences: pd.Series) -> pd.DataFrame:
        """
        Calculates thresholds and raw valence scores.
        """
        def _calculate_threshold_series(sign: int, constant: float) -> pd.Series:
            return central_measure + (sign * constant * mean_differences)

        def _calculate_raw_valence_score(record: dict) -> float:
            if record['period_value'] <= record['lower_l2_threshold']:
                return -1
            elif record['period_value'] <= record['lower_l1_threshold']:
                return (
                    (record['period_value'] - record['lower_l1_threshold']) /
                    (record['lower_l1_threshold'] - record['lower_l2_threshold'])
                )
            elif record['period_value'] >= record['higher_l2_threshold']:
                return 1
            elif record['period_value'] >= record['higher_l1_threshold']:
                return (
                        (record['period_value'] - record['higher_l1_threshold']) /
                        (record['higher_l2_threshold'] - record['higher_l1_threshold'])
                )
            else:
                return 0

        _threshold_df = pd.DataFrame(central_measure, columns=['central_measure']).assign(
            period_value=s,
            mean_differences=mean_differences,
            lower_l2_threshold=_calculate_threshold_series(-1, self.l2_normal_range_constant),
            lower_l1_threshold=_calculate_threshold_series(-1, self.l1_normal_range_constant),
            higher_l1_threshold=_calculate_threshold_series(1, self.l1_normal_range_constant),
            higher_l2_threshold=_calculate_threshold_series(1, self.l2_normal_range_constant),
        )

        _raw_scores = _threshold_df.apply(_calculate_raw_valence_score, axis=1)

        return _threshold_df.assign(raw_valence_scores=_raw_scores)

    def apply(self, s: pd.Series) -> ValenceScoreSeries:
        """
        Apply method for the normal range metric check.

        Parameters
        ----------
        s: metric time series

        Returns
        -------
        ValenceScoreSeries
        """
        def _map_raw_score_to_result(_raw_score: float) -> ValenceScore:

            _normalized_score = normalize_valence_score(
                _raw_score=_raw_score,
                is_higher_better=self.is_higher_better,
                is_lower_better=self.is_lower_better
            )

            _base_description = map_sign_to_string(_raw_score, [
                    'Lower than normal based on historical values.',
                    'Within the range of normal based on historical values.',
                    'Higher than normal based on historical values.'
                ],
                                                   )

            return ValenceScore(
                valence_score=_normalized_score,
                valence_label=map_score_to_string(_normalized_score),
                valence_description=map_score_to_string(_normalized_score, labels=[
                    f'Significantly {_base_description.lower()}',
                    _base_description,
                    _base_description,
                    _base_description,
                    f'Significantly {_base_description.lower()}',
                ]),
                metric_check_label=self._metric_check_label,
            )

        self._validate_inputs(s)

        _central_measure_series = self._calculate_central_measure(s)
        _mean_period_over_period_difference_series = self._calculate_rolling_mean_of_period_over_period_differences(s)
        _score_and_threshold_dataframe = self._calculate_thresholds_and_scores(
            s=s,
            central_measure=_central_measure_series,
            mean_differences=_mean_period_over_period_difference_series,
        )

        _output_data_series = _score_and_threshold_dataframe.raw_valence_scores.apply(_map_raw_score_to_result)

        self._validate_output(s, _output_data_series)

        return ValenceScoreSeries(_output_data_series)
