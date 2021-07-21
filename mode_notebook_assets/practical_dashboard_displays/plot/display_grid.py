from dataclasses import dataclass
from typing import List

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from IPython.core.display import HTML

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration import PlotConfiguration


@dataclass
class PlotlyTraceGridColumnSpec(object):
    horizontal_units: int  # scale-less; use for ratio

    def add_content_to_grid(self, grid: go.Figure) -> go.Figure:
        pass


class Text(PlotlyTraceGridColumnSpec):
    pass


class Number(PlotlyTraceGridColumnSpec):
    pass


class ValenceDot(PlotlyTraceGridColumnSpec):
    pass


class Sparkline(PlotlyTraceGridColumnSpec):
    pass


class BarChartColumn(PlotlyTraceGridColumnSpec):
    pass


@dataclass
class GridDisplay(object):
    results: List[MetricEvaluationResult]
    title: str
    column_schema: List[PlotlyTraceGridColumnSpec]
    config: PlotConfiguration

    def __post_init__(self):
        self._n_cols = len(self.column_schema)
        self._n_rows = len(self.results)

    def _generate_figure_layout(self):
        _column_unit_widths = [column.horizontal_units for column in self.column_schema]
        _column_unit_breakpoints = np.cumsum(_column_unit_widths)
        _column_normalized_breakpoints = _column_unit_breakpoints / np.sum(_column_unit_widths)
        _row_normalized_breakpoints = np.flip((np.arange(len(self.results)) + 1)) / (len(self.results))

        _layout = go.Layout(title=self.title)

        for column_index in range(0, self._n_cols):
            column_display_index = str(column_index + 1)
            for row_index in range(0, self._n_rows):
                row_display_index = str(row_index + 1)
                _axis_number = row_index * self._n_cols + column_index + 1
                _xaxis_name = f'xaxis{_axis_number}'
                _yaxis_name = f'yaxis{_axis_number}'
                _layout.update(
                    dict1={
                        f'xaxis{_axis_number}': {
                            'range':          [0, 1],
                            'anchor':         f'y{_axis_number}',
                            'domain':         [
                                # left domain value
                                0 if column_index == 0 else _column_normalized_breakpoints[column_index - 1],
                                # right domain value
                                _column_normalized_breakpoints[column_index]
                            ],
                            'showgrid':       False,
                            'zeroline':       False,
                            'showticklabels': False
                        },
                        f'yaxis{_axis_number}': {
                            'range':          [0, 1],
                            'anchor':         f'x{_axis_number}',
                            'domain':         [
                                # lower domain value
                                0 if row_index == self._n_rows-1 else _row_normalized_breakpoints[row_index + 1],
                                # upper domain value
                                _row_normalized_breakpoints[row_index],
                            ],
                            'showgrid':       False,
                            'zeroline':       False,
                            'showticklabels': False,
                        },
                    }
                )

        return _layout

    def _create_figure_from_layout(self, layout: go.Layout) -> go.Figure:
        # Temporary data
        return go.Figure(
            data=[{
                'type':    'bar',
                'x':       [0],
                'y':       [0],
                'xaxis':   f'x{i}',
                'yaxis':   f'y{i}',
                'visible': False
            } for i in range(1, self._n_cols * self._n_rows + 1)],
            layout=layout.update(dict1={'annotations': [
                {
                    'x':         1,
                    'y':         0.5,
                    'font':      {'size': 15},
                    'text':      str(i),
                    'xref':      f'x{i}',
                    'yref':      f'y{i}',
                    'xanchor':   'right',
                    'showarrow': False
                } for i in range(1, self._n_cols * self._n_rows + 1)
            ]})
        )

    def to_html(self) -> HTML:
        return HTML(self.to_plotly_figure().to_html())

    def to_plotly_figure(self) -> go.Figure:
        return self._create_figure_from_layout(
            layout=self._generate_figure_layout()
        )


@dataclass
class SparklineGridDisplay(GridDisplay):
    """
    Subclass for specific presets.
    Use properties?
    """
    column_schema = [
        # Text(horizontal_units=1),
        # Number(show_bar=True, horizontal_units=2),
        # ValenceDot(horizontal_units=1),
        # Sparkline(type='', horizontal_units=4),
    ]

# GridDisplay(
#     title='',
#     results=[
#         MetricEvaluationResult(),
#         MetricEvaluationResult(),
#     ],
#     config=PlotConfiguration(),
#     column_schema=[
#         Text(horizontal_units=1),
#         Number(show_bar=True, horizontal_units=2),
#         ValenceDot(horizontal_units=1),
#         Sparkline(type='', horizontal_units=4),
#     ],
# )
