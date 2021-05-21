import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

from mode_notebook_assets.practical_dashboard_displays.legacy_helper_functions import map_actionability_score_to_color
from mode_notebook_assets.practical_dashboard_displays.metric_evaluation_pipeline.valence_score import ValenceScore


class PlotConfiguration:

    neutral_valence_color = 'rgb(211,211,211)'
    override_valence_color: tuple = 'rgb(158,202,225)'
    good_valence_palette: list = None
    bad_valence_palette: list = None
    ambiguous_valence_palette: list = None
    primary_chart_trace_template = None
    secondary_chart_trace_template = None
    valence_chart_trace_template = None
    plotly_template = None

    def __post_init__(self):
        self.good_valence_palette = list(self.good_valence_palette or px.colors.sequential.Greens[3:-2])
        self.bad_valence_palette = list(self.bad_valence_palette or px.colors.sequential.Reds[3:-2])
        self.ambiguous_valence_palette = list(self.ambiguous_valence_palette or ['rgb(255,174,66)'])
        self.plotly_template = self.plotly_template or pio.templates['plotly_white']
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
            hoverinfo="x+text",
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