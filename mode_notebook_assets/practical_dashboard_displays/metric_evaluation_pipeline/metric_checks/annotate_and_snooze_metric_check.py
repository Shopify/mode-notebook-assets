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
    def run(self, annotations: pd.Series) -> pd.Series:

        def map_annotation_to_result(x: str) -> MetricCheckResult:

            if x == '':
                _raw_score = 0
                _is_override = False
                _description = x
                _valence_label = 'Annotation'
            else:
                _raw_score = 1
                _is_override = True
                _description = x
                _valence_label = 'Annotation'

            return MetricCheckResult(
                valence_score=_raw_score,
                valence_label=_valence_label,
                is_override=_is_override,
                valence_description=_description,
                metric_check_label='Annotate And Snooze Metric Check',
            )

        if len(annotations.index) == 0:
            return None


        _output = annotations.apply(
            map_annotation_to_result
        )

        self._validate_output(s=annotations, _output=_output)

        return _output