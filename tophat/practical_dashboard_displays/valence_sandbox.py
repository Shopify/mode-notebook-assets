import json
from importlib import reload

import streamlit

import plotly.io as pio

import mode_notebook_assets.practical_dashboard_displays.plot.display_grid as dg
import mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline as mep
import mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration as pc
from tophat.practical_dashboard_displays.common_data_for_tophat import INCREASING_SALES_TIME_SERIES, \
    AMBIGUOUS_TIME_SERIES, STABILIZING_SALES_TIME_SERIES

reload(pc)
reload(dg)
reload(mep)

grid_display = dg.GridDisplay(
    title='Grid Valence Display',
    results=[
        mep.MetricEvaluationPipeline().apply(
            s=INCREASING_SALES_TIME_SERIES
        ).add_metadata(name='Increasing Sales'),
        mep.MetricEvaluationPipeline().apply(
            s=INCREASING_SALES_TIME_SERIES
        ).add_metadata(name='Increasing Sales', url='https://www.shopify.com'),
        mep.MetricEvaluationPipeline().apply(
            s=INCREASING_SALES_TIME_SERIES
        ),
    ],
    column_schema=[
        dg.ValenceDot(horizontal_units=1),
        dg.ResultName(horizontal_units=2),
        dg.MostRecentPeriodValue(horizontal_units=2),
        dg.Sparkline(horizontal_units=4),
    ],
    config=pc.PlotConfiguration(),
)

streamlit.plotly_chart(grid_display.to_plotly_figure())

from plotly.graph_objs import *

