from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore, \
    ValenceScoreSeries


@dataclass
class RealisticRangeMetricCheck(AbstractMetricCheck):
    upper_bound: float
    lower_bound: float

    def apply(self, s: pd.Series) -> ValenceScoreSeries:
        def check_values_against_bounds(x: float) -> ValenceScore:
            if x > self.upper_bound:
                _valence_label = 'Above Realistic Range'
                _description = 'Result is higher than make sense for this metric'
                _is_ambiguous = True
                _raw_score = 1
            elif x < self.lower_bound:
                _valence_label = 'Below Realistic Range'
                _description = 'Result is lower than make sense for this metric'
                _is_ambiguous = True
                _raw_score = -1
            else:
                _valence_label = ''
                _description = 'Result makes sense for this metric'
                _is_ambiguous = False
                _raw_score = 0

            return ValenceScore(
                valence_label=_valence_label,
                valence_description=_description,
                is_ambiguous=_is_ambiguous,
                valence_score=_raw_score,
                metric_check_label='Realistic Range Metric Check'
            )

        self._validate_inputs(s)

        _output = s.apply(
            check_values_against_bounds
        )

        self._validate_output(s=s, _output=_output)

        return ValenceScoreSeries(_output)
