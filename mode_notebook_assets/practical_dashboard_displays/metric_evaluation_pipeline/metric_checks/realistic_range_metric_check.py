from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results \
    import MetricCheckResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck

@dataclass
class RealisticRangeMetricCheck(AbstractMetricCheck):

	upper_bound: float
	lower_bound: float

	def run(self, s: pd.Series) -> pd.Series:
		def check_values_against_bounds(x: float) -> MetricCheckResult:
			if x > self.upper_bound:
				_valence_label = 'Above Upper Bound'
				_description = 'Result is above upper bound'
				_is_ambiguous = False
				_raw_score = 1
			elif x < self.lower_bound:
				_valence_label = 'Below lower Bound'
				_description = 'Result is below lower bound'
				_is_ambiguous = False
				_raw_score = -1
			else:
				_valence_label = ''
				_description = 'Result is between bounds'
				_is_ambiguous = True
				_raw_score = 0

			return MetricCheckResult(
				valence_label=_valence_label,
				valence_description=_description,
				is_ambiguous=_is_ambiguous,
				valence_score=_raw_score,
				metric_check_label= 'Realistic Range Metric Check'
		)

		self._validate_inputs(s)

		_output = s.apply(
			check_values_against_bounds
		)

		self._validate_output(s=s, _output=_output)

		return _output
