from importlib import reload

import streamlit as st

import mode_notebook_assets
import mode_notebook_assets.practical_dashboard_displays.plot as plot
from tophat.practical_dashboard_displays.common_data_for_tophat import get_segmented_metric_example_df

reload(mode_notebook_assets)

df = get_segmented_metric_example_df().round()

st.set_page_config(layout="wide")

st.title('Tophat SparklinesBySegmentDisplay')

col1, col2, col3 = st.beta_columns(3)

col1.plotly_chart(
    plot.SparklinesBySegmentDisplay(
        df=df,
        grouping_set=['Category 1'],
        index_column=['Day'],
        measure_column='Revenue',
        display_title='Segmented Sparkline Display',
        metadata_lookup={
            '1C': {'url': 'https://www.shopify.com'}
        }
    ).to_plotly_figure(),
    use_container_width=True,
)

col2.plotly_chart(
    plot.SparklinesBySegmentDisplay(
        df=df,
        grouping_set=['Category 2'],
        index_column=['Day'],
        measure_column='Revenue',
        display_title='Segmented Sparkline Display',
    ).to_plotly_figure(),
    use_container_width=True,
)

col3.plotly_chart(
    plot.SparklinesBySegmentDisplay(
        df=df,
        grouping_set=['Category 1', 'Category 2'],
        index_column=['Day'],
        measure_column='Revenue',
        display_title='Segmented Sparkline Display',
    ).to_plotly_figure(),
    use_container_width=True,
)
