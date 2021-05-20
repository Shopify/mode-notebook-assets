from abc import ABC, abstractmethod
import pandas as pd

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries


class AbstractMetricCheck(ABC):
    """
    The AbstractMetricCheck implements the MetricCheck design pattern.
    To create your own MetricCheck:
        * Create a new dataclass inheriting from AbstractMetricCheck¹
        * Define configuration-level parameters as dataclass attributes²
        * Override the `apply` method to implement your MetricCheck
        * Return a ValenceScoreSeries

    ¹ When naming MetricChecks, follow the `[A-Za-z]MetricCheck` naming pattern,
    e.g. DeviationFromForecastMetricCheck not CheckMetricAgainstForecast.

    ² Initialization parameters should be independent of the actual data, meaning
    that it can be re-used. For example, you might add a manually set "realistic range"
    using dataclass parameters.
    """

    @abstractmethod
    def apply(self, s: pd.Series) -> ValenceScoreSeries:
        """
        An abstract implementation of MetricCheck.apply(). This method defines the processing
        logic of the MetricCheck. The majority of MetricChecks will only need `s` to execute `apply`.
        Some may use optional additional parameters (see list below).

        Make sure to validate inputs and outputs using the base class methods.

        Required Parameters
        ----------
        s: pd.Series, the numeric metric to be analyzed

        Optional Parameters for Subclass Methods
        ----------
        annotations: pd.Series, a text series of explanations that override other metrics
        target: pd.Series, a numeric series of quantitative goals
        forecast: pd.Series, a numeric series of quantitative expectations
        reference: pd.Series, a numeric series of another relevant metric to compare against

        Returns
        -------
        A pandas series of ValenceScore objects
        """

        # Index should be the same as s, and values should be ValenceScores
        _output_data_series = pd.Series()

        return ValenceScoreSeries(_output_data_series)
