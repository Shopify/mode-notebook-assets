from abc import ABC, abstractmethod
from dataclasses import dataclass
import plotly.graph_objects as go
from IPython.core.display import HTML

# display = ValenceDisplay([
#     Text(text=[], url=[]),
#     Number(data=[], auto_detect_percent=False, bar=True),
#     ValenceDot(valence_series=None),
#     Sparkline(data=[]),
# ])
#
# display.to_html()
# display.to_plotly_figure() => NotImplemented



@dataclass
class SparklineDisplay(ABC):
    pass

    def _build_sparkline_table(self):
        pass

    def to_html(self) -> HTML:
        pass

    def to_plotly_figure(self) -> go.Figure:
        pass


@dataclass
class SparklineBySegmentDisplay(SparklineDisplay):
    pass


@dataclass
class SparklineByMetricDisplay(SparklineDisplay):
    pass