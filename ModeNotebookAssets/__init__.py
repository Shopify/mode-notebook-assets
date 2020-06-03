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


class PlotlyBigNumber():
  '''
    Replicate Mode's Big Number DataViz in Plotly
    
    Usage (single quadrant):
      bn = PlotlyBigNumber()
      bn.add_metric('My Header', '{:,.0f}'.format(500), '{:,.2f}%'.format(.05)),
      bn.plot()
  '''

  MODE_CELL_WIDTH = {
    "col-md-2"  : 174,
    "col-md-3"  : 260,
    "col-md-4"  : 366,
    "col-md-5"  : 462,
    "col-md-6"  : 558,
    "col-md-7"  : 654,
    "col-md-8"  : 750,
    "col-md-9"  : 846,
    "col-md-10" : 942,
    "col-md-11" : 1038,
    "col-md-12" : 1133,
  }
  
  MODE_CELL_HEIGHT = {
    "small"   : 143,
    "medium"  : 346,
    "large"   : 489,
  }
  
  def __init__(self, width="col-md-2", height="small"):
    self.fig = go.FigureWidget()
    
    self.fig.add_pie(
      hole=1,
      values=[100],
      hoverinfo="none",
      textinfo="none",
    )
    
    self.fig.layout = go.Layout(
      showlegend=False,
      autosize=False,
      height=self.MODE_CELL_HEIGHT[height],
      width=self.MODE_CELL_WIDTH[width],
      margin={"l":0, "r":0, "t":0, "b":0},
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      annotations=[],
    )
      
  def set_bgcolor(self, color):
    self.fig.layout.paper_bgcolor = color
    self.fig.layout.plot_bgcolor = color
  
  def set_annotations_color(self, color):
    for annotation in self.fig.layout.annotations:
      annotation.font.color = color
  
  def add_metric(self, header='', body='', footer=''):
            
    self.fig.layout.annotations = [
      go.layout.Annotation(
        font=go.layout.annotation.Font(size=14),
        showarrow=False,
        text='{}'.format(header),
        x=.5,
        y=.8
      ),
      go.layout.Annotation(
        font=go.layout.annotation.Font(size=50),
        showarrow=False,
        text='{}'.format(body),
        x=.5,
        y=.5
      ),
      go.layout.Annotation(
        font=go.layout.annotation.Font(size=14),
        showarrow=False,
        text='{}'.format(footer),
        x=.5,
        y=.2
      )
    ]
    
  def plot(self):
    iplot(self.fig, config={'displayModeBar': False, 'showLink': True})
