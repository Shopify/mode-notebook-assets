import pytest
import pandas as pd

import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks as checks

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationPipeline, MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import \
    ValenceScoreSeries, ValenceScore


def test_metric_evaluation_pipeline_initializes():
    assert MetricEvaluationPipeline()


def test_metric_evaluation_pipeline_defaults():
    assert MetricEvaluationPipeline().metric_checks == [
        checks.StaticNormalRangeMetricCheck(),
        checks.SuddenChangeMetricCheck(),
        checks.AnnotateAndSnoozeMetricCheck(),
    ]


def test_metric_evaluation_pipeline_empty_check_list():
    assert MetricEvaluationPipeline(metric_checks=[]).metric_checks == list()


def test_metric_evaluation_pipeline_add_metric_checks():
    assert len(MetricEvaluationPipeline(append_to_metric_checks=[checks.RealisticRangeMetricCheck]).metric_checks) == 4


def test_metric_evaluation_pipeline_override_metric_checks():
    assert len(MetricEvaluationPipeline(metric_checks=[checks.RealisticRangeMetricCheck]).metric_checks) == 1


def test_metric_evaluation_pipeline_runs():
    assert isinstance(MetricEvaluationPipeline().apply(pd.Series([100]*20)), MetricEvaluationResult)


def test_metric_evaluation_pipeline_fails_with_empty_series():
    with pytest.raises(AssertionError):
        assert MetricEvaluationPipeline().apply(pd.Series())


def test_metric_evaluation_pipeline_requires_identical_index():
    with pytest.raises(AssertionError):
        MetricEvaluationPipeline()._validate_input_series(
            s=pd.Series(data=[100]*20, index=range(0, 20)),
            reference=pd.Series(data=[100]*20, index=range(10, 30))
        )


def test_metric_evaluation_pipeline_requires_single_contiguous_inputs():
    non_contiguous_data = [100, None] + [100] * 18
    test_series = [None, None] + [100] * 16 + [None, None]
    test_index = range(0, 20)

    with pytest.raises(AssertionError):
        # Test data series is rejected for non-contiguous data
        MetricEvaluationPipeline._validate_input_series(
            s=pd.Series(data=non_contiguous_data, index=test_index),
        )

    for input_name in ['target', 'forecast', 'reference']:
        with pytest.raises(AssertionError):
            # Test other inputs are rejected for non-contiguous data
            MetricEvaluationPipeline._validate_input_series(
                s=pd.Series(data=test_series, index=test_index),
                **{input_name: pd.Series(data=non_contiguous_data, index=test_index)},
            )


def test_metric_evaluation_pipeline_requires_series_type():
    for input_name in ['target', 'forecast', 'reference']:
        with pytest.raises(AssertionError):
            MetricEvaluationPipeline()._validate_input_series(
                s=pd.Series(data=[100]*20, index=range(0, 20)),
                **{input_name: [100]*18},
            )


def test_metric_evaluation_pipeline_output_requires_identical_index():
    with pytest.raises(AssertionError):
        MetricEvaluationPipeline()._validate_output_series(
            s=pd.Series(data=[100]*20, index=range(0, 20)),
            _output=pd.Series(data=[ValenceScore(0, '', '')]*20, index=range(10, 30))
        )


def test_metric_evaluation_pipeline_output_requires_valence_score_values():
    with pytest.raises(AssertionError):
        MetricEvaluationPipeline()._validate_output_series(
            s=pd.Series(data=[100]*20, index=range(0, 20)),
            _output=pd.Series(data=[0]*20, index=range(0, 20))
        )


def test_metric_evaluation_pipeline_output_requires_pandas_series():
    with pytest.raises(AssertionError):
        MetricEvaluationPipeline()._validate_output_series(
            s=pd.Series(data=[100]*20, index=range(0, 20)),
            _output=[0]*20
        )


def test_metric_evaluation_pipeline_missing_inputs():
    # TODO: Implement this once vs. target/forecast/reference is implemented
    pass
