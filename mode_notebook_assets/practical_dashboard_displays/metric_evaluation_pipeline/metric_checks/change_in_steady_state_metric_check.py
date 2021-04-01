from dataclasses import dataclass
import pandas as pd
import numpy as np

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

@dataclass
class ChangeInSteadyStateMetricCheck(AbstractMetricCheck):
    """
    Calculating if there has been a deviation from steady state within the period.
    The methodology and thresholds are suggested by Nick Desbarats (Practical Dashboards author)

    We assume a symmetric actionable/extreme ranges about the historical mean.

    Initialization
    --------------
    is_higher_better:   Should we interpret higher metric values as good (positive valence)?
                        Default value is True.
    is_lower_better:    Should we interpret lower metric values as good (positive valence)?
                        Default value is False.
    _min_periods:       Minimum number of periods to calculate the metric.
                        Default value is 1
    is_rolling_window:  Boolean of whether to use a rolling or expanding period.
                        Default value is True
    rolling_periods:    Int of the number of periods for rolling historical mean
                        Default value is 7
    l1_threshold:       Int determining the actionable number of consecutive periods the metric
                        was above or below the historical mean
                        Default value is 7
    l2_threshold:       Int determining the extreme number of consecutive periods the metric
                        was above or below the historical mean
                        Default value is 9
    """

    # for all checks
    is_higher_better: bool = True
    is_lower_better: bool = False

    # for checks with running averages
    _min_periods = 1
    is_rolling_window: bool = True # if false, expanding
    rolling_periods: int = 7

    # consecutive run threshold for steady state
    l1_threshold: int = 7
    l2_threshold: int = 9


    def __post_init__(self):
        assert self.l1_threshold < self.l2_threshold, 'L1 threshold must be less than L2 threshold.'


    def run(self, s: pd.Series) -> pd.Series:

        self._validate_inputs(s)

        # Calculate rolling or expanding mean, and store
        metric_mean = s.rolling(self.rolling_periods, min_periods = self._min_periods).mean() if self.is_rolling_window else s.expanding(min_periods = self._min_periods).mean()

        df = pd.DataFrame(
            {   'metric':  s,
                'metric_mean': metric_mean,
                'sign':    np.sign(s - metric_mean)
            }
        )

        # For each value in the sign series, track the number of previous
        # values that are on the same side of the mean (while tracking the current sign)
        # Example sign series: [1,1,-1,-1,-1,1,1,1,1,1]
        # Resulting series:    [1,2,-1,-2,-3,1,2,3,4,5]
        curr_val = None
        curr_consecutive_count = 0
        running_reps = []
        for x in df.sign:
            if curr_val is None:
                curr_val = x
            if x == curr_val:
                curr_consecutive_count += x
            else:
                curr_val = x
                curr_consecutive_count = x
            running_reps.append(curr_consecutive_count)
        df['running_reps'] = running_reps

        # Make default activation 0
        df = df.assign(
            activation = 0
        )

        # define mapping to actionability score
        def _actionability_score_mapping(r, L1_THRESHOLD, L2_THRESHOLD):
            '''
            This method takes the rolling count above/below the L1/L2 thresholds and maps
            them to an actionability score
            '''
            if abs(r.running_reps) >= L2_THRESHOLD:
                return np.sign(r.running_reps)
            elif abs(r.running_reps) < L1_THRESHOLD:
                return 0
            else:
                return np.sign(r.running_reps) * (((abs(r.running_reps) - L1_THRESHOLD) / (L2_THRESHOLD - L1_THRESHOLD)) + 0.01)

        # apply mapping and return
        df.activation = df.apply(lambda row: _actionability_score_mapping(row, self.l1_threshold, self.l2_threshold), axis=1)

        def map_value_to_result(_raw_score: float) -> MetricCheckResult:

            _normalized_score = normalize_valence_score(
                _raw_score,
                is_higher_better=self.is_higher_better,
                is_lower_better=self.is_lower_better,
            )

            _base_description = map_sign_to_string(
                _raw_score, [
                    'Drop in steady state below historical mean.',
                    'No significant change from historical mean.',
                    'Rise in steady state above historical mean.'
                ],
            )

            if np.isnan(_raw_score):
                return MetricCheckResult(
                    valence_score=0,
                    valence_label=map_score_to_string(0),
                    valence_description='Not enough data to calculate if change in prior period is significant.',
                    metric_check_label='Change in Steady State Check',
                )

            return MetricCheckResult(
                valence_score=_normalized_score,
                valence_label=map_score_to_string(_normalized_score),
                valence_description=map_score_to_string(_normalized_score, labels=[
                    f'Significant {_base_description.lower()}',
                    _base_description,
                    _base_description,
                    _base_description,
                    f'Significant {_base_description.lower()}',
                ]),
                metric_check_label='Change in Steady State Check',
            )

        _output = df.activation.apply(
            map_value_to_result
        )

        self._validate_output(s=s, _output=_output)

        return _output
