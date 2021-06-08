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

st.title('Sales Monitoring Dashboard')

st.plotly_chart(fig)

e1 = st.beta_expander(label='Hidden Gotcha Panel')

with e1:
    st.markdown(
        '## Work in progress\n'
        'Scanning segments for issues not yet implemented in V2.'
    )

e2 = st.beta_expander(label='Raw Results')

with e2:
    st.dataframe(pd.DataFrame(INCREASING_SALES_TIME_SERIES))
