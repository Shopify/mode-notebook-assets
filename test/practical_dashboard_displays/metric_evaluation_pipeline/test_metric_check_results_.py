from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_check_results import \
    MetricCheckResult


def test_init_metric_check_result():
    assert MetricCheckResult(
        valence_score=0,
        priority_score=3,
        is_override=False,
        is_ambiguous=False,
    )