trace1 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x1",
    "yaxis":   "y1",
    "visible": False
}
trace2 = {
    "type":        "bar",
    "x":           [6.4],
    "y":           [0],
    "xaxis":       "x2",
    "yaxis":       "y2",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace3 = {
    "type":        "bar",
    "x":           [12],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x2",
    "yaxis":       "y2",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace4 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [17],
    "y":      [0],
    "xaxis":  "x2",
    "yaxis":  "y2",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace5 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [5, 6, 4, 8, 2, 7, 2, 1, 17, 12],
    "xaxis":  "x3",
    "yaxis":  "y3",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace6 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x4",
    "yaxis":   "y4",
    "visible": False
}
trace7 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [5, 6, 4, 8, 2, 7, 2, 1, 17, 12],
    "xaxis":  "x5",
    "yaxis":  "y5",
    "marker": {"color": "rgb(0,210,0)"}
}
trace8 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [12],
    "xaxis":  "x5",
    "yaxis":  "y5",
    "marker": {"color": "rgb(0,0,255)"}
}
trace9 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x6",
    "yaxis":   "y6",
    "visible": False
}
trace10 = {
    "type":        "bar",
    "x":           [5.7],
    "y":           [0],
    "xaxis":       "x7",
    "yaxis":       "y7",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace11 = {
    "type":        "bar",
    "x":           [8],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x7",
    "yaxis":       "y7",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace12 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [10],
    "y":      [0],
    "xaxis":  "x7",
    "yaxis":  "y7",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace13 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [2, 5, 7, 8, 9, 10, 4, 1, 3, 8],
    "xaxis":  "x8",
    "yaxis":  "y8",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace14 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x9",
    "yaxis":   "y9",
    "visible": False
}
trace15 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [2, 5, 7, 8, 9, 10, 4, 1, 3, 8],
    "xaxis":  "x10",
    "yaxis":  "y10",
    "marker": {"color": "rgb(0,210,0)"}
}
trace16 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [8],
    "xaxis":  "x10",
    "yaxis":  "y10",
    "marker": {"color": "rgb(0,0,255)"}
}
trace17 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x11",
    "yaxis":   "y11",
    "visible": False
}
trace18 = {
    "type":        "bar",
    "x":           [4.8],
    "y":           [0],
    "xaxis":       "x12",
    "yaxis":       "y12",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace19 = {
    "type":        "bar",
    "x":           [8],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x12",
    "yaxis":       "y12",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace20 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [0],
    "xaxis":  "x12",
    "yaxis":  "y12",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace21 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [9, 4, 6, 3, 5, 1, 5, 2, 5, 8],
    "xaxis":  "x13",
    "yaxis":  "y13",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace22 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x14",
    "yaxis":   "y14",
    "visible": False
}
trace23 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [9, 4, 6, 3, 5, 1, 5, 2, 5, 8],
    "xaxis":  "x15",
    "yaxis":  "y15",
    "marker": {"color": "rgb(0,210,0)"}
}
trace24 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [8],
    "xaxis":  "x15",
    "yaxis":  "y15",
    "marker": {"color": "rgb(0,0,255)"}
}
trace25 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x16",
    "yaxis":   "y16",
    "visible": False
}
trace26 = {
    "type":        "bar",
    "x":           [4.3],
    "y":           [0],
    "xaxis":       "x17",
    "yaxis":       "y17",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace27 = {
    "type":        "bar",
    "x":           [6],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x17",
    "yaxis":       "y17",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace28 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [8],
    "y":      [0],
    "xaxis":  "x17",
    "yaxis":  "y17",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace29 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [6, 5, 7, 3, 1, 4, 8, 2, 1, 6],
    "xaxis":  "x18",
    "yaxis":  "y18",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace30 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x19",
    "yaxis":   "y19",
    "visible": False
}
trace31 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [6, 5, 7, 3, 1, 4, 8, 2, 1, 6],
    "xaxis":  "x20",
    "yaxis":  "y20",
    "marker": {"color": "rgb(0,210,0)"}
}
trace32 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [6],
    "xaxis":  "x20",
    "yaxis":  "y20",
    "marker": {"color": "rgb(0,0,255)"}
}
trace33 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x21",
    "yaxis":   "y21",
    "visible": False
}
trace34 = {
    "type":        "bar",
    "x":           [7.0],
    "y":           [0],
    "xaxis":       "x22",
    "yaxis":       "y22",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace35 = {
    "type":        "bar",
    "x":           [4],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x22",
    "yaxis":       "y22",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace36 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [13],
    "y":      [0],
    "xaxis":  "x22",
    "yaxis":  "y22",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace37 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [2, 1, 6, 3, 11, 7, 13, 12, 11, 4],
    "xaxis":  "x23",
    "yaxis":  "y23",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace38 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x24",
    "yaxis":   "y24",
    "visible": False
}
trace39 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [2, 1, 6, 3, 11, 7, 13, 12, 11, 4],
    "xaxis":  "x25",
    "yaxis":  "y25",
    "marker": {"color": "rgb(0,210,0)"}
}
trace40 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [4],
    "xaxis":  "x25",
    "yaxis":  "y25",
    "marker": {"color": "rgb(0,0,255)"}
}
trace41 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x26",
    "yaxis":   "y26",
    "visible": False
}
trace42 = {
    "type":        "bar",
    "x":           [7.7],
    "y":           [0],
    "xaxis":       "x27",
    "yaxis":       "y27",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace43 = {
    "type":        "bar",
    "x":           [14],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x27",
    "yaxis":       "y27",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace44 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [14],
    "y":      [0],
    "xaxis":  "x27",
    "yaxis":  "y27",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace45 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [3, 4, 5, 2, 12, 8, 14, 5, 10, 14],
    "xaxis":  "x28",
    "yaxis":  "y28",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace46 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x29",
    "yaxis":   "y29",
    "visible": False
}
trace47 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [3, 4, 5, 2, 12, 8, 14, 5, 10, 14],
    "xaxis":  "x30",
    "yaxis":  "y30",
    "marker": {"color": "rgb(0,210,0)"}
}
trace48 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [14],
    "xaxis":  "x30",
    "yaxis":  "y30",
    "marker": {"color": "rgb(0,0,255)"}
}
trace49 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x31",
    "yaxis":   "y31",
    "visible": False
}
trace50 = {
    "type":        "bar",
    "x":           [6.7],
    "y":           [0],
    "xaxis":       "x32",
    "yaxis":       "y32",
    "marker":      {"color": "rgb(0,210,0)"},
    "orientation": "h"
}
trace51 = {
    "type":        "bar",
    "x":           [5],
    "y":           [0],
    "width":       0.2,
    "xaxis":       "x32",
    "yaxis":       "y32",
    "marker":      {"color": "rgb(0,0,255)"},
    "offset":      -0.1,
    "orientation": "h"
}
trace52 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [12],
    "y":      [0],
    "xaxis":  "x32",
    "yaxis":  "y32",
    "marker": {
        "size":   9,
        "color":  "rgb(0,210,0)",
        "symbol": "diamond-tall"
    }
}
trace53 = {
    "type":   "bar",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [4, 6, 8, 8, 10, 12, 2, 7, 5, 5],
    "xaxis":  "x33",
    "yaxis":  "y33",
    "marker": {"color": ["rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)",
                         "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,210,0)", "rgb(0,0,255)"]}
}
trace54 = {
    "type":    "bar",
    "x":       [0],
    "y":       [0],
    "xaxis":   "x34",
    "yaxis":   "y34",
    "visible": False
}
trace55 = {
    "mode":   "lines",
    "type":   "scatter",
    "x":      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "y":      [4, 6, 8, 8, 10, 12, 2, 7, 5, 5],
    "xaxis":  "x35",
    "yaxis":  "y35",
    "marker": {"color": "rgb(0,210,0)"}
}
trace56 = {
    "mode":   "markers",
    "type":   "scatter",
    "x":      [9],
    "y":      [5],
    "xaxis":  "x35",
    "yaxis":  "y35",
    "marker": {"color": "rgb(0,0,255)"}
}
data = Data([trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13,
             trace14, trace15, trace16, trace17, trace18, trace19, trace20, trace21, trace22, trace23, trace24, trace25,
             trace26, trace27, trace28, trace29, trace30, trace31, trace32, trace33, trace34, trace35, trace36, trace37,
             trace38, trace39, trace40, trace41, trace42, trace43, trace44, trace45, trace46, trace47, trace48, trace49,
             trace50, trace51, trace52, trace53, trace54, trace55, trace56])
