from dataclasses import dataclass
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.helper_functions import normalize_valence_score, \
    map_score_to_string, map_sign_to_string
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score \
    import ValenceScore
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks.abstract_metric_check \
    import AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score_series import \
    ValenceScoreSeries


@dataclass
class ManualFourThresholdMetricCheck(AbstractMetricCheck):
    """
    Compare the metric to four manually specified thresholds.

    Initialization
    --------------
    threshold_1: The lower bound of extraordinarily low
    threshold_2: The lower found of normal
    threshold_3: The upper bound of normal
    threshold_4: The upper bound of extraordinarily high
    is_higher_better: Should we interpret higher metric values as good (positive valence)?
                      Default value is True.
    is_lower_better: Should we interpret lower metric values as good (positive valence)?
                      Default value is False.
    """
    threshold_1: float
    threshold_2: float
    threshold_3: float
    threshold_4: float
    is_higher_better: bool = True
    is_lower_better: bool = False

    def __post_init__(self):
        _threshold_list = [self.threshold_1, self.threshold_2, self.threshold_3, self.threshold_4]
        assert _threshold_list == sorted(_threshold_list), 'Thresholds must be in increasing order.'

    def apply(self, s: pd.Series) -> ValenceScoreSeries:
        def map_value_to_result(x: float) -> ValenceScore:
            if x <= self.threshold_1:
                _raw_score = -1
            elif x <= self.threshold_2:
                _raw_score = -0.01 - (self.threshold_2 - x) / (self.threshold_2 - self.threshold_1)
            elif x >= self.threshold_3:
                _raw_score = 0.01 + (x - self.threshold_3) / (self.threshold_4 - self.threshold_3)
            elif x >= self.threshold_4:
                _raw_score = 1
            else:
                _raw_score = 0

            _normalized_score = normalize_valence_score(
                _raw_score,
                is_higher_better=self.is_higher_better,
                is_lower_better=self.is_lower_better,
            )

            _base_description = map_sign_to_string(
                _raw_score, [
                    'Lower than normal based on manual thresholds.',
                    'Within the range of normal based on manual thresholds.',
                    'Higher than normal based on manual thresholds.'
                ],
            )

            return ValenceScore(
                valence_score=_normalized_score,
                valence_label=map_score_to_string(_normalized_score),
                valence_description=map_score_to_string(_normalized_score, labels=[
                    f'Significantly {_base_description.lower()}',
                    _base_description,
                    _base_description,
                    _base_description,
                    f'Significantly {_base_description.lower()}',
                ]),
                metric_check_label='Manual Four Threshold Check',
            )

        self._validate_inputs(s)

        _output_data_series = s.apply(
            map_value_to_result
        )

        self._validate_output(s=s, _output=_output_data_series)

        return ValenceScoreSeries(_output_data_series)
