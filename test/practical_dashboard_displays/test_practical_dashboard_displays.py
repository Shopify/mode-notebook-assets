import pytest
import pandas as pd
import mode_notebook_assets.practical_dashboard_displays as pdd

# read test series
_ts = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv').set_index('Month')['Sales']


def test_disable_steady_state():
    assert pdd.MetricEvaluationPipeline(
        _ts,
        check_change_in_steady_state_long=False
    ).display_actionability_time_series()


def test_disable_normal_range():
    assert pdd.MetricEvaluationPipeline(
        _ts,
        check_outside_of_normal_range=False
    ).display_actionability_time_series()


def test_disable_sudden_change():
    assert pdd.MetricEvaluationPipeline(
        _ts,
        check_sudden_change=False
    ).display_actionability_time_series()


def test_disable_multiple_statistics():
    assert pdd.MetricEvaluationPipeline(
        _ts,
        check_change_in_steady_state_long=False,
        check_sudden_change=False
    ).display_actionability_time_series()


pytest.main()