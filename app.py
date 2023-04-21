from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math

# Incorporate data
df = pd.read_csv('diem.csv')
Khoi_dict = {"A":['Toan', 'Ly', 'Hoa'],
             'B':['Toan', 'Hoa','Sinh'],
             'C':['Lich su', 'Dia ly', 'Van'],
             'D':['Toan', 'Van', 'Ngoai ngu'],
             'A1':['Toan','Ly','Ngoai ngu']}
To_hop_dict = {'KHTN':['Sinh', 'Ly', 'Hoa'],
               'KHXH':['Lich su', 'Dia ly', 'GDCD'],
               'both':['Sinh', 'Ly', 'Hoa','Lich su', 'Dia ly', 'GDCD']}

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
        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),
    
        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHTN', style={'fontWeight': 'bold', 'color': '#f73600','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHTN', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHXH', style={'fontWeight': 'bold', 'color': '#00aeef','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHXH', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHTN+KHXH', style={'fontWeight': 'bold', 'color': '#006600','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHTN + KHXH', style={'paddingTop': '.3rem','text-align':'center'}),
        
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi ít hơn 3 môn', style={'fontWeight': 'bold', 'color': '#660033','text-align':'center'}),
            html.Label('Tổng số sinh viên thi ít hơn 3 môn', style={'paddingTop': '.3rem','text-align':'center'}),
        
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

    ], style={'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

    # ]),
    html.Div(className='row', children=[
        html.Div(className='two columns', children=[
            html.Hr(),
            dash_table.DataTable(page_size=10, id='tabel_tinh',
                                #  style_cell={'padding': '5px'},
                                #  style_data={ 'border': '1px solid blue' }
                                 )
        ]),
        html.Div(className='five columns', children=[
            dcc.Graph(figure={}, id='mon_thi-graph')
            
        ]),
        html.Div(className='five columns', children=[
            dcc.Graph(figure={}, id='mon_khong_thi-graph')
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=['Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh','Lich su', 'Dia ly', 'GDCD'],value='Toan',  id='controls-mon'),
            dcc.Graph(figure={}, id='mon-graph'),
            dash_table.DataTable(page_size=10, id='tabel_mon')
            
        ]),
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=['A','B','C','D','A1'],value='A',  id='controls-khoi'),
            dcc.Graph(figure={}, id='khoi-graph'),
            dash_table.DataTable(page_size=10, id='tabel_khoi')
        ])
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='mon_line-graph')
            
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='khoi_line-graph')
        ])
    ])
])


# Add controls to build the interaction
@callback(
    [Output(component_id='Tổng số sinh viên thi', component_property='children'),
     Output('Tổng số sinh viên thi KHTN', 'children'),
     Output('Tổng số sinh viên thi KHXH', 'children'),
     Output('Tổng số sinh viên thi KHTN+KHXH', 'children'),
     Output('Tổng số sinh viên thi ít hơn 3 môn', 'children'),
    ],
    Input(component_id='controls-year', component_property='value')
)
def text_value(year_chosen):
    df1 = df[df['Year']==year_chosen]
    total = df1.shape[0]
    KHTN = df1[~df1[To_hop_dict['KHTN']].isnull().any(axis=1)].shape[0]
    KHXH = df1[~df1[To_hop_dict['KHXH']].isnull().any(axis=1)].shape[0]
    both = df1[~df1[To_hop_dict['both']].isnull().any(axis=1)].shape[0]
    null_fill = df1.isnull().sum(axis=1)
    less2 = null_fill[null_fill>6].shape[0]
    return total, KHTN, KHXH, both,less2

