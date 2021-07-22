from dataclasses import dataclass

import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

from mode_notebook_assets.practical_dashboard_displays.legacy_helper_functions import map_actionability_score_to_color
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore


@dataclass
class PlotConfiguration:
    neutral_valence_color: str = 'rgba(211,211,211,0)'
    past_valence_color: str = 'rgb(211,211,211)'
    override_valence_color: tuple = 'rgb(158,202,225)'
    good_valence_palette: list = None
    bad_valence_palette: list = None
    ambiguous_valence_palette: list = None
    primary_chart_trace_template: go.Trace = None
    secondary_chart_trace_template: go.Trace = None
    valence_chart_trace_template: go.Trace = None
    plotly_template: go.layout.Template = None

    def __post_init__(self):
        self.good_valence_palette = list(self.good_valence_palette or px.colors.sequential.Greens[3:-2])
        self.bad_valence_palette = list(self.bad_valence_palette or px.colors.sequential.Reds[3:-2])
        self.ambiguous_valence_palette = list(self.ambiguous_valence_palette or ['rgb(255,174,66)'])
        self.plotly_template = self.plotly_template or pio.templates['plotly_white'].update(
            layout=dict(
                margin=dict(l=20, r=20, t=50, b=20, pad=4),
            ),
        )
        self.primary_chart_trace_template = self.primary_chart_trace_template or go.Scatter(
            mode='lines',
            line=dict(color='gray', width=4),
            showlegend=False,
        )
        self.secondary_chart_trace_template = self.secondary_chart_trace_template or go.Scatter(
            mode='lines',
            line=dict(color='lightgray', dash='dash'),
            showlegend=False,
        )
        self.valence_chart_trace_template = self.valence_chart_trace_template or go.Scatter(
            mode='markers',
            name='Valence',
            hoverinfo="x+y+text",
            hovertemplate='<b>%{x}</b>: %{y}<br><br>%{text}',
            marker=dict(size=10),
            showlegend=False,
        )

    def map_valence_score_to_color(self, v: ValenceScore) -> str:
        if v.is_override:
            return self.override_valence_color
        else:
            return map_actionability_score_to_color(
                v.valence_score,
                good_palette=self.good_valence_palette,
                bad_palette=self.bad_valence_palette,
                ambiguous_palette=self.ambiguous_valence_palette,
                neutral_color=self.neutral_valence_color,
            )

    def map_past_valence_scores_to_color(self, v: ValenceScore) -> str:
        """
        Used to add grey dots over top of valence colors.
        """
        if v.is_override:
            return self.past_valence_color
        else:
            return map_actionability_score_to_color(
                v.valence_score,
                good_palette=[self.past_valence_color],
                bad_palette=[self.past_valence_color],
                ambiguous_palette=[self.past_valence_color],
                neutral_color=self.neutral_valence_color,
            )
