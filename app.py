# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv(r'D:\st\Dash\diem_2022.csv')
Khoi_dict = {"A":['Toan', 'Ly', 'Hoa'],
             'B':['Toan', 'Hoa','Sinh'],
             'C':['Lich su', 'Dia ly', 'GDCD'],
             'D':['Toan', 'Van', 'Ngoai ngu'],
             'A1':['Toan','Ly','Ngoai ngu']}
# print(df.head())
# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Initialize the app
# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.Div(children='Pho diem theo mon'),
    dcc.Dropdown(options=['Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh','Lich su', 'Dia ly', 'GDCD'],value='Toan',  id='controls-mon'),
    dcc.Graph(figure={}, id='mon-graph'),

    html.Div(children='Pho diem theo khoi'),
    # dash_table.DataTable(data=df.to_dict('records'), page_size=10)
    dcc.Dropdown(options=['A','B','C','D','A1'],value='A',  id='controls-khoi'),
    dcc.Graph(figure={}, id='khoi-graph')
])
# Add controls to build the interaction
@callback(
    Output(component_id='mon-graph', component_property='figure'),
    Input(component_id='controls-mon', component_property='value')
)
def update_graph_mon(mon_chosen):
    data = df[~df[mon_chosen].isnull()][mon_chosen]
    data_output= data.value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    fig = px.bar(data_output, x='Diem', y='counts')
    return fig

@callback(
    Output(component_id='khoi-graph', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value')
)
def update_graph_khoi(khoi_chosen):
    data = df[~df[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1)
    data_output= data.Diem.value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    fig = px.bar(data_output, x='Diem', y='counts')
    
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


    #123