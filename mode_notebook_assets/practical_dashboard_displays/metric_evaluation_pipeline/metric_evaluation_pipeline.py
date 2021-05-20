from dataclasses import dataclass
from typing import List

import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks as checks
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks import \
    AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries


@dataclass
class MetricEvaluationPipeline:

    metric_checks: List[AbstractMetricCheck] = None
    append_to_metric_checks: List[AbstractMetricCheck] = None

    def __post_init__(self):

        self.metric_checks = self.metric_checks or [
            checks.StaticNormalRangeMetricCheck(),
            checks.SuddenChangeMetricCheck(),
            checks.AnnotateAndSnoozeMetricCheck(),
        ]

        if self.append_to_metric_checks:
            self.metric_checks.append(self.append_to_metric_checks)

    def _validate_input_series(self) -> None:
        pass

    def _validate_output_series(self) -> None:
        pass

    def apply(self, s, **kwargs) -> ValenceScoreSeries:
        # Validate input
        # Verify that the appropriate inputs are present
        # Apply MetricChecks using the appropriate inputs
        # Combine the outputs of the checks
        # Validate the output
        # Return output
        return NotImplemented
