import json

from IPython.core.display import display, HTML

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
