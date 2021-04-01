# %%
project_id = "shopify-data-bigquery-global"
import pandas_gbq as pbq
def test_query():
    return '''select * from scratch.practical_dashboards_data
    where metric = 'gmv' and segment = 'overall' and region = 'Canada'
    order by snap_date asc
    '''
df = pbq.read_gbq(test_query(), project_id=project_id)
df = df.set_index('snap_date')
# %%
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import MetricEvaluationPipeline
import pandas as pd
import numpy as np
import plotly as p
from dataclasses import dataclass
import plotly
import plotly.graph_objs as go

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools

# %%

def get_cumulative_values(s: pd.Series):
    return s.cumsum()

@dataclass
class BuildTargetPlots():
    """
    Build 
    """
    actuals: pd.Series
    date_range: pd.Series

    targets: pd.Series = None
    actuals_yoy: pd.Series = None
   
    metric_type: str = 'additive'

    def build_cumulative_tracking(self):

        fig = go.Figure()

        actuals_ytd = self.actuals.cumsum()

        fig.add_trace(go.Scatter({
            'mode': 'lines',
            'x': self.date_range,
            'y': actuals_ytd,
            'line': {
                'color': '#2d862d',
            },
            'name': 'YTD Actuals',
            'hoverinfo': 'name+x+y+text',
            }))

        if self.targets is not None:
            targets_ytd = self.targets.cumsum()

            fig.add_trace(go.Scatter({
                'mode': 'lines',
                'x': self.date_range,
                'y': targets_ytd,
                'name': 'YTD Targets',
                'line': {
                    'color': '#ffaa80',
                },
                'hoverinfo': 'name+x+y+text',
                }))
        
        return fig

    def build_yoy_tracking(self, chart_type: str = 'line'):
        
        fig = go.Figure()

        if chart_type == 'line':

            fig.add_trace(go.Scatter({
                'mode': 'lines',
                'x': self.date_range,
                'y': self.actuals_yoy,
                'name': 'Daily YOY',
                'hoverinfo': 'name+x+y+text',
                'line': {
                'color': '#80ccff',
                },
            }))
      
            fig.add_trace(go.Scatter({
                'mode': 'lines',
                'x': self.date_range,
                'y': self.actuals,
                'name': 'Daily Actuals',
                'line': {
                'color': '#005c99',
                },
                'hoverinfo': 'name+x+y+text',
            }))
        else:
            
            fig.add_trace(go.Bar({
                'x': self.date_range,
                'y': self.actuals_yoy,
                'name': 'Daily YOY',
                'marker_color': '#80ccff',
                'hoverinfo': 'name+x+y+text',
            }))
            
            fig.add_trace(go.Bar({
                'x': self.date_range,
                'y': self.actuals,
                'name': 'Daily Actuals',
                'marker_color': '#005c99',
                'hoverinfo': 'name+x+y+text',
            }))
    
            fig2.update_traces(marker_line_width=1, opacity=0.7)
        
        return fig

# %%
if __name__ == "__name__":
    import pandas_gbq as pbq
    project_id = "shopify-data-bigquery-global"

    def test_query():
        return '''select * from scratch.practical_dashboards_data
        where metric = 'gmv' and segment = 'overall' and region = 'Canada'
        order by snap_date asc
        '''

    df = pbq.read_gbq(test_query(), project_id=project_id)

    BuildTargetPlots(actuals=df.value, date_range=df.index, targets=df.target).build_cumulative_tracking()
    
    BuildTargetPlots(actuals=df.value, date_range=df.index, actuals_yoy=df.value_yoy).build_yoy_tracking()

    MetricEvaluationPipeline(
        s=df['value'],
        ).display_actionability_time_series(
        title='Canada GMV',
        return_html=False
    )
# %%
