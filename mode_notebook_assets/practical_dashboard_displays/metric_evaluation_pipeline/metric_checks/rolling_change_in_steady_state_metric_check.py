from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

@dataclass
class RollingChangeInSteadyStateMetricCheck(AbstractMetricCheck):
    """
    TODO
    """
    num_rolling_periods: int
    is_higher_better: bool = True
    is_lower_better: bool = False
    longest_run_1_threshold: int = 7
    longest_run_2_threshold: int = 9

    def run(self, s: pd.Series) -> pd.Series:
        # Validity checks (enough values in the series? valid number of rolling periods?)
        # 1. Calculate the rolling mean
        # 2. Use 7 & 9 for longest run thresholds
            # 2.a. Calculate default thresholds based on rolling mean (stdev or something else)
            # 2.b. Allow for manual thresholding (later)
        # 3. Determine if values are above or below rolling mean
        # 4. Track number of consecutive values that are above/below the mean
        # 5. Linear interpolation of the longest # of runs (in future improvement consider supporting something other than linear interpolation)
            # this is the raw score
        #  Normalize raw scores
        pass
        # return _output
