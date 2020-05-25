import json

from IPython.core.display import display, HTML
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot

init_notebook_mode(connected=False)


class AgGridTable(object):
    """
        Parameters
        ----------
        df : Pandas DataFrame
        div_id : Name of your div element uniquely identify this ag-grid object
        Returns
        -------
        string
    """

    def __init__(self, df, div_id=""):
        self.div_id = div_id
        self.header = """
            <script src="https://unpkg.com/ag-grid-community/dist/ag-grid-community.min.noStyle.js"></script>
          <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/dist/styles/ag-grid.css">
          <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/dist/styles/ag-theme-balham.css">
          """

        self.column_defs = self.dataframe_dtypes_to_column_definitions(df)
        self.body = '''<div id="{div_id}" style="height: 600px;width:100%;" class="ag-theme-balham"></div>
  
            <script type="text/javascript" charset="utf-8">
            
              function onBtnExportDataAsCsv(div_name) {{
                  window['gridOptions_'+div_name].api.exportDataAsCsv();
              }}
              
              function dateFormatter(params) {{
                          if (params.value == null) return '';
                  if (params.value == 'NaT') return '';
                  return new Date(params.value).toISOString();
              }}
              
              // specify the columns
              var columnDefs = {column_defs};
  
              // specify the data
              var rowData = {data};
  
              // let the grid know which columns and what data to use
              var gridOptions_{div_id} = {{
                columnDefs: columnDefs,
                rowData: rowData,
                pagination: true
              }};
  
            // lookup the container we want the Grid to use
            var eGridDiv = document.querySelector('#{div_id}');
  
            // create the grid passing in the div to use together with the columns & data we want to use
            new agGrid.Grid(eGridDiv, gridOptions_{div_id});
  
            </script>
        '''.format(
            div_id=self.div_id,
            # TODO: this is not elegant at all but I don't have a better solution yet
            column_defs=json.dumps(self.column_defs).replace('"dateFormatter"', "dateFormatter"),
            data=df.to_json(orient='records'),
        )

        self.csv_export_button = '''<div id="csvExportbutton_{div_id}" style="margin: 10px 0">
          <button onclick="onBtnExportDataAsCsv('{div_id}')">Export CSV</button>
        </div>
        '''.format(div_id=div_id)

        self.html = "<html>" + self.header + self.body + self.csv_export_button + "</html>"

    def dataframe_dtypes_to_column_definitions(self, df) -> list:
        """
        """
        colDefs = []
        for col, dtype in df.dtypes.iteritems():
            colDef = {"headerName": col, "field": col, "sortable": True, "filter": True, "editable": True,
                      "filterParams": {"applyButton": True, "resetButton": True}}
            if any(s in str(dtype) for s in ('int', 'float')):
                colDef["filter"] = 'agNumberColumnFilter'
            elif 'date' in str(dtype):
                colDef["filter"] = 'agDateColumnFilter'
                colDef["valueFormatter"] = 'dateFormatter'

            colDefs.append(colDef)

        return colDefs

    def show(self):
        display(HTML(self.header + self.body + self.csv_export_button))


