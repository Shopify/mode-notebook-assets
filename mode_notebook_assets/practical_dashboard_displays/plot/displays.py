from dataclasses import dataclass
from typing import Dict, Any, List

import pandas as pd
from IPython.core.display import HTML
from plotly.graph_objs import Figure

from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_checks import \
    AnnotateAndSnoozeMetricCheck
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.metric_evaluation_pipeline import \
    MetricEvaluationPipeline, MetricEvaluationResult
from mode_notebook_assets.practical_dashboard_displays.plot.display_grid import GridDisplay, ValenceDot, ResultName, \
    MostRecentPeriodValue, MostRecentPeriodBarHorizontal, Sparkline
from mode_notebook_assets.practical_dashboard_displays.plot.plot_configuration import PlotConfiguration

SPARKLINE_GRID_SCHEMA = [
    ValenceDot(horizontal_units=1),
    ResultName(horizontal_units=3),
    MostRecentPeriodValue(horizontal_units=1),
    MostRecentPeriodBarHorizontal(horizontal_units=1),
    Sparkline(horizontal_units=4),
]


@dataclass
class SparklinesByMetricDisplay:
    results: List[MetricEvaluationResult]
    title: str
    config: PlotConfiguration

    def __post_init__(self):
        self.column_schema = SPARKLINE_GRID_SCHEMA

        self.grid_display_object = GridDisplay(
            title=self.title,
            results=self.results,
            column_schema=self.column_schema,
            config=PlotConfiguration() if self.config is None else self.config,
        )

    def to_plotly_figure(self):
        return self.grid_display_object.to_plotly_figure()

    def to_html(self):
        return self.grid_display_object.to_html()


@dataclass
class SparklinesBySegmentDisplay:
    df: pd.DataFrame
    grouping_set: list
    index_column: str
    measure_column: str
    display_title: str = None
    metric_evaluation_pipeline: MetricEvaluationPipeline = None
    annotations_lookup: Dict[str, pd.Series] = None
    metadata_lookup: Dict[str, Dict[str, Any]] = None
    config: PlotConfiguration = None

    def __post_init__(self):
        if self.metric_evaluation_pipeline is None:
            self.metric_evaluation_pipeline = MetricEvaluationPipeline()

        self.results_list = self._generate_results_list()

        self._grid_display_object = GridDisplay(
            title='Grid Valence Display',
            results=self.results_list,
            column_schema=[
                ValenceDot(horizontal_units=1),
                ResultName(horizontal_units=3),
                MostRecentPeriodValue(horizontal_units=1),
                MostRecentPeriodBarHorizontal(horizontal_units=1),
                Sparkline(horizontal_units=4),
            ],
            config=PlotConfiguration() if self.config is None else self.config,
        )

    def _generate_grouping_set_series_lookup(self):
        def convert_to_tuple(x):
            if isinstance(x, str):
                return (x,)
            else:
                return tuple(x)

        _df = self.df.copy().reset_index()

        _grouping_set_actuals = [
            convert_to_tuple(x) for x in list(
                _df.groupby(self.grouping_set).sum()[self.measure_column].sort_values(ascending=False).index
            )
        ]

        _output = {}

        for s in _grouping_set_actuals:
            _key = ' '.join(s)
            _output[_key] = (
                _df[(_df[self.grouping_set] == s).all(axis=1)]
                    .groupby(self.index_column).sum()[self.measure_column]
            )

        return _output

    def _generate_results_list(self):
        _data_series_lookup = self._generate_grouping_set_series_lookup()
        _results_list = []
        for key, series in _data_series_lookup.items():
            _is_annotation_in_mep = any([
                isinstance(check, AnnotateAndSnoozeMetricCheck)
                for check in self.metric_evaluation_pipeline.metric_checks
            ])
            _is_annotation_provided = self.annotations_lookup is not None and key in self.annotations_lookup
            if _is_annotation_provided and not _is_annotation_in_mep:
                self.metric_evaluation_pipeline.metric_checks.append(AnnotateAndSnoozeMetricCheck())

            if self.metadata_lookup is not None and key in self.metadata_lookup:
                _metadata_to_add = self.metadata_lookup[key]
            else:
                _metadata_to_add = {}

            _results_list.append(
                self.metric_evaluation_pipeline.apply(
                    s=series,
                ).add_metadata(
                    name=key,
                ).add_metadata(
                    **_metadata_to_add
                )
            )

        return _results_list

    def to_plotly_figure(self) -> Figure:
        return self._grid_display_object.to_plotly_figure()

    def to_html(self) -> HTML:
        return self._grid_display_object.to_html()