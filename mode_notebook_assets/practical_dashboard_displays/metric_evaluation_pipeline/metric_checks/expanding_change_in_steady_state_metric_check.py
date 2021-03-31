from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

@dataclass
class ExpandingChangeInSteadyStateMetricCheck(AbstractMetricCheck):
    """
    TODO
    """
    is_higher_better: bool = True
    is_lower_better: bool = False
    longest_run_1_threshold: int = 7
    longest_run_2_threshold: int = 9

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


        # Split series into baseline / test




        # this will have leading nulls of size s.len - window_size
        expanding_mean = s.expanding().mean()
        rolling_mean = s.rolling(rolling_window_size, min_periods = None, win_type = _win_type, closed=None).mean()
        pass
        # return _output