class PlotlyBigNumberGrid():
    """
    The PlotlyBigNumberGrid class constructs a grid display that is primarily used for big-numbers.

    At present the behaviour of PlotlyBigNumberGrid is to construct a uniformly spaced grid of cells,
    each of which can have various labels and progress indicators added. In addition, some convenience
    functions have been included to create frequently occuring displays.

    Note that the row and column indices used are zero based and increase from left to right and from
    bottom to top. In other words, the (row, column) indices for a 2x2 display are as follows:

    -------------------
    |        |        |
    | (1, 0) | (1, 1) |
    |        |        |
    -------------------
    |        |        |
    | (0, 0) | (0, 1) |
    |        |        |
    -------------------

    Currently there is some support for themes. Themes are specified using nested dictionaries. The
    currently supported theme construct is the following hierarchy:

    theme
     - background [color]

     - unfilled_color [color]
     - progress_color [color]

     - success_color [color]
     - failure_color [color]

     - big_number
        - title_font [plotly font]
        - subtitle_font [plotly font]
        - aggregate_font [plotly font]
        - footer_font [plotly font]
    """

    DEFAULT_THEME = dict(
        background='#f7f7f9',

        unfilled_color='#DFE3E8',
        progress_color='#007ACE',

        success_color='#50B83C',
        failure_color='#DE3618',

        big_number=dict(
            title_font=dict(
                family='Graphik, Helvetica, Arial, sans-serif',
                size=18,
                color='rgb(57, 57, 69)',
            ),
            subtitle_font=dict(
                family='Graphik, Helvetica, Arial, sans-serif',
                size=14,
                color='rgb(99, 115, 129)',
            ),
            aggregate_font=dict(
                family='Graphik, Helvetica, Arial, sans-serif',
                size=48,
                color='rgb(99, 115, 129)',
            ),
            footer_font=dict(
                family='Graphik, Helvetica, Arial, sans-serif',
                size=18,
                color='rgb(99, 115, 129)',
            ),
        )
    )

    def __init__(self, rows=1, cols=1, xgap=0, ygap=0, width=1129, height=346, layout=None, theme=None):
        """
        Construct a PlotlyBigNumberGrid object.

        Args:
          rows (int, optional): The number of rows in the underlying grid. Defaults to 1.
          cols (int, optional): The number of columns in the underlying grid. Defaults to 1.

          xgap (float, optional): The gap, in axis units (between 0 and 1) between columns. Defaults to 0.
          ygap (float, optional): The gap, in axis units (between 0 and 1) between rows. Defaults to 0.

          width (int, optional): The width, in pixels, of the resulting image. Defaults to 1129.
          height (int, optional): The height, in pixels, of the resulting image. Defaults to 346.

          layout (dict, optional): After the default Plotly layout object is created, the attributes
            in `layout` are added. This allows for specialization of the underlying layout.

          theme (dict, optional): The default theme attributes can be customized as desired by the end user.
        """
        self.theme = self.DEFAULT_THEME
        if theme is not None:
            self.theme.update(theme)

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
                                    margin=dict(l=0,
                                                r=0,
                                                t=0,
                                                b=0,
                                                autoexpand=False),
                                    paper_bgcolor=self.theme['background'],
                                    plot_bgcolor=self.theme['background'],
                                    yaxis=dict(zeroline=False,
                                               showgrid=False,
                                               showticklabels=False),
                                    xaxis=dict(zeroline=False,
                                               showgrid=False,
                                               showticklabels=False),
                                    )
        if layout is not None:
            self.fig.layout.update(layout)

    def _get_base_x(self, row, col, placement='center'):
        """
        Compute and return the x coordinate corresponding to the `placement` portion of the cell
        with indices given by `row` and `col`.
        """
        accum = 0
        if placement == 'right':
            accum += self.cell_width
        if placement == 'center':
            accum += self.cell_width / 2
        return (self.cell_width + self.xgap) * col + accum

    def _get_base_y(self, row, col, placement='middle'):
        """
        Compute and return the y coordinate corresponding to the `placement` portion of the cell
        with indices given by `row` and `col`.
        """
        accum = 0
        if placement == 'top':
            accum += self.cell_height
        if placement == 'middle':
            accum += self.cell_height / 2
        return (self.cell_height + self.ygap) * row + accum

    def add_label(self, row, col, text, x, y, font=None, align=None,
                  cell_xanchor='center', cell_yanchor='middle',
                  label_xanchor='center', label_yanchor='middle'):
        """
        Adds a text label as an annotation to the indicated cell.

        Adding a label to the underlying cell requires specifying how to align both the text label
        itself and its placement in the underlying cell. This is done in the following way. First,
        an anchor point in the underlying cell is chosen using `cell_xanchor` and `cell_yanchor`.
        Then, an anchor point in the text label is chosen using `label_xanchor` and `label_yanchor`.
        Lastly, the label anchor is placed at the position specified by `x` and `y`, relative to
        the cell anchor.

        Note that `x` and `y` are in axis units. This means that `x` and `y` should be between 1
        and 0 (inclusive). Also, the underlying cell has height and width 1 in axis units.

        Args:
          row (int): The row index of the cell in which to place the label.
          col (int): The column index of the cell in which to place the label.

          text (str): The string representing the text content of the label.

          x (float): The x coordinate at which to place the label. This is in axis units.
          y (float): The y coordinate at which to place the label. This is in axis units.

          cell_xanchor (str, optional): The base x coordinate for the cell anchor. Can be one of
            `left`, `center`, or `right`. Defaults to `center`.
          cell_yanchor (str, optional): The base y coordinate for the cell anchor. Can be one of
            `top`, `middle`, or `bottom`. Defaults to `middle`.

          label_xanchor (str, optional): The base x coordinate for the label anchor. Can be one of
            `left`, `center`, or `right`. Defaults to `center`.
          label_yanchor (str, optional): The base y coordinate for the label anchor. Can be one of
            `top`, `middle`, or `bottom`. Defaults to `middle`.

          align (str, optional): Indicates how the text should be aligned.

          font (dict, optional): Provides additional attributes for the font object used for the label.
        """
        base_x = self._get_base_x(row, col, cell_xanchor)
        base_y = self._get_base_y(row, col, cell_yanchor)

        label_ann = go.layout.Annotation(
            showarrow=False,
            font=font,
            text=text,
            align=align,
            xref='paper',
            xanchor=label_xanchor,
            x=base_x + x * self.cell_width,
            yref='paper',
            yanchor=label_yanchor,
            y=base_y + y * self.cell_height,
        )

        self.fig.layout.annotations += (label_ann,)

    def add_metric(self, row, col, title, subtitle, aggregate, footer, footer_color=None):
        """
        Add a metric (a big-number) to an existing PlotlyBigNumberGrid.

        The title, subtitle, aggregate and footer parameters are all assumed to be strings. Also note that
        these strings are passed to Plotly to render and so support some html styling. Notably they support
        the <br> tag.

        Args:
          row (int): The row index of the cell in which the big-number display will be created.
          col (int): The column index of the cell in which the big-number display will be created.

          title (str): The title for the big-number display.
          subtitle (str): The subtitle for the big-number display. This is typically used to help
            explain the metric being displayed.
          aggregate (str): The aggregated value that will be displayed in the middle of the big-number
            display. Note that it is assumed that this is a string.
          footer (str): The footer for the big-number display. This is often used to show things like
            period over period growth for the metric being displayed.

          footer_color (str, optional): This color will be used over the template value for the footer.
            This is provided for situations in which you want conditional formatting of the footer.
        """

        # Add the title
        self.add_label(row=row,
                       col=col,
                       text=title,
                       font=self.theme['big_number']['title_font'],
                       x=0,
                       y=0.4,
                       )

        # Add the subtitle
        self.add_label(row=row,
                       col=col,
                       text=subtitle,
                       font=self.theme['big_number']['subtitle_font'],
                       x=0,
                       y=0.25
                       )

        # Add the aggregate
        self.add_label(row=row,
                       col=col,
                       text=aggregate,
                       font=self.theme['big_number']['aggregate_font'],
                       x=0,
                       y=0,
                       )

        # Add the footer
        footer_font = self.theme['big_number']['footer_font']
        if footer_color is not None:
            footer_font['color'] = footer_color

        self.add_label(row=row,
                       col=col,
                       text=footer,
                       font=footer_font,
                       x=0,
                       y=-0.25,
                       )

    def _get_axis_num(self):
        """A simple reference count as we need to generate new axes."""
        self.axis_count += 1
        return self.axis_count

    def _add_bar_chart(self, xaxis, yaxis, value, color, hover_text=None, base=None):
        """Adds a bar chart with optional hover text."""
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
                      width=0.7, height=0.1, x=0, y=0,
                      cell_xanchor='center', cell_yanchor='bottom',
                      line_xanchor='center', line_yanchor='bottom',
                      goal_type=False, goal_invert=False,
                      xaxis=None, yaxis=None, ):
        """
        Adds a sparkline to an existing PlotlyBigNumberGrid.

        Adding a sparkline to the underlying cell requires specifying how to align both the sparkline
        itself and its placement in the underlying cell. This is done in the following way. First,
        an anchor point in the underlying cell is chosen using `cell_xanchor` and `cell_yanchor`.
        Then, an anchor point in the sparkline is chosen using `line_xanchor` and `line_yanchor`.
        Lastly, the line anchor is placed at the position specified by `x` and `y`, relative to
        the cell anchor.

        Note that `x` and `y` are in axis units. This means that `x` and `y` should be between 1
        and 0 (inclusive). Also, the underlying cell has height and width 1 in axis units.

        The default behaviour of the sparkline is to assume that the user wishes to indicate the progress
        made toward a particular goal. This means that if the current value is less than the target value,
        the progress made so far will be indicated with `progress_color`. Then, once the target has been
        reached, the resulting sparkline will display `success_color`.

        If desired, the sparkline can instead indicate whether or not a goal has been met. This can be
        done by setting `goal_type` to `True`. In this case, if the current value of the metric is less
        than the target, the sparkline will display `failure_color`, and when the current value exceeds
        the target then the sparkline will display `success_color`. In addition, this behaviour can
        be inverted by setting `goal_invert` to `True`.

        Args:
          row (int): The row index for the cell in which the sparkline will be added.
          col (int): The column index for the cell in which the sparkline will be added.

          value (float): The current value of the metric being displayed.
          target (float): The target value of the metric being displayed.

          value_txt (str, optional): Optional hover text for the current value.
          target_txt (str, optional): Optional hover text for the target value.

          width (float, optional): The width of the sparkline, in axis units. Defaults to 0.7.
          height (float, optional): The height of the sparkline, in axis units. Defaults to 0.1.

          x (float, optional): The x coordinate in axis units of the sparkline anchor relative to
            the cell anchor. Defaults to 0.
          y (float, optional): The y coordinate in axis units of the sparkline anchor relative to
            the cell anchor. Defaults to 0.

          cell_xanchor (str, optional): The base x coordinate for the cell anchor. Can be one of
            `left`, `center`, or `right`. Defaults to `center`.
          cell_yanchor (str, optional): The base y coordinate for the cell anchor. Can be one of
            `top`, `middle`, or `bottom`. Defaults to `bottom`.

          line_xanchor (str, optional): The base x coordinate for the sparkline anchor. Can be one of
            `left`, `center`, or `right`. Defaults to `center`.
          line_yanchor (str, optional): The base y coordinate for the sparkline anchor. Can be one of
            `top`, `middle`, or `bottom`. Defaults to `bottom`.

          goal_type (bool, optional): Should the displayed sparkline be a goal indicator. Defaults to False.
          goal_invert (bool, optional): If the displayed sparkline is a goal indicator, should the behaviour
            be inverted. Defaults to False.

          xaxis (dict, optional): Additional attributes that can be added to the xaxis dictionary.
          yaxis (dict, optional): Additional attributes that can be added to the yaxis dictionary.
        """

        # In order for the sparklines to work correctly, we need to make sure that barmode is set to stack.
        self.fig.layout.update({'barmode': 'stack'})

        # Since we need to create a new set of axes for the bar charts, we get a new axis index.
        axis_index = self._get_axis_num()

        # Now we need to set up the x-axis.
        x_left = self._get_base_x(row, col, cell_xanchor) + x * self.cell_width

        if line_xanchor == 'right':
            x_left -= width * self.cell_width
        elif line_xanchor == 'center':
            x_left -= width * self.cell_width / 2

        x_right = x_left + width * self.cell_width

        # Now we need to set up the y-axis.
        y_bottom = self._get_base_y(row, col, cell_yanchor) + y * self.cell_height

        if line_yanchor == 'top':
            y_bottom -= height * self.cell_height
        elif line_yanchor == 'middle':
            y_bottom -= height * self.cell_height / 2

        y_top = y_bottom + height * self.cell_height

        # Add the x-axis for the sparkline.
        self.fig.layout['xaxis{}'.format(axis_index)] = dict(
            domain=[x_left, x_right],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            automargin=False,
            anchor='y{}'.format(axis_index),
        )

        # Update the axis properties as necessary.
        if xaxis:
            self.fig.layout['xaxis{}'.format(axis_index)].update(xaxis)

        # Add the y-axis for the sparkline
        self.fig.layout['yaxis{}'.format(axis_index)] = dict(
            domain=[y_bottom, y_top],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            automargin=False,
            anchor='x{}'.format(axis_index),
        )

        # Update the axis properties as necessary.
        if yaxis:
            self.fig.layout['yaxis{}'.format(axis_index)].update(yaxis)

        # Next, add the actual sparkline.
        if value < target:  # We have not yet reached the target
            value_color = self.theme['progress_color']
            if goal_type and goal_invert:
                value_color = self.theme['success_color']
            elif goal_type:
                value_color = self.theme['failure_color']

            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=value,
                                color=value_color,
                                hover_text=value_txt,
                                )
            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=target - value,
                                color=self.theme['unfilled_color'],
                                hover_text=target_txt,
                                )

        else:  # value >= target and so we have reached our target
            value_color = self.theme['success_color']
            if goal_type and goal_invert:
                value_color = self.theme['failure_color']

            self._add_bar_chart(xaxis='x{}'.format(axis_index),
                                yaxis='y{}'.format(axis_index),
                                value=target,
                                color=self.theme['unfilled_color'],
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

