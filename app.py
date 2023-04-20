from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import math

# Incorporate data
df = pd.read_csv('diem_2022.csv')
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
# app.layout = html.Div([
#     dcc.Dropdown(options=[i for i in range(2017,2023)],value='2022',  id='controls-year'),
#     html.Div(children='Pho diem theo mon'),
#     dcc.Dropdown(options=['Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh','Lich su', 'Dia ly', 'GDCD'],value='Toan',  id='controls-mon'),
#     dcc.Graph(figure={}, id='mon-graph'),

#     html.Div(children='Pho diem theo khoi'),
#     # dash_table.DataTable(data=df.to_dict('records'), page_size=10)
#     dcc.Dropdown(options=['A','B','C','D','A1'],value='A',  id='controls-khoi'),
#     dcc.Graph(figure={}, id='khoi-graph')
# ])

app.layout = html.Div([
    html.Div(className='row', children='Biggest title',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.Dropdown(options=[i for i in range(2017,2023)],value=2022,  id='controls-year')
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=['Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh','Lich su', 'Dia ly', 'GDCD'],value='Toan',  id='controls-mon'),
            dcc.Graph(figure={}, id='mon-graph')
        ]),
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=['A','B','C','D','A1'],value='A',  id='controls-khoi'),
            dcc.Graph(figure={}, id='khoi-graph')
        ])
    ])
])


# Add controls to build the interaction
@callback(
    Output(component_id='mon-graph', component_property='figure'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_mon(mon_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[mon_chosen].isnull()]
    if mon_chosen=='Van':
        data_output= (data[mon_chosen]*4).round()/4
        data_output=data_output.value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo mon",text_auto=True)
    else:
        data_output= data[mon_chosen].value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo mon",text_auto=True)
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90)
    fig.update_traces(
    textposition='inside',textfont=dict(
        size=100),textangle = 90)
    # annotations = []
    # for country, population in zip(data_output["Diem"], data_output["counts"]):
    #     annotations.append(dict(xref='Diem', yref='Diem', x=population+3, y=country,
    #                             text='{:,}'.format(population), font=dict(size=12),
    #                             showarrow=False))
    # fig.update_layout(annotations=annotations)
    return fig

@callback(
    Output(component_id='khoi-graph', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_khoi(khoi_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1).apply(lambda x: round(x*2)/2)
    data_output = data.Diem.value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    print(data_output.head())
    fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo khoi",text_auto=True)
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90)
    fig.update_traces(
    textposition='inside',textfont=dict(
        size=100),textangle = 90)
    # print(data_output)
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    