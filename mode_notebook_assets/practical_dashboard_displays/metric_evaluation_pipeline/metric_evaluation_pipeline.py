import functools
import operator
from dataclasses import dataclass
from typing import List
from inspect import signature

import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks as checks
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks import \
    AbstractMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries, ValenceScore


@dataclass
class MetricEvaluationResultMetadata:
    name: str = None
    url: str = None


@dataclass
class MetricEvaluationResult:
    data: pd.Series
    valence_score_series: ValenceScoreSeries
    metadata: MetricEvaluationResultMetadata = None

    def __post_init__(self):
        try:
            pd.testing.assert_index_equal(self.data.index, self.valence_score_series.score_series.index, check_names=False)
        except AssertionError:
            raise AssertionError('''
                    MetricEvaluationResult data and valence_score_series must have the same index.
                ''')

    def add_metadata(self, name: str = None, url: str = None):
        """
        Adds metadata to self.metadata. If a value is provided, it overrides the
        existing value. If None is provided it does not change the existing value.

        Returns self for method chaining.
        """
        if self.metadata is None:
            self.metadata = MetricEvaluationResultMetadata(
                name=name,
                url=url,
            )
        else:
            if name:
                self.metadata.name = name
            if url:
                self.metadata.url = url

        return self

    def plot(self):
        return NotImplemented

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns time series, valence, and supplemental data to user as a Pandas DataFrame.
        TODO: Pass extra data series, thresholds, and intermediate values.

        Returns
        -------
        pd.DataFrame
        """
        return pd.merge(
            self.data.rename('Period Value'),
            self.valence_score_series.score_series.rename('ValenceScore Object'),
            left_index=True,
            right_index=True,
        ).join(
            pd.json_normalize(self.valence_score_series.score_series.apply(lambda v: v.to_dict()))
        )



@dataclass
class MetricEvaluationPipeline:
    metric_checks: List[AbstractMetricCheck] = None
    append_to_metric_checks: List[AbstractMetricCheck] = None

    def __post_init__(self):

        if self.metric_checks != list():
            self.metric_checks = self.metric_checks or [
                checks.StaticNormalRangeMetricCheck(),
                checks.SuddenChangeMetricCheck(),
            ]

        if self.append_to_metric_checks:
            self.metric_checks.extend(self.append_to_metric_checks)

    @staticmethod
    def _validate_input_series(s, **kwargs) -> None:
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
        kwargs: One or more optional/additional series used in the MetricCheck, e.g. forecast or target

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
            assert (
                _series.loc[_series.first_valid_index(): _series.last_valid_index()].notnull().all()
            ), (
                'Numeric series may have leading or trailing null values to represent missing or non-applicable '
                'data points. However, values for the series should otherwise be non-Null.'
            )

        _assert_single_contiguous_dense_sequence(s)

        for _input_series in kwargs.values():
            assert isinstance(_input_series, pd.Series), 'All MetricCheck inputs should be Pandas Series.'
            if is_numeric_dtype(_input_series):
                _assert_single_contiguous_dense_sequence(_input_series)
            try:
                pd.testing.assert_index_equal(_input_series.index, s.index, check_names=False),
            except AssertionError:
                raise AssertionError('''
                    All MetricCheck inputs must have identical indices. This is 
                    enforced by the MetricEvaluationPipeline. If the MetricCheck is applied 
                    outside of a MetricEvaluationPipeline, it is the responsibility of the 
                    caller to conform the indices.
                ''')

    @staticmethod
    def _validate_output_series(s: pd.Series, _output: pd.Series) -> None:
        """
        Check the output is valid.

        Parameters
        ----------
        s: The input metric data series
        _output: The output series created by `apply`

        Returns
        -------
        None
        """
        assert (isinstance(_output, pd.Series)), 'MetricCheck output must be a Pandas Series.'

        assert s.index.equals(_output.index), 'MetricCheck should not change the index of the series. ' \
                                              'Indexing must be handled by the MetricEvaluationPipeline.'
        for result in _output.values:
            assert issubclass(result.__class__, ValenceScore), 'All elements of MetricCheck output ' \
                                                               'must inherit from the ValenceScore'

    def apply(self, s, annotations: pd.Series = None, target: pd.Series = None, forecast: pd.Series = None,
              reference: pd.Series = None) -> MetricEvaluationResult:

        assert not s.empty, 'Primary series should not be empty'

        _optional_input_series = {
            # We're more permissive with annotations so they can be optional by default
            'annotations': (
                pd.Series(data=['' for _ in s], index=s.index) if annotations is None
                else annotations.reindex(index=s.index, fill_value='')
            ),

            # These numeric series are None unless provided by the user
            'target':      target,
            'forecast':    forecast,
            'reference':   reference,
        }

        # Verify that the appropriate inputs are present
        for check in self.metric_checks:
            for name, series in _optional_input_series.items():
                if name in signature(check.apply).parameters:
                    assert series is not None, f'Input {name} is required by {check.__class__}.'

        # Validate input
        self._validate_input_series(
            s, **{key: value for key, value in _optional_input_series.items() if value is not None}
        )

        # Apply MetricChecks using the appropriate inputs
        _metric_check_results = []
        for check in self.metric_checks:
            _required_inputs = {
                key: value for key, value in _optional_input_series.items()
                if key in signature(check.apply).parameters
            }
            _metric_check_results.append(
                check.apply(s, **_required_inputs)
            )

        # Combine the outputs of the checks using __add__ method
        _output_valence_score_series = functools.reduce(
            operator.add,
            _metric_check_results
        )

        # Validate the output
        self._validate_output_series(s, _output_valence_score_series.score_series)

        # Return output
        return MetricEvaluationResult(
            data=s,
            valence_score_series=_output_valence_score_series
        )