@callback(
    Output(component_id='tabel_tinh', component_property='data'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def table_tinh(mon_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    output= df1.MaTinh.value_counts().sort_values(ascending=False).head(10).reset_index()
    output.columns=['Tỉnh','Số thí sinh tham gia thi']
    return output.to_dict('records')

@callback(
    Output(component_id='mon_thi-graph', component_property='figure'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_monthi(year_chosen):
    df1 = df[df['Year']==year_chosen]
    df1 = df1[[ 'Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh', 'Lich su','Dia ly', 'GDCD']]
    output= df1.isnull().sum().reset_index()
    output.columns=['Môn','counts']
    output['counts']=df1.shape[0]-output['counts']
    fig=px.bar(output,x='counts',y='Môn',title='Số thí sinh thi các môn', orientation='h',template='none')
    fig.update_layout(
    yaxis=dict(categoryorder='total ascending'))
    return fig

@callback(
    Output(component_id='mon_khong_thi-graph', component_property='figure'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_monthi(year_chosen):
    df1 = df[df['Year']==year_chosen]
    df1 = df1[[ 'Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh', 'Lich su','Dia ly', 'GDCD']]
    output= 9-df1.isnull().sum(axis=1)
    output = output.value_counts().reset_index()
    output.columns=['Số môn thi','counts']
    fig=px.pie(output,values='counts',names='Số môn thi',title='Tỉ lệ thi số môn',template='none')
    fig.update_layout(
    legend_title='Tổng số môn thi',
    legend=dict(
        traceorder='normal',
        font=dict(size=12),
        borderwidth=1 ))
    return fig

@callback(
    Output(component_id='mon-graph', component_property='figure'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_mon(mon_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[mon_chosen].isnull()]
    if mon_chosen=='Van':
        # data_output= data[mon_chosen]
        # print(data_output)
        data_output= (data[mon_chosen]*4).round()/4
        data_output=data_output.value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo mon",text_auto=True,template='none')
    else:
        data_output= data[mon_chosen].value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo mon",text_auto=True,template='none')
        fig.update_layout(width=1000, height=500)
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
    Output(component_id='tabel_mon', component_property='data'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def table_mon(mon_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[mon_chosen].isnull()]
    output = pd.DataFrame({"Thống kê":['Tổng số thí sinh',
                                       'Điểm trung bình',
                                       'Số thí sinh đạt điểm <=1',
                                       'Số thí sinh đạt điểm dưới trung bình(<5)',
                                       'Số sinh viên đạt điểm >9',
                                       'Số điểm nhiều thí sinh đạt nhất'],
                            "Số lượng":[data.shape[0],
                                        data[mon_chosen].mean().round(2),
                                        data[data[mon_chosen]<=1].shape[0],
                                        data[data[mon_chosen]<5].shape[0],
                                        data[data[mon_chosen]>9].shape[0],
                                        data[mon_chosen].value_counts().sort_values(ascending=False).index[0]],
                            "Tỉ lệ":['',
                                     '',
                                        f'{round(((data[data[mon_chosen]<=1].shape[0]/data.shape[0])*100),2)}%',
                                        f'{round(((data[data[mon_chosen]<5].shape[0]/data.shape[0])*100),2)}%',
                                        f'{round(((data[data[mon_chosen]>9].shape[0]/data.shape[0])*100),2)}%',
                                     '']})
    return output.to_dict('records')

@callback(
    Output(component_id='khoi-graph', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def update_graph_khoi(khoi_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1).round()
    data_output = data.Diem.value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo khoi",text_auto=True,template='none')
    fig.update_layout(width=1000, height=500)
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90)
    fig.update_traces(
    textposition='inside',textfont=dict(
        size=10),textangle = 90)
    # print(data_output)
    return fig

@callback(
    Output(component_id='tabel_khoi', component_property='data'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-year', component_property='value')
)
def table_khoi(khoi_chosen,year_chosen):
    df1 = df[df['Year']==year_chosen]
    data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1).round()
    # print(data['Diem'])
    output = pd.DataFrame({"Thống kê":['Tổng số thí sinh',
                                       'Điểm trung bình',
                                       'Số thí sinh đạt điểm <=10',
                                       'Số sinh viên đạt điểm >=27',
                                       'Số sinh viên đạt điểm từ 16-30 điểm',
                                       'Số điểm nhiều thí sinh đạt nhất'],
                            "Số lượng":[data.Diem.shape[0],
                                        data.Diem.mean().round(2),
                                        data.Diem[data.Diem <=10].shape[0],
                                        data.Diem[data.Diem >=27].shape[0],
                                        data.Diem[data.Diem >=16].shape[0],
                                        data.Diem.value_counts().sort_values(ascending=False).index[0]],
                             "Tỉ lệ":['',
                                     '',
                                        f'{round(((data.Diem[data.Diem <=10].shape[0]/data.Diem.shape[0])*100),2)}%',
                                        f'{round(((data.Diem[data.Diem >=27].shape[0]/data.Diem.shape[0])*100),2)}%',
                                        f'{round(((data.Diem[data.Diem >=16].shape[0]/data.Diem.shape[0])*100),2)}%',
                                        '']
                            })
    return output.to_dict('records')

@callback(
    Output(component_id='mon_line-graph', component_property='figure'),
    Input(component_id='controls-mon', component_property='value')
)
def line_mon(mon_chosen):
    # df1 = df[df['Year']>=2020]
    df1 = df[~df[mon_chosen].isnull()]
    if mon_chosen=='Van':
        list_output=[]
        for i in range(2020,2023):
            data = df1[df1['Year']==i]
            data_output= (data[mon_chosen]*4).round()/4
            data_output=data_output.value_counts().reset_index()
            data_output.columns = ['Diem', 'counts']
            data_output = data_output.sort_values(by="Diem", ascending=True)
            data_output['Year']=i
            list_output.append(data_output)
        data_output=pd.concat(list_output)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2020]['Diem'], y=data_output[data_output['Year']==2020]['counts'],
                    mode='lines',
                    name='2020'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2021]['Diem'], y=data_output[data_output['Year']==2021]['counts'],
                    mode='lines',
                    name='2021'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2022]['Diem'], y=data_output[data_output['Year']==2022]['counts'],
                    mode='lines',
                    name='2022'))

    else:
        list_output=[]
        for i in range(2020,2023):
            data = df1[df1['Year']==i]
            data_output= data[mon_chosen].value_counts().reset_index()
            data_output.columns = ['Diem', 'counts']
            data_output = data_output.sort_values(by="Diem", ascending=True)
            data_output['Year']=i
            list_output.append(data_output)
        data_output=pd.concat(list_output)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2020]['Diem'], y=data_output[data_output['Year']==2020]['counts'],
                    mode='lines',
                    name='2020'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2021]['Diem'], y=data_output[data_output['Year']==2021]['counts'],
                    mode='lines',
                    name='2021'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2022]['Diem'], y=data_output[data_output['Year']==2022]['counts'],
                    mode='lines',
                    name='2022'))
    fig.update_layout(width=1000, height=500,template='none')
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90)
    return fig 

@callback(
    Output(component_id='khoi_line-graph', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value')
)
def line_khoi(khoi_chosen):
    list_output=[]
    for i in range(2020,2023):
        df1 = df[df['Year']==i]
        data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
        data['Diem'] = data.sum(axis=1).round()
        data_output = data.Diem.value_counts().reset_index()
        data_output = data_output.sort_values(by="Diem", ascending=True)
        data_output.columns = ['Diem', 'counts']
        data_output['Year']=i
        list_output.append(data_output)
    data_output=pd.concat(list_output)
    fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo khoi",text_auto=True,template='none')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2020]['Diem'], y=data_output[data_output['Year']==2020]['counts'],
                mode='lines',
                name='2020'))
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2021]['Diem'], y=data_output[data_output['Year']==2021]['counts'],
                mode='lines',
                name='2021'))
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2022]['Diem'], y=data_output[data_output['Year']==2022]['counts'],
                mode='lines',
                name='2022'))
    fig.update_layout(width=1000, height=500,template='none')
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90)
    return fig 

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)