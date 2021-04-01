from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from plotly import graph_objects as go

from mode_notebook_assets.practical_dashboard_displays.legacy_helper_functions import map_actionability_score_to_color
from mode_notebook_assets.practical_dashboard_displays import MetricEvaluationPipeline


def html_div_grid(html_elements:list, table_width='98%', cell_padding='5px', columns=3):

    def table_div(s):
        return f'<div style="width:{table_width}; display: table;">{s}</div>'

    def row_div(s):
        return f'<div style="display: table-row;">{s}</div>'

    def cell_div(s):
        return f'<div style="width: {"{}%".format(round(100/len(html_elements)))}; display: table-cell; padding:{cell_padding}">{s}</div>'

    html_element_rows = [html_elements[i*columns:min(i*columns+columns, len(html_elements))] for i in range(0, len(html_elements)//columns+1)]
    html_format = table_div(''.join(row_div(''.join(cell_div(e) for e in l)) for l in html_element_rows))
    return html_format


def plotly_div_grid(fig_list: list, **kwargs):
    def handle_element(e):
        if isinstance(e, str):
            return e
        else:
            return e.to_html()

    return html_div_grid(
        [handle_element(fig) for fig in fig_list],
        **kwargs,
    )


def convert_metric_status_table_to_html(df: pd.DataFrame, title=None, include_actionability_score=False,
                                        sort_records_by_actionability=False, sort_records_by_value=False,
                                        sort_records_by_name=False, auto_detect_percentages=False,
                                        limit_rows: int = None, font_color='#3C3C3C', title_color='#2A3F5F',
                                        display_current_value_bars=True):

    _df = df.copy()

    def format_urls(r):
        _url = r.get('URL')
        if _url:
            return f'''<a href="{_url}" target="_blank" style="color: {title_color}"><b>{r['Metric']}</b></a>'''
        else:
            return f'''<b>{r['Metric']}</b>'''

    def format_current_value(r):
        _current_value = r.get('Current Value')
        if 0 < _current_value < 1:
            return '<p style="text-align: center">{:.0f}%</p>'.format(_current_value*100)
        else:
            return '<p style="text-align: center">{:.0f}</p>'.format(_current_value)


    if 'URL' in _df.columns:
        _df['Metric'] = _df.apply(
            func=format_urls,
            axis=1,
        )
        _df = _df.drop('URL', axis=1)
    else:
        _df['Metric'] = _df.apply(
            func=lambda r: f'''<b style="color: {title_color}">{r['Metric']}</b>''',
            axis=1,
        )

    if auto_detect_percentages:
        _df['Current Value'] = _df.apply(
            func=format_current_value,
            axis=1,
        )

    if sort_records_by_actionability and sort_records_by_value:
        _df = _df.sort_values(by=['Actionability Score', 'Current Value'], ascending=False)
    elif sort_records_by_value:
        _df = _df.sort_values(by=['Current Value'], ascending=False)
    elif sort_records_by_actionability:
        _df = _df.sort_values(by=['Actionability Score'], ascending=False)
    elif sort_records_by_name:
        _df = _df.sort_values(by=['Metric'])
    else:
        pass

    if include_actionability_score is False and 'Actionability Score' in _df.columns:
        _df = _df[[c for c in _df.columns if c != 'Actionability Score']]

    if limit_rows is not None:
        _df = _df.head(limit_rows)

    _output = _df.style.set_table_styles(
        [{'selector': '*',
          'props': [('all', 'revert')]},
         {'selector': '.row_heading',
          'props': [('display', 'none')]},
         {'selector': '.col_heading',
          'props': [('display', 'none')]},
         {'selector': '.blank.level0',
          'props': [('display', 'none')]},
         {'selector': 'tr',
          'props': [('padding-bottom', '100em')]},
         {'selector': '.data',
          'props': [
              ('font-family', 'Arial'),
              ('color', font_color),
              ('border-width', 0),
              ('padding-bottom', '.25em'),
          ]}]
    ).format({
        'Metric': '{}',
        'Current Value': '{}' if auto_detect_percentages else '<p style="text-align: center">{:.0f}</p>'
    })

    if display_current_value_bars and not auto_detect_percentages:
        _output = _output.bar(
            'Current Value',
            color='lightgray',
            vmin=0,
        )

    _output = _output.render(header=False, index=False)

    if title is not None:
        _output = f'<h4 style="color: {title_color};">{title}</h4>' + _output

    return _output


@dataclass
class DatasetEvaluationGenerator:

    df: pd.DataFrame
    grouping_set: list
    index_column: str
    measure_column: str
    title_format_template: str = None

    def generate_grouping_set_series_lookup(self):
        def convert_to_tuple(x):
            if isinstance(x, str):
                return (x, )
            else:
                return tuple(x)

        _df = self.df.copy().reset_index()

        _grouping_set_actuals = [
            convert_to_tuple(x) for x in list(
                _df.groupby(self.grouping_set)
                    .sum()[self.measure_column]
                    .sort_values(ascending=False).index
            )
        ]

        _output = {}

        for s in _grouping_set_actuals:
            if self.title_format_template is None:
                _key = ' '.join(s)
            else:
                _key = self.title_format_template.format(*s)

            _output[_key] = (
                _df[(_df[self.grouping_set] == s).all(axis=1)]
                    .groupby(self.index_column).sum()[self.measure_column]
            )

        return _output

    def generate_grouping_set_metric_pipeline_lookup(self, metric_evaluation_pipeline_options=None):
        _data_series_lookup = self.generate_grouping_set_series_lookup()

        _metric_evaluation_pipeline_options = (metric_evaluation_pipeline_options or {})

        _pipeline_lookup = {
            key: MetricEvaluationPipeline(
                series,
                metric_name=key,
                measure_name=self.measure_column,
                **_metric_evaluation_pipeline_options,
            ) for key, series in _data_series_lookup.items()
        }

        return _pipeline_lookup

    def generate_actionability_time_series_figures(self, actionability_time_series_options=None):

        _actionability_time_series_options = (actionability_time_series_options or {})

        return [
            pipeline.display_actionability_time_series(
                title=key,
                metric_name=self.measure_column,
                **_actionability_time_series_options,
            )
            for key, pipeline in self.generate_grouping_set_metric_pipeline_lookup().items()
        ]

    def display_actionability_time_series_grid(self, actionability_time_series_options=None,
                                               plotly_div_grid_options=None):

        _plotly_div_grid_options = (plotly_div_grid_options or {})

        return plotly_div_grid(
            self.generate_actionability_time_series_figures(
                actionability_time_series_options=actionability_time_series_options
            ),
            **_plotly_div_grid_options
        )

    def generate_actionability_summary_records(self, get_current_display_record_options=None):

        _get_current_display_record_options = (get_current_display_record_options or {})

        return [
            pipeline.get_current_display_record(
                **_get_current_display_record_options
            ) for key, pipeline in self.generate_grouping_set_metric_pipeline_lookup().items()
        ]

    def display_actionability_summary_records(self,
                                              get_current_display_record_options=None,
                                              convert_metric_status_table_to_html_options=None):

        _convert_metric_status_table_to_html_options = (convert_metric_status_table_to_html_options or {})
        return convert_metric_status_table_to_html(
            pd.DataFrame.from_records(
                self.generate_actionability_summary_records(
                    get_current_display_record_options=get_current_display_record_options
                )
            ),
            **_convert_metric_status_table_to_html_options
        )


def make_metric_segmentation_grid_display(df: pd.DataFrame, index_column: str, measure_column: str, spec: List[tuple]):
    """
    A reusable template for creating a collection of metric segmentation grids that all display different segmentations
    of the same metric.

    Parameters
    ----------
    df: Dataframe, passed as-is to DatasetEvaluationGenerator
    index_column: date column for grouping, passed as-is to DatasetEvaluationGenerator
    measure_column: additive fact column to display as metric, passed as-is to DatasetEvaluationGenerator
    spec: A list of tuples in format (column_name, display_name). For each entry in spec, a segmentation grid
          will be displayed based on the categorical column `column_name` and will be labelled with the display
          string `display_name`

    Returns
    -------
    An HTML string. Display in a notebook using IPython.display.HTML
    """
    return html_div_grid([
        DatasetEvaluationGenerator(
            df=df,
            grouping_set=[colname],
            index_column=index_column,
            measure_column=measure_column
        ).display_actionability_summary_records(
            convert_metric_status_table_to_html_options={
                'title': displayname,
            },
        )
        for colname, displayname in spec
    ])


def make_metric_collection_display(metric_specifications: List[dict], title: str = None,
                                   convert_metric_status_table_to_html_options: dict = None):
    """
    A template function for generating a list of sparkline displays for
    independent time series.

    Parameters
    ----------
    metric_specifications: A list of dictionaries with keys time_series (pd.Series), name (str), and url (optional str)
    title: A (str) title for the display
    convert_metric_status_table_to_html_options: pass keyword arguments to convert_metric_status_table_to_html

    Returns
    -------
    HTML string KPI display - render in notebook with IPython.display.HTML
    """
    def add_dict_key(d: dict, key: str, value: str):
        _output = d.copy()
        _output[key] = value
        return _output

    return convert_metric_status_table_to_html(pd.DataFrame([
        # Initialize a MetricEvaluationPipeline
        add_dict_key(
            MetricEvaluationPipeline(
                s=kpi_dict['time_series'],
                metric_name=kpi_dict['name'],
                # Instead of the annotated time series chart,
                # we're going to ask for the raw info for the
                # current period to build up our KPI collection.
            ).get_current_display_record(),
            'URL',
            kpi_dict.get('url'),
        )
        for kpi_dict in metric_specifications
    ]),
        title=title,
        display_current_value_bars=False,
        **(convert_metric_status_table_to_html_options or {}),
    )


@dataclass
class TestCumulativeTargetAttainmentDisplay:
    """
    Class for creating a cumulative target attainment display.
    It answers the question "how are we pacing against our end
    of period target"? Valence indicators are based on whether
    we are pacing towards our end of period goal.
    Input series are non-cumulative, but will be transformed
    to cumulative series for calculation and display.
    Parameters
    ----------
    actual: Non-cumulative time series of actual values (pd.Series)
    target_total: The total target for the given period (int)
    target_period_index: A pd.DatetimeIndex representing the target period; to get started, try out pd.date_range
    """

    actual: pd.Series
    target_total: int
    period_start_date: str
    period_end_date: str

    metric_name: str = None

    minor_attainment_deviation: float = 0
    major_attainment_deviation: float = .20

    is_higher_good: bool = True
    is_lower_good: bool = False
    good_palette: list = None
    bad_palette: list = None
    ambiguous_palette: list = None

    def __post_init__(self):

        self.target_period_index = pd.date_range(start=self.period_start_date, end=self.period_end_date)

        if type(self.target_total) in [int, float]:

            self._cleaned_actual = pd.Series(
                data=self.actual.values,
                index=pd.to_datetime(self.actual.index),
            ).reindex(
                index=pd.date_range(self.period_start_date, max(self.actual.index)),
                fill_value=0,
            )

            current_period = max(self._cleaned_actual.index)
            current_period_index = self._cleaned_actual.index.get_loc(current_period)

            # generate target series
            number_of_periods = len(self.target_period_index)
            interpolated_period_target = round(self.target_total / number_of_periods)
            period_target_remainder = self.target_total - (interpolated_period_target * number_of_periods)

            self.target_attainment_df = pd.DataFrame(index=self.target_period_index).assign(
                is_current_period=pd.Series([False] * (len(self._cleaned_actual) - 1) + [True],
                                            index=self._cleaned_actual.index),
                actual=self._cleaned_actual,
                actual_cumulative=self._cleaned_actual.cumsum(),
                target_interpolated=interpolated_period_target,
                target_cumulative=lambda df: df.target_interpolated.cumsum() + period_target_remainder,
                attainment_pacing_proportion=lambda df: df.actual_cumulative / df.target_cumulative,
                actionability_hover_text=lambda df: df.attainment_pacing_proportion.apply(
                    lambda x: 'Pacing to {}% of target.'.format(int(100 * x)) if not pd.isnull(x) else ''
                ),
                actionability_scores=(
                    lambda df: df.apply(
                        lambda r: self.calculate_target_attainment_valence(
                            actual_value=r['actual_cumulative'],
                            target_value=r['target_cumulative'],
                        ) if r['is_current_period'] else 0,
                        axis=1
                    )
                ),
                actionability_actuals=lambda df: df.actual_cumulative,
                # initialize as empty; only last period will be calculated
            )

        else:

            self._cleaned_actual = pd.Series(
                data=self.actual.values,
                index=pd.to_datetime(self.actual.index),
            ).reindex(
                index=pd.date_range(self.period_start_date, max(self.actual.index)),
                fill_value=0,
            )

            self.reindexed_target_series = pd.Series(
                data=self.target_total,
                index=pd.to_datetime(self.target_total.index)
            )

            current_period = max(self._cleaned_actual.index)
            current_period_index = self._cleaned_actual.index.get_loc(current_period)

            self.target_attainment_df = pd.DataFrame(index=self._cleaned_actual.index).assign(
                is_current_period=pd.Series([False] * (len(self._cleaned_actual) - 1) + [True],
                                            index=self._cleaned_actual.index),
                actual=self._cleaned_actual,
                actual_cumulative=self._cleaned_actual.cumsum(),
                target_interpolated=self.reindexed_target_series,
                target_cumulative=lambda df: df.target_interpolated.cumsum().interpolate(),

                attainment_pacing_proportion=lambda df: df.actual_cumulative / df.target_cumulative,
                actionability_hover_text=lambda df: df.attainment_pacing_proportion.apply(
                    lambda x: 'Pacing to {}% of target.'.format(int(100 * x)) if not pd.isnull(x) else ''
                ),
                actionability_scores=(
                    lambda df: df.apply(
                        lambda r: self.calculate_target_attainment_valence(
                            actual_value=r['actual_cumulative'],
                            target_value=r['target_cumulative'],
                        ) if r['is_current_period'] else 0,
                        axis=1
                    )
                ),
                actionability_actuals=lambda df: df.actual_cumulative,
                # initialize as empty; only last period will be calculated
            )

        self.target_attainment_df.actionability_scores[current_period_index] = self.calculate_target_attainment_valence(
            actual_value=self.target_attainment_df.actual_cumulative[current_period_index],
            target_value=self.target_attainment_df.target_cumulative[current_period_index],
        )

    def calculate_target_attainment_valence(self, actual_value, target_value):

        target_deviation = (actual_value - target_value) / target_value
        if np.abs(target_deviation) < self.minor_attainment_deviation:
            return 0
        else:
            # The minimum actionable score is 0.01 (minor deviation) and the
            # "soft maximum" is 1 (major deviation). Actionability score is based on
            # where the deviation occurs between the minor and major deviation thresholds.
            # Scores above 1 are allowed but do not change the output.
            return np.sign(target_deviation) * (
                    0.01 + (
                    (np.abs(target_deviation) - self.minor_attainment_deviation)
                    / (self.major_attainment_deviation - self.minor_attainment_deviation)
            )
            )

    def display_cumulative_attainment_chart(self, title=None, show_legend=False, enforce_non_negative_yaxis=True):

        fig = go.Figure(
            layout=go.Layout(
                title=title,
                paper_bgcolor='white',
                plot_bgcolor='white',
                hovermode='x',
            )
        )

        # plot cumulative target values
        fig.add_trace(
            go.Scatter(
                x=self.target_attainment_df.index,
                y=self.target_attainment_df.target_cumulative,
                mode='lines',
                name='Target',
                line=dict(color='lightgray', dash='dash'),
                showlegend=show_legend,
            )
        )

        # plot cumulative actual values
        fig.add_trace(
            go.Scatter(
                x=self.target_attainment_df.index,
                y=self.target_attainment_df.actual_cumulative,
                mode='lines',
                name='Actual',
                line=dict(color='gray', width=4),
                showlegend=show_legend,
            )
        )

        # plot actionable periods
        fig.add_trace(
            go.Scatter(
                x=self.target_attainment_df.index,
                y=self.target_attainment_df.actionability_actuals,
                text=self.target_attainment_df.actionability_hover_text,
                mode='markers',
                name='Actionability',
                hoverinfo="x+text",
                marker=dict(
                    size=10,
                    color=[
                        map_actionability_score_to_color(
                            score,
                            good_palette=self.good_palette,
                            bad_palette=self.bad_palette,
                            ambiguous_palette=self.ambiguous_palette,
                            neutral_color='rgba(255,255,255, 0)',
                        ) for score in self.target_attainment_df.actionability_scores
                    ]
                ),
                showlegend=show_legend,
            )
        )

        if enforce_non_negative_yaxis:
            fig.update_yaxes(rangemode='nonnegative')

        return fig.to_html()