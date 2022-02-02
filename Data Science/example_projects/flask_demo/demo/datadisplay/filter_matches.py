"""Instantiate a Dash app."""
import dash
from dash import html
from .layout import html_layout

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/exampledashboard/',
        external_stylesheets=[
            '/static/style.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
                  html.H1("hello"), 
                  id='dash-container'
                  )
    return dash_app.server


#def create_data_table(df):
    #"""Create Dash datatable from Pandas DataFrame."""
    #table = dash_table.DataTable(
        #id='database-table',
        #columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns],
        #data=df.to_dict("records"),
        #sort_action="native",
        #filter_action="native",
        #row_selectable="multi",
        #row_deletable=True,
        #selected_columns=[],
        #selected_rows=[],
        #sort_mode='native',
        #page_size=10,
        #export_format='csv',
    #)
    #return table
    
#def init_table_callbacks(dash_app):
    #@dash_app.callback(
        #Output('database-table', 'style_data_conditional'),
        #[Input('database-table', 'selected_columns')]
        #)
    #def update_table(selected_columns):
        #return [{
            #'if': { 'column_id': i },
            #'background_color': '#D2F3FF'
        #} for i in selected_columns]



