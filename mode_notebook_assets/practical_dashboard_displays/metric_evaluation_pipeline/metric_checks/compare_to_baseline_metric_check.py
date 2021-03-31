from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

@dataclass
class CompareToBaselineMetricCheck(AbstractMetricCheck):
    """
    Compare the metric to a manually specified constant baseline.
    It also includes the option to have a percent threshold. #TODO

    Initialization
    --------------
    baseline: float of what the constant baseline is
    threshold_pct: float of what the percent range above and below the baseline is considered within range.
    """
    baseline: float = 0.0
    threshold_pct: float = 0.1

    def run(self, s: pd.Series, baseline: int, threshold_pct: int):

        def map_value_to_result(x: int) -> MetricCheckResult:
            if (x - baseline) / baseline < -1 * threshold_pct:
                _raw_score = -1
            elif ((x - baseline) / baseline >= -1 * threshold_pct) & ((x - baseline) / baseline <= threshold_pct):
                _raw_score = 0
            elif (x - baseline) / baseline > threshold_pct:
                _raw_score = 1
            else:
                _raw_score = 0

            _base_labels = map_sign_to_string(
                _raw_score, [
                    'Lower than',
                    'Within the range of',
                    'Higher than'
                ],
            )

            _base_description = map_sign_to_string(
                _raw_score, [
                    'Lower than normal based on manual thresholds.',
                    'Within the range of normal based on manual thresholds.',
                    'Higher than normal based on manual thresholds.'
                ],
            )

            return MetricCheckResult(
                valence_score=_raw_score,
                valence_label=_base_labels,
                valence_description=_base_description,
                metric_check_label='Compare to Baseline Metric Check',

            )

        _output = s.apply(
            map_value_to_result
        )

        return _output

