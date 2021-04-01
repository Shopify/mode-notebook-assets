#%%

import pandas_gbq as pbq

project_id = "shopify-data-bigquery-global"


def test_query():
    return '''select * from scratch.practical_dashboards_data'''
df = pbq.read_gbq(test_query(), project_id=project_id)
# %%
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import MetricEvaluationPipeline
# %%
import pandas as pd
import numpy as np
import plotly as p
from dataclasses import dataclass
import plotly
import plotly.graph_objs as go

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools

# %%

@dataclass
class BuildTargetPlots:
    """
    Build 
    """
    actuals: pd.Series
    date_range: pd.Series
    targets: pd.Series
    metric_type: str = 'additive'



    def build_cumulative_tracking(df, metric_name, segment_type='overall', chart_type='line', value_type=''):
    
    actuals = select_data(df, metric_name, segment_type)
    targets = select_data(datasets['0 - Targets'].copy(), metric_name, segment_type)
    
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter({
        'mode': 'lines',
        'x': targets['target_period_start'],
        'y': targets['ytd_target'],
        'name': 'YTD Targets',
        'line': {
            'color': '#ffaa80',
        },
        'hoverinfo': 'name+x+y+text',
        }))
    
  fig1.add_trace(go.Scatter({
      'mode': 'lines',
      'x': actuals['snap_date'],
      'y': actuals['ytd_value'],
      'line': {
        'color': '#2d862d',
      },
      'name': 'YTD Actuals',
      'hoverinfo': 'name+x+y+text',
    }))
  
  fig2 = go.Figure()
  
  if chart_type == 'line':
    fig2.add_trace(go.Scatter({
        'mode': 'lines',
        'x': actuals['snap_date'],
        'y': actuals['yoy_value'],
        'name': 'Daily YOY',
        'hoverinfo': 'name+x+y+text',
        'line': {
          'color': '#80ccff',
        },
      }))
      
    fig2.add_trace(go.Scatter({
        'mode': 'lines',
        'x': actuals['snap_date'],
        'y': actuals['value'],
        'name': 'Daily Actuals',
        'line': {
          'color': '#005c99',
        },
        'hoverinfo': 'name+x+y+text',
      }))
  else:
    fig2.add_trace(go.Bar({
        'x': actuals['snap_date'],
        'y': actuals['yoy_value'],
        'name': 'Daily YOY',
        'marker_color': '#80ccff',
        'hoverinfo': 'name+x+y+text',
      }))
      
    fig2.add_trace(go.Bar({
        'x': actuals['snap_date'],
        'y': actuals['value'],
        'name': 'Daily Actuals',
        'marker_color': '#005c99',
        'hoverinfo': 'name+x+y+text',
      }))
    fig2.update_traces(marker_line_width=1, opacity=0.7)
    
      
  for i in range(len(fig1.data)):
    fig1.data[i].xaxis='x1'
    fig1.data[i].yaxis='y1'

  fig1.layout.xaxis1.update({'anchor': 'y1'})
  fig1.layout.yaxis1.update({'anchor': 'x1', 'domain': [.55, 1]})

  for i in range(len(fig2.data)):
      fig2.data[i].xaxis='x2'
      fig2.data[i].yaxis='y2'

  # initialize xaxis2 and yaxis2
  fig2['layout']['xaxis2'] = {}
  fig2['layout']['yaxis2'] = {}

  fig2.layout.xaxis2.update({'anchor': 'y2'})
  fig2.layout.yaxis2.update({'anchor': 'x2', 'domain': [0, .45]})

  sub_plot_layout = go.Layout({
    'showlegend': True,
    'height': 320,
    'width': 650,
    'title': {
      'text': metric_name.upper() + ' - ' + segment_type.upper(),
      'font': {"size": 14},
      'x':0.5,
      'y':0.99,
      'xanchor': 'center',
      'yanchor': 'top',
    },
    'xaxis': {
      'title_font': {"size": 10},
      'tickfont': {"size": 10},
    },
    'yaxis': {
      'tickmode': 'auto',
      #'title': metric_name.upper(),
      'ticksuffix': value_type,
      'title_font': {"size": 10},
      'tickfont': {"size": 10},
    },
    'xaxis2': {
      'title': 'Date',
      'title_font': {"size": 10},
      'tickfont': {"size": 10},
    },
    'yaxis2': {
      'tickmode': 'auto',
      #'title': metric_name.upper(),
      'ticksuffix': value_type,
      'title_font': {"size": 10},
      'tickfont': {"size": 10},
    },
    'legend': {
      'orientation': 'h',
      #'xanchor': 'right',
      #'yanchor': 'top',
      'bgcolor': 'rgba(0, 0, 0, 0)',
      'x':0.03,
      'y':0.99,
      'traceorder':'normal',
      'font' : {
          'size':8,
       },
    },
    'autosize': True,
    'margin': {'t':20, 'l':0, 'b':0,'r':0},
    'paper_bgcolor': '#FFF',
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
  })
  
  fig = go.Figure(layout=sub_plot_layout)
  fig.add_traces([fig1.data[0], fig1.data[1],fig2.data[0], fig2.data[1]])
  fig.layout.update(fig1.layout)
  fig.layout.update(fig2.layout)
  return fig