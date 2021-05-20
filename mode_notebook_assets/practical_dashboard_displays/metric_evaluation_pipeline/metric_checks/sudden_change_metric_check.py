from dataclasses import dataclass
import pandas as pd
import numpy as np

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score \
    import ValenceScore, ValenceScoreSeries
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

SUDDEN_CHANGE_METRIC_CHECK_LABEL = 'Sudden Change Metric Check'


@dataclass
class SuddenChangeMetricCheck(AbstractMetricCheck):
    """
    Calculating if there has been a sudden change over prior period.

    The methodology and thresholds are suggested by Nick Desbarats (Practical Dashboards author)
    as an application of XmR charts from Statistical Process Control (SPC) theory.

    For more information about SPC and XmR charts, please see: 
    https://r-bar.net/control-chart-constants-tables-explanations/

    Initialization
    --------------
    is_higher_better:   Should we interpret higher metric values as good (positive valence)?
                        Default value is True.
    is_lower_better:    Should we interpret lower metric values as good (positive valence)?
                        Default value is False.
    minimum_periods:    Minimum number of periods to calculate the metric.
                        Default value is 3
    is_rolling_window:  Boolean of whether to use a rolling or expanding period.
                        Default value is True
    rolling_periods:    Int of the number of periods for rolling.
                        Default value is 12
    l1_check_constant:  Constant float for determining actionable range
                        Default value is 3.27
    l2_check_constant:  Constant float for determining extreme range
                        Default value is 4.905
    """
    # for all checks
    is_higher_better: bool = True
    is_lower_better: bool = False

    # for checks with running averages
    minimum_periods: int = 3
    is_rolling_window: bool = True  # if false, expanding
    rolling_periods: int = 12

    # for checks with SPC constants
    l1_check_constant: float = 3.27
    l2_check_constant: float = 4.905

    def apply(self, s: pd.Series) -> ValenceScoreSeries:

        period_change = s - s.shift(1)

        if self.is_rolling_window:
            mean_of_pop_differences = abs(s - period_change). \
                rolling(self.rolling_periods, min_periods=self.minimum_periods).mean()
        else:
            mean_of_pop_differences = abs(s - period_change). \
                expanding(min_periods=self.minimum_periods).mean()

        sudden_change_l1_threshold_value = self.l1_check_constant * mean_of_pop_differences
        sudden_change_l2_threshold_value = self.l2_check_constant * mean_of_pop_differences

        period_is_actionable = np.abs(period_change) >= sudden_change_l1_threshold_value

        period_score = (abs(period_change) - sudden_change_l1_threshold_value) \
                       / (sudden_change_l2_threshold_value - sudden_change_l1_threshold_value) \
                       * np.sign(period_change)

        period_score_actionable = period_score * period_is_actionable

        def map_value_to_result(_raw_score: float) -> ValenceScore:

            _normalized_score = normalize_valence_score(
                _raw_score,
                is_higher_better=self.is_higher_better,
                is_lower_better=self.is_lower_better,
            )

            _base_description = map_sign_to_string(
                _raw_score, [
                    'drop in value over prior period.',
                    'No significant change from prior period.',
                    'spike in value over prior period.'
                ],
            )

            if np.isnan(_raw_score):
                return ValenceScore(
                    valence_score=0,
                    valence_label=map_score_to_string(0),
                    valence_description='Not enough data to calculate if change in prior period is significant.',
                    metric_check_label=SUDDEN_CHANGE_METRIC_CHECK_LABEL,
                )

            return ValenceScore(
                valence_score=_normalized_score,
                valence_label=map_score_to_string(_normalized_score),
                valence_description=map_score_to_string(_normalized_score, labels=[
                    f'Sudden significant {_base_description.lower()}',
                    f'Sudden {_base_description.lower()}',
                    _base_description,
                    f'Sudden {_base_description.lower()}',
                    f'Sudden significant {_base_description.lower()}',
                ]),
                metric_check_label=SUDDEN_CHANGE_METRIC_CHECK_LABEL,
            )

        self._validate_inputs(s)

        _output = period_score_actionable.apply(
            map_value_to_result
        )

        self._validate_output(s=s, _output=_output)

        return ValenceScoreSeries(_output)