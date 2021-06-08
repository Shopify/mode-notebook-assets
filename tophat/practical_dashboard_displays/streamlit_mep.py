import streamlit as st
import pandas as pd
import mode_notebook_assets.practical_dashboard_displays.plot.charts as charts
import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline as mep
from tophat.practical_dashboard_displays.common_data_for_tophat import INCREASING_SALES_TIME_SERIES

# Process metrics

fig = charts.TimeSeriesValenceLineChart(
    result=mep.MetricEvaluationPipeline().apply(
        s=INCREASING_SALES_TIME_SERIES
    ),
    title='Tophat time series with checks',
).to_plotly_figure()

# Layout

st.set_page_config(layout='wide')

st.title('Sales Monitoring Dashboard')

col1, col2, col3 = st.beta_columns(3)

col1.plotly_chart(fig, use_container_width=True)
col2.plotly_chart(fig, use_container_width=True)
col3.plotly_chart(fig, use_container_width=True)

e1 = st.beta_expander(label='Hidden Gotcha Panel')

with e1:
    st.markdown(
        '## Work in progress\n'
        'Scanning segments for issues not yet implemented in V2.'
    )

e2 = st.beta_expander(label='Raw Results')

with e2:
    st.dataframe(pd.DataFrame(INCREASING_SALES_TIME_SERIES))
