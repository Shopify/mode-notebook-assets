from dataclasses import dataclass
import pandas as pd
from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck
@dataclass
class AnnotateAndSnoozeMetricCheck(AbstractMetricCheck):
    """
    Override the metric annotations to manually specified descriptions.
    """
    def run(self, s: pd.Series, annotations: pd.Series) -> pd.Series:
        """
        if annotations len(annotations.index) == 0:
            _output = None
        else:
            _output = annotations.apply(map_string_to_result)
        """
        def map_string_to_result(x: float) -> MetricCheckResult:
            if x = '':
                _raw_score = 0
                _is_override = False
            else:
                _raw_score = 1
                _is_override = True
                _base_description = x
            return MetricCheckResult(
                valence_score=_raw_score,
                valence_label=map_score_to_string(_raw_score),
                is_override=_is_override,
                valence_description=_base_description,
                metric_check_label='Annotate And Snooze Metric Check',
            )
        self._validate_inputs(s)
        _output = annotations.apply(
            map_string_to_result
        )
        self._validate_output(s=s, _output=_output)
        return _output