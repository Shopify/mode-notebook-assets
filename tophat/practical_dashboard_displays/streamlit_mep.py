from random import random
import datetime

import streamlit as st
import pandas as pd
import mode_notebook_assets.practical_dashboard_displays as pdd

# Create datasets
_ts_path = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/shampoo.csv'
_ts = pd.read_csv(_ts_path) \
    .set_index('Month')['Sales'].round()

_category_1 = [f'1{char}' for char in 'ABC']
_category_2 = [f'2{char}' for char in 'XYZ']
_t = [datetime.datetime(2020,1,1) + datetime.timedelta(days=x) for x in range(0,25)]

rows = []
for t in _t:
    for c1 in _category_1:
        for c2 in _category_2:
            rows.append({
                'Day': t,
                'Category 1': c1,
                'Category 2': c2,
                'Revenue': 50 + hash(c1) % 10 + (hash(c2) % 2 * _t.index(t)/4) + 10*random(),
            })

_df = pd.DataFrame.from_records(rows)

# Process metrics

mep = pdd.LegacyMetricEvaluationPipeline(
    _ts,
)

fig = mep.display_actionability_time_series(
    title='Tophat time series with checks',
    metric_name='Sales',
    return_html=False,
)

# Layout

st.title('Sales Monitoring Dashboard')

st.plotly_chart(fig)

e1 = st.beta_expander(label='Hidden Gotcha Panel')

with e1:
    st.markdown(
        pdd.make_metric_segmentation_grid_display(
            df=_df,
            index_column='Day',
            measure_column='Revenue',
            spec=[
                ('Category 1', 'First Category'),
                ('Category 2', 'Second Category'),
                ('Category 1', 'First Category Repeated'),
            ]
        ),
        unsafe_allow_html=True,
    )

e2 = st.beta_expander(label='Raw Results')

with e2:
    st.dataframe(mep.results)