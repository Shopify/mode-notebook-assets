from importlib import reload

import streamlit as st

import pandas as pd
import numpy as np

import mode_notebook_assets.practical_dashboard_displays.plot.display_grid as dg
import mode_notebook_assets.practical_dashboard_displays.plot.charts as charts
import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline as mep
import mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration as pc

reload(pc)
reload(dg)
reload(mep)
reload(charts)

DATE_RANGE = pd.date_range('2020-01-01', periods=20, freq='M')

SERIES_3 = pd.Series(
    data=[89, 86, 88, 84, 65, 90, 89, 120, 88, 84, 85, 89, 90, 89, 120, 88, 84, 85, 89, 60],
    index=DATE_RANGE,
)

SERIES_2 = pd.Series(
    data=[89, 86, 88, 89, 86, 88, 89, 86, 88, 89, 84, 85, 89, 89, 86, 88, 84, 85, 89, 70],
    index=DATE_RANGE,
)

SERIES_1 = pd.Series(
    data=[89, 86, 88, 84, 85, 89, 89, 86, 86, 88, 86, 88, 89, 89, 86, 88, 84, 85, 89, 100],
    index=DATE_RANGE,
)

RANDOM_TIME_SERIES_10 = [pd.Series(
    data=np.round(np.random.rand(20, 1) * 10 + 25).ravel(),
    index=DATE_RANGE,
) for _ in range(0, 10)]

METRIC_EVALUATION_RESULTS_LIST = [
    mep.MetricEvaluationPipeline().apply(
        s=SERIES_1
    ).add_metadata(
        name='Increasing Sales'
    ),
    mep.MetricEvaluationPipeline().apply(
        s=SERIES_2
    ).add_metadata(
        name='Increasing Sales',
        url='https://www.shopify.com'
    ),
    mep.MetricEvaluationPipeline().apply(
        s=SERIES_3
    ),
    mep.MetricEvaluationPipeline().apply(
        s=RANDOM_TIME_SERIES_10[0],
    ),
    mep.MetricEvaluationPipeline(
        append_to_metric_checks=[mep.checks.AnnotateAndSnoozeMetricCheck()]
    ).apply(
        s=RANDOM_TIME_SERIES_10[1],
        annotations=pd.Series(
            ['This result is normal and is overridden by the user.'],
            index=[DATE_RANGE[-1]],
        )
    ),
    mep.MetricEvaluationPipeline().apply(
        s=RANDOM_TIME_SERIES_10[2],
    ),
]

time_series_display_1 = charts.TimeSeriesValenceLineChart(
    result=METRIC_EVALUATION_RESULTS_LIST[0],
    title='Product Sales Valence Chart'
)

time_series_display_2 = charts.TimeSeriesValenceLineChart(
    result=METRIC_EVALUATION_RESULTS_LIST[2],
    title='Division Revenue Valence Chart'
)

time_series_display_3 = charts.TimeSeriesValenceLineChart(
    result=METRIC_EVALUATION_RESULTS_LIST[4],
    title='Bookings with Annotations'
)

grid_display = dg.GridDisplay(
    title='Grid Valence Display',
    results=METRIC_EVALUATION_RESULTS_LIST,
    column_schema=[
        dg.ValenceDot(horizontal_units=1),
        dg.ResultName(horizontal_units=3),
        dg.MostRecentPeriodValue(horizontal_units=1),
        dg.MostRecentPeriodBarHorizontal(horizontal_units=1),
        dg.Sparkline(horizontal_units=4),
    ],
    config=pc.PlotConfiguration(),
)

st.set_page_config(layout="wide")

st.title('Valence Dashboard Demo')

col1, col2, col3 = st.beta_columns(3)
col1.plotly_chart(time_series_display_1.to_plotly_figure().update_layout({'height': 300}), use_container_width=True)
col2.plotly_chart(time_series_display_2.to_plotly_figure().update_layout({'height': 300}), use_container_width=True)
col3.plotly_chart(time_series_display_3.to_plotly_figure().update_layout({'height': 300}), use_container_width=True)

col4, col5, col6, col7 = st.beta_columns(4)
col4.plotly_chart(grid_display.to_plotly_figure(), use_container_width=True)
col5.plotly_chart(grid_display.to_plotly_figure(), use_container_width=True)
col6.plotly_chart(grid_display.to_plotly_figure(), use_container_width=True)
col7.plotly_chart(grid_display.to_plotly_figure(), use_container_width=True)
