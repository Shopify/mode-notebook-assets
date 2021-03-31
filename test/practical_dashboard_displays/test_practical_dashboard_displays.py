import pytest
import pandas as pd
import mode_notebook_assets.practical_dashboard_displays as pdd

# read test series
import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline

_ts = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv').set_index('Month')['Sales']


def test_disable_steady_state():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_change_in_steady_state_long=False
    ).display_actionability_time_series()


def test_disable_normal_range():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_outside_of_normal_range=False
    ).display_actionability_time_series()


def test_disable_sudden_change():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_sudden_change=False
    ).display_actionability_time_series()


def test_disable_multiple_statistics():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_change_in_steady_state_long=False,
        check_sudden_change=False
    ).display_actionability_time_series()


def test_disable_all_actionability_checks():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_outside_of_normal_range=False,
        check_change_in_steady_state_long=False,
        check_sudden_change=False
    ).display_actionability_time_series()


def test_get_current_actionability_score_no_checks():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
        check_outside_of_normal_range=False,
        check_change_in_steady_state_long=False,
        check_sudden_change=False
    ).get_current_actionability_status() == 0


def test_get_current_actionability_score():
    assert mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline.MetricEvaluationPipeline(
        _ts,
    ).get_current_actionability_status()


pytest.main()