layout = {
    "title":       "Sparkline Chart",
    "xaxis1":      {
        "range":          [0, 1],
        "anchor":         "y1",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis2":      {
        "anchor":         "y2",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis3":      {
        "anchor":         "y3",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis4":      {
        "range":          [0, 1],
        "anchor":         "y4",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis5":      {
        "anchor":         "y5",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis6":      {
        "range":          [0, 1],
        "anchor":         "y6",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis7":      {
        "anchor":         "y7",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis8":      {
        "anchor":         "y8",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis9":      {
        "range":          [0, 1],
        "anchor":         "y9",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis1":      {
        "range":          [0, 1],
        "anchor":         "x1",
        "domain":         [0.857142857142857, 0.9999999999999998],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis2":      {
        "anchor":         "x2",
        "domain":         [0.857142857142857, 0.9999999999999998],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis3":      {
        "anchor":         "x3",
        "domain":         [0.857142857142857, 0.9999999999999998],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis4":      {
        "range":          [0, 1],
        "anchor":         "x4",
        "domain":         [0.857142857142857, 0.9999999999999998],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis5":      {
        "anchor":         "x5",
        "domain":         [0.857142857142857, 0.9999999999999998],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis6":      {
        "range":          [0, 1],
        "anchor":         "x6",
        "domain":         [0.7142857142857142, 0.857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis7":      {
        "anchor":         "x7",
        "domain":         [0.7142857142857142, 0.857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis8":      {
        "anchor":         "x8",
        "domain":         [0.7142857142857142, 0.857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis9":      {
        "range":          [0, 1],
        "anchor":         "x9",
        "domain":         [0.7142857142857142, 0.857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis10":     {
        "anchor":         "y10",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis11":     {
        "range":          [0, 1],
        "anchor":         "y11",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis12":     {
        "anchor":         "y12",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis13":     {
        "anchor":         "y13",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis14":     {
        "range":          [0, 1],
        "anchor":         "y14",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis15":     {
        "anchor":         "y15",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis16":     {
        "range":          [0, 1],
        "anchor":         "y16",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis17":     {
        "anchor":         "y17",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis18":     {
        "anchor":         "y18",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis19":     {
        "range":          [0, 1],
        "anchor":         "y19",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis20":     {
        "anchor":         "y20",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis21":     {
        "range":          [0, 1],
        "anchor":         "y21",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis22":     {
        "anchor":         "y22",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis23":     {
        "anchor":         "y23",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis24":     {
        "range":          [0, 1],
        "anchor":         "y24",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis25":     {
        "anchor":         "y25",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis26":     {
        "range":          [0, 1],
        "anchor":         "y26",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis27":     {
        "anchor":         "y27",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis28":     {
        "anchor":         "y28",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis29":     {
        "range":          [0, 1],
        "anchor":         "y29",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis30":     {
        "anchor":         "y30",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis31":     {
        "range":          [0, 1],
        "anchor":         "y31",
        "domain":         [0.0, 0.09090909090909091],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis32":     {
        "anchor":         "y32",
        "domain":         [0.09090909090909091, 0.36363636363636365],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis33":     {
        "anchor":         "y33",
        "domain":         [0.36363636363636365, 0.6363636363636364],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis34":     {
        "range":          [0, 1],
        "anchor":         "y34",
        "domain":         [0.6363636363636364, 0.7272727272727273],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "xaxis35":     {
        "anchor":         "y35",
        "domain":         [0.7272727272727273, 1.0],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis10":     {
        "anchor":         "x10",
        "domain":         [0.7142857142857142, 0.857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis11":     {
        "range":          [0, 1],
        "anchor":         "x11",
        "domain":         [0.5714285714285714, 0.7142857142857142],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis12":     {
        "anchor":         "x12",
        "domain":         [0.5714285714285714, 0.7142857142857142],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis13":     {
        "anchor":         "x13",
        "domain":         [0.5714285714285714, 0.7142857142857142],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis14":     {
        "range":          [0, 1],
        "anchor":         "x14",
        "domain":         [0.5714285714285714, 0.7142857142857142],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis15":     {
        "anchor":         "x15",
        "domain":         [0.5714285714285714, 0.7142857142857142],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis16":     {
        "range":          [0, 1],
        "anchor":         "x16",
        "domain":         [0.42857142857142855, 0.5714285714285714],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis17":     {
        "anchor":         "x17",
        "domain":         [0.42857142857142855, 0.5714285714285714],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis18":     {
        "anchor":         "x18",
        "domain":         [0.42857142857142855, 0.5714285714285714],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis19":     {
        "range":          [0, 1],
        "anchor":         "x19",
        "domain":         [0.42857142857142855, 0.5714285714285714],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis20":     {
        "anchor":         "x20",
        "domain":         [0.42857142857142855, 0.5714285714285714],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis21":     {
        "range":          [0, 1],
        "anchor":         "x21",
        "domain":         [0.2857142857142857, 0.42857142857142855],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis22":     {
        "anchor":         "x22",
        "domain":         [0.2857142857142857, 0.42857142857142855],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis23":     {
        "anchor":         "x23",
        "domain":         [0.2857142857142857, 0.42857142857142855],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis24":     {
        "range":          [0, 1],
        "anchor":         "x24",
        "domain":         [0.2857142857142857, 0.42857142857142855],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis25":     {
        "anchor":         "x25",
        "domain":         [0.2857142857142857, 0.42857142857142855],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis26":     {
        "range":          [0, 1],
        "anchor":         "x26",
        "domain":         [0.14285714285714285, 0.2857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis27":     {
        "anchor":         "x27",
        "domain":         [0.14285714285714285, 0.2857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis28":     {
        "anchor":         "x28",
        "domain":         [0.14285714285714285, 0.2857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis29":     {
        "range":          [0, 1],
        "anchor":         "x29",
        "domain":         [0.14285714285714285, 0.2857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis30":     {
        "anchor":         "x30",
        "domain":         [0.14285714285714285, 0.2857142857142857],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis31":     {
        "range":          [0, 1],
        "anchor":         "x31",
        "domain":         [0.0, 0.14285714285714285],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis32":     {
        "anchor":         "x32",
        "domain":         [0.0, 0.14285714285714285],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis33":     {
        "anchor":         "x33",
        "domain":         [0.0, 0.14285714285714285],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis34":     {
        "range":          [0, 1],
        "anchor":         "x34",
        "domain":         [0.0, 0.14285714285714285],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "yaxis35":     {
        "anchor":         "x35",
        "domain":         [0.0, 0.14285714285714285],
        "showgrid":       False,
        "zeroline":       False,
        "showticklabels": False
    },
    "showlegend":  False,
    "annotations": [
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "adam",
            "xref":      "x1",
            "yref":      "y1",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "6.4",
            "xref":      "x4",
            "yref":      "y4",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "andrew",
            "xref":      "x6",
            "yref":      "y6",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "5.7",
            "xref":      "x9",
            "yref":      "y9",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "michael",
            "xref":      "x11",
            "yref":      "y11",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "4.8",
            "xref":      "x14",
            "yref":      "y14",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "chris",
            "xref":      "x16",
            "yref":      "y16",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "4.3",
            "xref":      "x19",
            "yref":      "y19",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "jack",
            "xref":      "x21",
            "yref":      "y21",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "7.0",
            "xref":      "x24",
            "yref":      "y24",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "robin",
            "xref":      "x26",
            "yref":      "y26",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "7.7",
            "xref":      "x29",
            "yref":      "y29",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "alex",
            "xref":      "x31",
            "yref":      "y31",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         1,
            "y":         0.5,
            "font":      {"size": 15},
            "text":      "6.7",
            "xref":      "x34",
            "yref":      "y34",
            "xanchor":   "right",
            "showarrow": False
        },
        {
            "x":         0.045454545454545456,
            "y":         1.03,
            "font":      {
                "size":  13,
                "color": "#0f0f0f"
            },
            "text":      "name",
            "xref":      "paper",
            "yref":      "paper",
            "xanchor":   "center",
            "yanchor":   "middle",
            "showarrow": False,
            "textangle": 0
        },
        {
            "x":         0.22727272727272727,
            "y":         1.03,
            "font":      {
                "size":  13,
                "color": "#0f0f0f"
            },
            "text":      "bullet",
            "xref":      "paper",
            "yref":      "paper",
            "xanchor":   "center",
            "yanchor":   "middle",
            "showarrow": False,
            "textangle": 0
        },
        {
            "x":         0.5,
            "y":         1.03,
            "font":      {
                "size":  13,
                "color": "#0f0f0f"
            },
            "text":      "bar",
            "xref":      "paper",
            "yref":      "paper",
            "xanchor":   "center",
            "yanchor":   "middle",
            "showarrow": False,
            "textangle": 0
        },
        {
            "x":         0.6818181818181818,
            "y":         1.03,
            "font":      {
                "size":  13,
                "color": "#0f0f0f"
            },
            "text":      "avg",
            "xref":      "paper",
            "yref":      "paper",
            "xanchor":   "center",
            "yanchor":   "middle",
            "showarrow": False,
            "textangle": 0
        },
        {
            "x":         0.8636363636363636,
            "y":         1.03,
            "font":      {
                "size":  13,
                "color": "#0f0f0f"
            },
            "text":      "line",
            "xref":      "paper",
            "yref":      "paper",
            "xanchor":   "center",
            "yanchor":   "middle",
            "showarrow": False,
            "textangle": 0
        }
    ]
}
fig = Figure(data=data, layout=layout)
streamlit.plotly_chart(fig)
