from abc import abstractmethod
from dataclasses import dataclass
from typing import List

import plotly.graph_objects as go
import numpy as np
from IPython.core.display import HTML

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.plot.charts import ValenceChart, TimeSeriesValenceLineChart
from mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration import PlotConfiguration


@dataclass
class PlotlyTraceGridColumnSpec(object):
    horizontal_units: int  # scale-less; use for ratio

    def create_figure_from_metirc_evaluation_result(self, result: MetricEvaluationResult,
                                                    config: PlotConfiguration) -> List[go.Trace]:
        return [
            go.Scatter(
                x=[0.5],
                y=[0.5],
                text=['Placeholder'],
                hovertemplate='This trace has not been implemented.',
                textposition='middle center',
                mode='text',
                name='Info',
                textfont=config.plotly_template.layout.font.to_plotly_json(),
            )
        ]


class AbstractTextColumn(PlotlyTraceGridColumnSpec):

    @staticmethod
    @abstractmethod
    def _get_text_from_result(self, result: MetricEvaluationResult) -> str:
        return NotImplemented

    @property
    def label(self):
        return 'Info'

    @property
    @abstractmethod
    def hovertemplate(self):
        return 'See Plotly documentation to configure hover template.'

    def create_figure_from_metirc_evaluation_result(self, result: MetricEvaluationResult,
                                                    config: PlotConfiguration) -> List[go.Trace]:
        return [
            go.Scatter(
                x=[0.5],
                y=[0.5],
                text=[self._get_text_from_result(result)],
                hovertemplate=self.hovertemplate,
                textposition='middle center',
                mode='text',
                name=self.label,
                textfont=config.plotly_template.layout.font.to_plotly_json(),
            )
        ]


class MostRecentPeriodValue(AbstractTextColumn):

    @property
    def hovertemplate(self):
        return 'The most recent period value is %{text}.'

    def _get_text_from_result(self, result: MetricEvaluationResult) -> str:
        return str(result.data.values[-1])


class MostRecentPeriodBarHorizontal(PlotlyTraceGridColumnSpec):

    def create_figure_from_metirc_evaluation_result(self, result: MetricEvaluationResult,
                                                    config: PlotConfiguration) -> List[go.Trace]:

        return [
            go.Bar(
                x=[result.data.values[-1]],
                y=[0],
                orientation='h',
                text=[''],
                hovertemplate='',
                name='Info',
                width=.25,
                marker={'color': config.secondary_chart_trace_template.line.color}
            )
        ]


class ResultName(AbstractTextColumn):

    @property
    def hovertemplate(self):
        return 'Click here for detailed insights for this metric.'

    def _get_text_from_result(self, result: MetricEvaluationResult) -> str:
        if result.metadata is not None:
            if result.metadata.url is None:
                return result.metadata.name or 'Metric Unknown'
            else:
                return f'<a href="{result.metadata.url}">{result.metadata.name}</a>'
        else:
            return 'Metric Unknown'


class ValenceDot(PlotlyTraceGridColumnSpec):

    def create_figure_from_metirc_evaluation_result(self, result: MetricEvaluationResult,
                                                    config: PlotConfiguration) -> List[go.Trace]:
        return [
            go.Scatter(
                x=[0.5],
                y=[0.5],
                marker=dict(
                    size=[25],
                    color=[config.map_valence_score_to_color(result.valence_score_series.last_record())]
                ),
                hovertemplate=result.valence_score_series.last_record().valence_description,
                name='Valence Indicator',
            )
        ]


class Sparkline(PlotlyTraceGridColumnSpec):

    def create_figure_from_metirc_evaluation_result(self, result: MetricEvaluationResult,
                                                    config: PlotConfiguration) -> List[go.Trace]:
        _time_series_chart = TimeSeriesValenceLineChart(
            result=result,
            metric_name=None if result.metadata is None else result.metadata.name,
            config=config,
        ).to_plotly_figure()
        return _time_series_chart.data


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

        _layout = go.Layout(
            title=self.title,
            showlegend=False,
            template=self.config.plotly_template,
        )

        for column_index in range(0, self._n_cols):
            for row_index in range(0, self._n_rows):
                _axis_number = row_index * self._n_cols + column_index + 1
                _layout.update(
                    dict1={
                        f'xaxis{_axis_number}': {
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
                            'anchor':         f'x{_axis_number}',
                            'domain':         [
                                # lower domain value
                                0 if row_index == self._n_rows - 1 else _row_normalized_breakpoints[row_index + 1],
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
        _figure = go.Figure(layout=layout)

        _maximum_recent_period = max([result.data.values[-1] for result in self.results])

        for column_index in range(0, self._n_cols):
            for row_index in range(0, self._n_rows):
                _axis_number = row_index * self._n_cols + column_index + 1
                _result_traces = self.column_schema[column_index].create_figure_from_metirc_evaluation_result(
                    self.results[row_index],
                    self.config,
                )
                for trace in _result_traces:
                    _figure = _figure.add_trace(
                        trace.update(
                            xaxis=f'x{_axis_number}',
                            yaxis=f'y{_axis_number}',
                        )
                    )

                if isinstance(self.column_schema[column_index], MostRecentPeriodBarHorizontal):
                    _figure.layout.update(
                        {f'xaxis{_axis_number}': {'range': [0, _maximum_recent_period]}}
                    )


        return _figure

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
        ValenceDot(horizontal_units=1),
        ResultName(horizontal_units=2),
        MostRecentPeriodValue(horizontal_units=1),
        MostRecentPeriodBarHorizontal(horizontal_units=1),
        Sparkline(horizontal_units=4),
    ]