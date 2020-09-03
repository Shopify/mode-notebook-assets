import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

import pandas as pd

init_notebook_mode(connected=False)

class PlotlyBigNumberGrid():
    """
    The PlotlyBigNumberGrid class constructs a big-number like display.
    """
    BACKGROUND = '#f7f7f9'
    UNFILLED_COLOR = '#DFE3E8'
    PROGRESS_COLOR = '#007ACE'
    SUCCESS_COLOR = '#50B83C'
    FAILURE_COLOR = '#DE3618'

    def __init__(self, rows=1, cols=1, xgap=0, ygap=0, width=1129, height=346, layout=None):
        """
        Constructs a PlotlyBigNumberGrid object which can have various metrics added.
        
        rows and cols can be set in order to construct multi-big-num arrays and displays.
        width and height can be set and will affect the resulting image size.
        xgap and ygap set the space, in axis units, between the cells in the display.
        """

        self.rows = rows
        self.cols = cols

        self.xgap = xgap
        self.ygap = ygap

        self.cell_width = (1. - (self.cols - 1) * self.xgap) / self.cols
        self.cell_height = (1. - (self.rows - 1) * self.ygap) / self.rows

        self.width = width
        self.height = height

        self.axis_count = 0

        self.fig = go.Figure()

        self.fig.layout = go.Layout(showlegend=False,
                                    autosize=False,
                                    height=self.height,
                                    width=self.width,
                                    margin={'l': 0, 'r': 0, 't': 0, 'b': 0, 'autoexpand': False},
                                    paper_bgcolor=self.BACKGROUND,
                                    plot_bgcolor=self.BACKGROUND,
                                    yaxis=dict(zeroline=False,
                                               showgrid=False,
                                               showticklabels=False),
                                    xaxis=dict(zeroline=False,
                                               showgrid=False,
                                               showticklabels=False),
                                    )
        if layout is not None:
            self.fig.layout.update(layout)

    def get_base_x(self, row, col, placement='center'):
        """Compute the x coordinate corresponding to the placement portion of the cell with indices given by row and col."""
        if placement == 'left':
            return (self.cell_width + self.xgap) * col
        elif placement == 'right':
            return (self.cell_width + self.xgap) * col + self.cell_width
        else:
            return (self.cell_width + self.xgap) * col + self.cell_width / 2

    def get_base_y(self, row, col, placement='middle'):
        """Compute the y coordinate corresponding to the placement portion of the cell with indices given by row and col."""
        if placement == 'bottom':
            return (self.cell_height + self.ygap) * row
        elif placement == 'top':
            return (self.cell_height + self.ygap) * row + self.cell_height
        else:
            return (self.cell_height + self.ygap) * row + self.cell_height / 2

    def add_label(self, row, col, text, x, y, font=None, align=None, xanchor='center', yanchor='middle'):
        """Adds a text label as an annotation to the indicated cell."""
        base_x = self.get_base_x(row, col, xanchor)
        base_y = self.get_base_y(row, col, yanchor)

        label_ann = go.layout.Annotation(
            showarrow=False,
            font=font,
            text=text,
            align=align,
            xref='paper',
            xanchor=xanchor,
            x=base_x + x * self.cell_width,
            yref='paper',
            yanchor=yanchor,
            y=base_y + y * self.cell_height,
        )

        self.fig.layout.annotations += (label_ann,)

    def add_metric(self, row, col, title, subtitle, aggregate, footer, footer_color=None):
        """
        Add a metric to an existing PlotlyBigNumberGrid.
        
        row and col specify which of the cells will display the metric. Note that 0-offsets are used.
        title is a string which represents the first line of a particular metric.
        subtitle appears directly under the title and typically helps explain the metric.
        aggregate is the largest item displayed and should contain whatever value you wish to display.
        footer appears below the aggregate and is sometimes used to show things like period over period growth.
        footer_color may optionally be used to set the color of the footer string.
        
        The title, subtitle, aggregate and footer parameters are all assumed to be strings. Also note that
        these strings are passed to Plotly to render and so support some html styling. Notably they support
        the <br> tag.
        """

        # Add the title
        self.add_label(row=row,
                       col=col,
                       text=title,
                       font=go.layout.annotation.Font(
                           family='Graphik, Helvetica, Arial, sans-serif',
                           size=18,
                           color='rgb(57, 57, 69)',
                       ),
                       x=0,
                       y=0.4,
                       )

        # Add the subtitle
        self.add_label(row=row,
                       col=col,
                       text=subtitle,
                       font=go.layout.annotation.Font(
                           family='Graphik, Helvetica, Arial, sans-serif',
                           size=14,
                           color='rgb(99, 115, 129)',
                       ),
                       x=0,
                       y=0.25
                       )

        # Add the aggregate
        self.add_label(row=row,
                       col=col,
                       text=aggregate,
                       font=go.layout.annotation.Font(
                           family='Graphik, Helvetica, Arial, sans-serif',
                           size=48,
                           color='rgb(99, 115, 129)',
                       ),
                       x=0,
                       y=0,
                       )

        if footer is not None:
            # Add the footer
            self.add_label(row=row,
                           col=col,
                           text=footer,
                           font=go.layout.annotation.Font(
                               family='Graphik, Helvetica, Arial, sans-serif',
                               size=18,
                               color=footer_color if footer_color else 'rgb(99, 115, 129)',
                           ),
                           x=0,
                           y=-0.25,
                           )

    def _get_axis_num(self):
        self.axis_count += 1
        return self.axis_count

    def _add_bar_chart(self, xaxis, yaxis, value, color, hover_text=None, base=None):
        self.fig.add_bar(
            showlegend=False,
            hoverinfo='none' if hover_text is None else 'text',
            hovertext=[hover_text],
            base=base,
            x=[value],
            xaxis=xaxis,
            y=[0],
            yaxis=yaxis,
            orientation='h',
            marker=dict(
                color=color,
            ),
        )

    def add_sparkline(self, row, col, value, target,
                      value_txt=None, target_txt=None,
                      width=0.7, height=0.1,
                      x=0, y=0,
                      xanchor='center',
                      yanchor='bottom',
                      goal_type=False, goal_invert=False,
                      xaxis=None, yaxis=None, ):

        """Adds a sparkline to the cell indexed by row and col."""

        # In order for the sparklines to work correctly, we need to make sure that barmode is set to stack.
        self.fig.layout.update({'barmode': 'stack'})

        # Set up axes
        axis_index = self._get_axis_num()

        x_left = self.get_base_x(row, col, xanchor) + x

        if xanchor == 'right':
            x_left -= width * self.cell_width
        elif xanchor == 'center':
            x_left -= width * self.cell_width / 2

        x_right = x_left + width * self.cell_width

        y_bottom = self.get_base_y(row, col, yanchor) + y

        if yanchor == 'top':
            y_bottom -= height * self.cell_height
        elif yanchor == 'middle':
            y_bottom -= height * self.cell_height / 2

        y_top = y_bottom + height * self.cell_height

        # First, add axis for the sparkline
        self.fig.layout['xaxis{}'.format(axis_index)] = dict(
            domain=[x_left, x_right],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            automargin=False,
            anchor='y{}'.format(axis_index),
        )

        if xaxis:
            self.fig.layout['xaxis{}'.format(axis_index)].update(xaxis)

        self.fig.layout['yaxis{}'.format(axis_index)] = dict(
            domain=[y_bottom, y_top],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            automargin=False,
            anchor='x{}'.format(axis_index),
        )

        if yaxis:
            self.fig.layout['yaxis{}'.format(axis_index)].update(yaxis)

        # Next, add the actual sparkline.

        if value < target:  # We have not yet reached the target
            value_color = self.PROGRESS_COLOR
            if goal_type and goal_invert:
                value_color = self.SUCCESS_COLOR
            elif goal_type:
                value_color = self.FAILURE_COLOR

            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=value,
                                color=value_color,
                                hover_text=value_txt,
                                )
            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=target - value,
                                color=self.UNFILLED_COLOR,
                                hover_text=target_txt,
                                )

        else:  # value >= target and so we have reached our target
            value_color = self.SUCCESS_COLOR
            if goal_type and goal_invert:
                value_color = self.FAILURE_COLOR

            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=target,
                                color=self.UNFILLED_COLOR,
                                hover_text=target_txt,
                                base=0,
                                )
            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=value,
                                color=value_color,
                                hover_text=value_txt,
                                base=0,
                                )
            targ = dict(
                type='line',
                x0=target,
                x1=target,
                y0=-.5,
                y1=.5,
                xref='x{}'.format(axis_index),
                yref='y{}'.format(axis_index),
                line=dict(
                    color='#000000',
                )
            )
            self.fig.layout.shapes += (targ,)

    def plot(self):
        """Plot and display the PlotlyBigNumberGrid"""
        iplot(self.fig, image_width=self.width, image_height=self.height,
              config={'displayModeBar': False, 'showLink': True})

