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
    TODO
    """
    is_higher_better: bool = True
    is_lower_better: bool = False

    # for checks with running averages
    is_rolling_window: bool = True # if false, use an expanding window
    rolling_periods: int = 14

    longest_run_1_threshold: int = 7
    longest_run_2_threshold: int = 9

    _min_periods = 1

    def run(self, s: pd.Series) -> pd.Series:
        # ------ PSEUDO CODE ------
        # Validity checks (enough values in the series? valid number of rolling periods?)
        # Split series into baseline / test
        # Calculate the mean on the baseline
        # Use 7 & 9 for longest run thresholds
            # a. Calculate default thresholds based on th mean (stdev or something else)
            # b. Allow for manual thresholding (later)
        # Determine if values are above or below the mean
        # Track number of consecutive values that are above/below the mean
        # Linear interpolation of the longest # of runs (in future improvement consider supporting something other than linear interpolation)
            # this is the raw score
        #  Normalize raw scores
        # ------ END PSEUDO CODE ------


        # Calculate rolling & expanding averages, and store
        df = pd.DataFrame(
                {   'metric':           s,
                    'rolling_average':  s.rolling(rolling_window_size, min_periods=_min_periods).mean(),
                    'sign':             np.sign(s - s.rolling(rolling_window_size, min_periods=_min_periods).mean())
                }
            )

        # calculate the rolling sums with windows equal in size to our L1 & L2 thresholds
        df = df.assign(
                rolling_sum_L1_THRESHOLD = df.sign.rolling(L1_THRESHOLD, min_periods=1).sum(),
                rolling_sum_L2_THRESHOLD = df.sign.rolling(L2_THRESHOLD, min_periods=1).sum(),
                activation = 0
            )

        # define mapping to actionability score
        def _actionability_score_mapping(r, L1_THRESHOLD, L2_THRESHOLD):
            '''
            This method takes the rolling count above/below the L1/L2 thresholds and maps
            them to an actionability score
            '''
            if abs(r.rolling_sum_L2_THRESHOLD) >= L2_THRESHOLD:
                return np.sign(r.rolling_sum_L2_THRESHOLD)
            else:
                return np.sign(r.rolling_sum_L1_THRESHOLD) * (((abs(r.rolling_sum_L1_THRESHOLD) - L1_THRESHOLD) / L2_THRESHOLD) + 0.01)

        # apply mapping
        df['activation'] = df.apply(lambda row: _actionability_score_mapping(row), axis=1)

        pass
        # return _output
