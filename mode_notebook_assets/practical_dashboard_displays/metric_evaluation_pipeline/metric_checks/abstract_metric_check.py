from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union

import pandas as pd
from pandas.api.types import is_numeric_dtype

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult

OptionalSeries = Union[pd.Series, None]


class AbstractMetricCheck(ABC):
    """
    The AbstractMetricCheck implements the MetricCheck design pattern.
    To create your own MetricCheck:
        * Create a new dataclass inheriting from AbstractMetricCheck¹
        * Define configuration-level parameters as dataclass attributes²
        * Override the `run` method to implement your MetricCheck
        * Return a series of MetricCheckResults

    ¹ When naming MetricChecks, follow the `[A-Za-z]MetricCheck` naming pattern,
    e.g. DeviationFromForecastMetricCheck not CheckMetricAgainstForecast.

    ² Initialization parameters should be independent of the actual data, meaning
    that it can be re-used. Attributes that might change from run to run should
    be passed to `run`. For example, you might add a manually set "realistic range"
    using dataclass parameters.
    """

    @staticmethod
    def _validate_inputs(s: pd.Series, *args) -> None:
        """
        Validates all input series. The first series is assumed to be the
        main metric series, and it also accepts an arbitrary number of
        other series. Example usage is;

        ```
        self._validate_inputs(s, annotations, target)
        ```

        Parameters
        ----------
        s: The main Pandas Series for the MetricCheck
        args: One or more optional/additional series used in the MetricCheck, e.g. forecast or target

        Returns
        -------
        None
        """
        def _assert_single_contiguous_dense_sequence(_series: pd.Series) -> None:
            """
            Assert that the input series has no Null values after removing leading
            and trailing Nulls. An motivating example for this requirement is a
            ForecastCheck, which might have a main value series that ends with trailing
            Nulls, and a forecast series that begins with leading nulls, but the actual
            and forecast periods should have no nulls.

            This is a strong assertion, and I'm not 100% sure it's the right one, but
            I'm putting it in because I'd rather start out with more constraints. However,
            we can revisit this design choice.
            """

            assert is_numeric_dtype(_series), 'The "Single Contiguous Dense Sequence" constraint should only be ' \
                                              'applied to numeric Series'

            assert (
                not _series.loc[_series.first_valid_index(): _series.last_valid_index()].isnull().values.any()
            ), (
                'Numeric series may have leading or trailing null values to represent missing or non-applicable '
                'data points. However, values for the series should otherwise be non-Null.'
            )

        _assert_single_contiguous_dense_sequence(s)

        for _input_series in args:
            if is_numeric_dtype(_input_series):
                _assert_single_contiguous_dense_sequence(_input_series)
            assert isinstance(_input_series, pd.Series), 'All MetricCheck inputs should be Pandas Series.'
            assert (_input_series.index == s.index), '''
                All MetricCheck inputs must have identical indices. This is 
                enforced by the MetricEvaluationPipeline. If the MetricCheck is run 
                outside of a MetricEvaluationPipeline, it is the responsibility of the 
                caller to conform the indices.
            '''

    @staticmethod
    def _validate_output(s: pd.Series, _output: pd.Series) -> None:
        """
        Check the output is valid.

        Parameters
        ----------
        s: The input metric data series
        _output: The output series created by `run`

        Returns
        -------
        None
        """

        assert s.index.equals(_output.index), 'MetricCheck should not change the index of the series. ' \
                                              'Indexing must be handled by the MetricEvaluationPipeline.'
        assert (isinstance(_output, pd.Series)), 'MetricCheck output must be a Pandas Series.'
        for result in _output.values:
            assert issubclass(result.__class__, MetricCheckResult), 'All elements of MetricCheck output ' \
                                                                    'must inherit from the MetricCheckResult'

    @abstractmethod
    def run(self, s: pd.Series) -> pd.Series:
        """
        An abstract implementation of MetricCheck.run(). This method defines the processing
        logic of the MetricCheck. The majority of MetricChecks will only need `s` to run.
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
        A pandas series of MetricCheckResult objects
        """

        # Validate inputs
        self._validate_inputs(s)

        # Index should be the same as s, and values should be MetricCheckResults
        _output = pd.Series()

        # Validate outputs
        self._validate_output(s, _output)

        return _output
