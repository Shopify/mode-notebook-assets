from dataclasses import dataclass
import pandas as pd
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore, \
    ValenceScoreSeries


@dataclass
class AnnotateAndSnoozeMetricCheck(AbstractMetricCheck):
    """
    Override the metric annotations to manually specified descriptions.
    """
    def apply(self, annotations: pd.Series) -> ValenceScoreSeries:

        def map_annotation_to_result(x: str) -> ValenceScore:

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

            return ValenceScore(
                valence_score=_raw_score,
                valence_label=_valence_label,
                is_override=_is_override,
                valence_description=_description,
                metric_check_label='Annotate And Snooze Metric Check',
            )

        _output = annotations.apply(
            map_annotation_to_result
        )

        return ValenceScoreSeries(_output)
