import json
from importlib import reload

import streamlit as st

import pandas as pd

import plotly.io as pio

import mode_notebook_assets.practical_dashboard_displays.plot.display_grid as dg
import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline as mep
import mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration as pc
from tophat.practical_dashboard_displays.common_data_for_tophat import INCREASING_SALES_TIME_SERIES, \
    AMBIGUOUS_TIME_SERIES, STABILIZING_SALES_TIME_SERIES

SERIES_3 = pd.Series(
    data=[89, 86, 88, 84, 65, 90, 89, 120, 88, 84, 85, 89, 90, 89, 120, 88, 84, 85, 89, 60],
    index=pd.date_range('2020-01-01', periods=20, freq='M'),
)

SERIES_2 = pd.Series(
    data=[89, 86, 88, 89, 86, 88, 89, 86, 88, 89, 86, 88, 89, 84, 85, 89, 89, 86, 88, 84, 85, 89, 70],
    index=pd.date_range('2020-01-01', periods=23, freq='M'),
)

SERIES_1 = pd.Series(
    data=[89, 86, 88, 84, 85, 89, 89, 86, 88, 89, 89, 86, 88, 86, 88, 89, 89, 86, 88, 84, 85, 89, 100],
    index=pd.date_range('2020-01-01', periods=23, freq='M'),
)

reload(pc)
reload(dg)
reload(mep)

grid_display = dg.GridDisplay(
    title='Grid Valence Display',
    results=[
        mep.MetricEvaluationPipeline().apply(
            s=SERIES_1
        ).add_metadata(name='Increasing Sales'),
        mep.MetricEvaluationPipeline().apply(
            s=SERIES_2
        ).add_metadata(name='Increasing Sales', url='https://www.shopify.com'),
        mep.MetricEvaluationPipeline().apply(
            s=SERIES_3
        ),
    ],
    column_schema=[
        dg.ValenceDot(horizontal_units=1),
        dg.ResultName(horizontal_units=2),
        dg.MostRecentPeriodValue(horizontal_units=1),
        dg.MostRecentPeriodBarHorizontal(horizontal_units=1),
        dg.Sparkline(horizontal_units=4),
    ],
    config=pc.PlotConfiguration(),
)

st.plotly_chart(grid_display.to_plotly_figure())