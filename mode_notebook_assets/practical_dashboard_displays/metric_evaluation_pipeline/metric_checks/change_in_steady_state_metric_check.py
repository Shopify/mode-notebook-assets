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

    _min_periods = 2

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
        tmp = tmp.assign(
                    values = s,
                    rolling_average = s.rolling(rolling_window_size).mean(),
                    sign = np.sign(s - s.rolling(rolling_window_size).mean()),
                    # get sign of the difference + or - 1
                    # sign_series.rolling(L1_THRESHOLD).apply() <- are ALL values in this window same sign?
                    # sign_series.rolling(L2_THRESHOLD).apply() <- are ALL values in this window same sign?
                    # score is +/- 0.1 based on the l1 series
                    #

                    # expanding_average = s.expanding(min_periods=_min_periods).mean(),
         )

         tmp = tmp.assign(
                    rolling_sum_L1_THRESHOLD = tmp.sign.rolling(L1_THRESHOLD).sum(),
                    rolling_sum_L2_THRESHOLD = tmp.sign.rolling(L2_THRESHOLD).sum(),
                    activation = 0
         )

         tmp.activation.loc[tmp.rolling_sum_L2 >= L2_THRESHOLD] = 1
         tmp.activation.loc[tmp.rolling_sum_L2 <= L2_THRESHOLD] = -1
         tmp.activation.loc[(tmp.rolling_sum_L1 >= L1_THRESHOLD) and (tmp.rolling_sum_L1 <= L2_THRESHOLD)] = 0.01 + (tmp.rolling_sum_L1 - L1_THRESHOLD)/(L2_THRESHOLD - L1_THRESHOLD)   #prob a cleverer way of getting +ve, -ve cases
         tmp.activation.loc[(tmp.rolling_sum_L1 >= -L1_THRESHOLD) and (tmp.rolling_sum_L1 <= -L2_THRESHOLD)] = -1*(0.01 + (tmp.rolling_sum_L1 - L1_THRESHOLD)/(L2_THRESHOLD - L1_THRESHOLD))


        # determine the length of the longest run
        flip_signs = np.sign(tmp['value'] - tmp['rolling_average'])  # is it above or below average?

        flip_locations = np.where(np.diff(flip_signs))[0]
        flip_locations = np.insert(flip_locations, 0, 0)    # put in first index
        flip_locations = np.append(len(tmp['value']) - 1)   # put in last index

        length_of_runs = np.diff(flip_locations)

        # pseudo-ish
        # find out name of actionable whatever later, but we want to do mapping
        # actionable = length_of_runs.any() > longest_run_1_threshold
        # super_actionable = length_of_runs.any()  > longest_run_2_threshold



        # this will have leading nulls of size s.len - window_size
        # expanding_mean = s.expanding().mean()
        # rolling_mean = s.rolling(rolling_window_size, min_periods = None, win_type = _win_type, closed=None).mean()
        pass
        # return _output
