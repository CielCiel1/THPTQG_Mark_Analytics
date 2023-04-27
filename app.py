from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
import pkg_resources

# Incorporate data
df = pd.read_csv('data_full.csv')
df = df[['SBD', 'Toan', 'Van', 'Ngoai ngu', 'Ly', 'Hoa', 'Sinh', 'Lich su','Dia ly', 'GDCD', 'MaTinh', 'Year']]
df.columns =[ 'SBD','Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD','Mã Tỉnh','Year']
tinh = pd.read_csv('Tinh.csv')
diemchuan=pd.read_csv('diemchuan.csv')
Khoi_dict = {"A00":['Toán', 'Lý', 'Hóa'],
             'B00':['Toán', 'Hóa','Sinh'],
             'C00':['Lịch sử', 'Địa lý', 'Văn'],
             'D01':['Toán', 'Văn', 'Ngoại ngữ'],
             'A01':['Toán','Lý','Ngoại ngữ']}
To_hop_dict = {'KHTN':['Sinh', 'Lý', 'Hóa'],
               'KHXH':['Lịch sử', 'Địa lý', 'GDCD'],
               'both':['Sinh', 'Lý', 'Hóa','Lịch sử', 'Địa lý', 'GDCD']}
tinh_dict = tinh.set_index('TenTinh').to_dict()['MaTinh']

dt = df[[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD','Year']].groupby('Year').agg('mean').round(2).reset_index()
dt["Year"] = dt['Year'].astype(str)
dt = dt.T.reset_index()
dt.columns = dt.iloc[0]
dt = dt[1:]

# print(df.head())
# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Initialize the app
# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(className='row', children='Phân tích điểm thi THPT Quốc gia',
             style={'textAlign': 'center', 'color': 'red', 'fontSize': 35}),
    
    html.Div(className='row', children=[
        dcc.Dropdown(options=[i for i in tinh_dict.keys()],value='Toàn Quốc',  id='controls-tinh', style={'marginRight':'10px','width':'100%'}),
        dcc.Dropdown(options=[i for i in range(2017,2023)],value=2022,  id='controls-year', style={'marginRight':'10px','width':'100%'})
    ]),
    html.Div(className='row', children='Phân tích tổng quan',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 25}),
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
        html.Div(className = 'one clomuns',children=[]),
        html.Div(className='three columns', children=[
            html.Br(),
            html.Br(),
            html.Label('Thống kê điểm trung bình qua các năm của toàn quốc',style={'fontWeight': 'bold', 'color': '#00aeef','text-align':'center'}),
            html.Br(),
            dash_table.DataTable(dt.to_dict('records'), [{"name": i, "id": i} for i in dt.columns]
                                #  style_cell={'padding': '5px'},
                                #  style_data={ 'border': '1px solid blue' }
                                 )
        ]),
        html.Div(className='eight columns', children=[
            dcc.Graph(figure={}, id='mon_thi-graph')
            
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure={},id='ti_le_diem')
        ]),
        html.Div(className='three columns', children=[
            dcc.Graph(figure={}, id='mon_khong_thi-graph')
        ])
    ]),
    html.Div(className='row', children='Phân tích phổ điểm',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 25}),
    html.Br(),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD'],value='Toán',  id='controls-mon'),
            dcc.Graph(figure={}, id='mon-graph'),
            dash_table.DataTable(page_size=10, id='tabel_mon')
            
        ]),
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=['A00','B00','C00','D01','A01'],value='A00',  id='controls-khoi'),
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
    ]),
    html.Div(className='row', children='Thống kê điểm chuẩn các trường Đại học',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 25}),
    html.Br(),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.I('Nhập tổng điểm của bạn:'),
            dcc.Input(id="Diem_cua_ban", type="number", placeholder='Nhập điểm của bạn',value=24, style={'marginRight':'10px','width':'10%'}),
            dcc.Input(id="Truong_cua_ban_b1", type="text", placeholder='Nhập trường bạn cần tìm', style={'marginRight':'10px','width':'32%'}),
            dcc.Input(id="Khoi_cua_ban_b1", type="text", placeholder='Nhập khối của bạn', style={'marginRight':'10px','width':'32%'}),
            html.Br(),
            html.I('* chỉ hiện thị điểm chuẩn nhỏ hơn hoặc bằng tổng điểm của bạn,(lưu ý khối A sẽ nhập A00, khối B : B00,.. )', style={'color':'red','font-size': '12px'}),
            html.Br(),
            html.Br(),
            html.Label('Tìm kiếm điểm chuẩn',style={'fontWeight': 'bold', 'color': '#00aeef','text-align':'center'}),
            dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},page_size=10, id='table_daihoc')
            # html.I('* chỉ hiện thị điểm chuẩn nhỏ hơn hoặc bằng tổng điểm của bạn', style={'color':'red','font-size': '12px'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Input(id="Truong_cua_ban_b2", type="text", placeholder='Nhập trường bạn cần tìm', style={'marginRight':'10px','width':'100%'}),
            # dcc.Input(id="Khoi_cua_ban_b2", type="text", placeholder='Nhập khối của bạn', style={'marginRight':'10px','width':'48%'}),
            html.Br(),
            html.I('* hiện thị điểm chuẩn của các trường trong khoảng +-3 điểm so với điểm trung bình của Khối', style={'color':'red','font-size': '12px'}),
            html.Br(),
            html.Br(),
            html.Label('So sánh phổ điểm theo khối và điểm chuẩn của các trường Đại Học',style={'fontWeight': 'bold', 'color': '#00aeef','text-align':'center'}),
            dash_table.DataTable(style_data={'whiteSpace': 'normal','height': 'auto',},page_size=10, id='table_trungbinh')
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
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def text_value(year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    total = df1.shape[0]
    KHTN = df1[~df1[To_hop_dict['KHTN']].isnull().any(axis=1)].shape[0]
    KHXH = df1[~df1[To_hop_dict['KHXH']].isnull().any(axis=1)].shape[0]
    both = df1[~df1[To_hop_dict['both']].isnull().any(axis=1)].shape[0]
    null_fill = df1.isnull().sum(axis=1)
    less2 = null_fill[null_fill>6].shape[0]
    return total, KHTN, KHXH, both,less2

@callback(
    Output(component_id='mon_thi-graph', component_property='figure'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def update_graph_monthi(year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    df1 = df1[[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD']]
    output= df1.isnull().sum().reset_index()
    output.columns=['Môn','counts']
    output['counts']=df1.shape[0]-output['counts']
    fig=px.bar(output,x='counts',y='Môn',title=f'Số thí sinh thi các môn {tinh_chosen} {year_chosen}', orientation='h',template='none')
    fig.update_layout(
    yaxis=dict(categoryorder='total ascending'))
    fig.update_traces(textposition='inside',textfont=dict(size=10))
    fig.update_yaxes(title = 'Môn thi')
    fig.update_xaxes(title = 'Tổng số sinh viên thi')
    return fig

@callback(
    Output(component_id='mon_khong_thi-graph', component_property='figure'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def update_graph_monthi(year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    df1 = df1[[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD']]
    output= 9-df1.isnull().sum(axis=1)
    output = output.value_counts().reset_index()
    output.columns=['Số môn thi','counts']
    custom_colors = ['#1B72C9', '#E65DE2', '#900C3F', '#581845']
    fig=px.pie(output,values='counts',names='Số môn thi',title=f'Tỉ lệ thi số môn năm {tinh_chosen} {year_chosen}',template='none', color_discrete_sequence = custom_colors)
    fig.update_layout(
    legend_title='Tổng số môn thi',width=500, height=450,
    legend=dict(
        traceorder='normal',
        font=dict(size=12)
         ))
    return fig

@callback(
    Output(component_id='ti_le_diem', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def update_graph_ti_le(khoi_chosen,year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1).round()
    data['Range_Điểm'] = np.where(data['Diem']<=15,'0-15',
                                  np.where(data['Diem']<=20,'15-20',
                                           np.where(data['Diem']<=24,'20-24',
                                                    np.where(data['Diem']<=27,'24-27',
                                                             '27-30'))))
    custom_colors = ['#1B72C9', '#E65DE2', '#900C3F', '#581845']
    data_output = data['Range_Điểm'].value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    fig = px.pie(data_output, values='counts', names='Diem', title=f"Tỉ lệ điểm theo khối {khoi_chosen}" ,template='none', color_discrete_sequence = custom_colors)
    fig.update_layout(
    legend_title='Tổng điểm khối thi',#width=500, height=500,
    legend=dict(
        traceorder='normal',
        font=dict(size=12)
         ))
    return fig

@callback(
    Output(component_id='mon-graph', component_property='figure'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def update_graph_mon(mon_chosen,year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    data = df1[~df1[mon_chosen].isnull()]
    if mon_chosen=='Văn':
        # data_output= data[mon_chosen]
        # print(data_output)
        data_output= (data[mon_chosen]*4).round()/4
        data_output=data_output.value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title=f"Phổ điểm theo môn {mon_chosen}",text_auto=True,template='none')
    else:
        data_output= data[mon_chosen].value_counts().reset_index()
        data_output.columns = ['Diem', 'counts']
        fig = px.bar(data_output, x='Diem', y='counts', title=f"Phổ điểm theo môn {mon_chosen}",text_auto=True,template='none')
        fig.update_layout(width=1000, height=500)
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90,title = 'Điểm')
    fig.update_traces(
    textposition='inside',textfont=dict(
        size=100),textangle = 90)
    fig.update_yaxes(title = 'Tổng số sinh viên')
    return fig

@callback(
    Output(component_id='tabel_mon', component_property='data'),
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def table_mon(mon_chosen,year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
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
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def update_graph_khoi(khoi_chosen,year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
    data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data['Diem'] = data.sum(axis=1).round()
    data_output = data.Diem.value_counts().reset_index()
    data_output.columns = ['Diem', 'counts']
    fig = px.bar(data_output, x='Diem', y='counts', title=f"Phổ điểm theo khối {khoi_chosen}",text_auto=True,template='none')
    fig.update_layout(width=1000, height=500)
    fig.update_xaxes(tickvals = data_output['Diem'].unique(), title = 'Điểm')
    fig.update_traces(
    textposition='inside',textfont=dict(
        size=10))
    # print(data_output)
    fig.update_yaxes(title = 'Tổng số sinh viên')
    return fig

@callback(
    Output(component_id='tabel_khoi', component_property='data'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def table_khoi(khoi_chosen,year_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[df_tinh['Year']==year_chosen]
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
    Input(component_id='controls-mon', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def line_mon(mon_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df.copy()
    df1 = df_tinh[~df_tinh[mon_chosen].isnull()]
    if mon_chosen=='Văn':
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
                    name='2020',line_shape='spline'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2021]['Diem'], y=data_output[data_output['Year']==2021]['counts'],
                    mode='lines',
                    name='2021',line_shape='spline'))
        fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2022]['Diem'], y=data_output[data_output['Year']==2022]['counts'],
                    mode='lines',
                    name='2022',line_shape='spline'))
        fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90, title = 'Điểm')
        fig.update_layout(
        legend=dict(
        orientation="h",
        yanchor="top",y=1.1)
        )
        fig.update_yaxes(title = 'Tổng số sinh viên')

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
        fig.update_layout(width=1000, height=500,template='none',title="So sánh phổ điểm của 3 năm gần nhất môn"
        )
        fig.update_xaxes(tickvals = data_output['Diem'].unique(),tickangle=90,title = 'Điểm')
        fig.update_layout(
        legend=dict(
        orientation="h",
        yanchor="top",y=1.1)
        )
        fig.update_yaxes(title = 'Tổng số sinh viên')
    return fig 

@callback(
    Output(component_id='khoi_line-graph', component_property='figure'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-tinh', component_property='value')
)
def line_khoi(khoi_chosen,tinh_chosen):
    if tinh_chosen !='Toàn Quốc':
        df1=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df1=df.copy()
    list_output=[]
    for i in range(2020,2023):
        df1 = df[df['Year']==i]
        data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
        data['Diem'] = data.sum(axis=1).round()
        data_output = data.Diem.value_counts().reset_index()
        # data_output = data_output.sort_values(by="Diem", ascending=True)
        data_output.columns = ['Diem', 'counts']
        data_output = data_output.sort_values(by="Diem", ascending=True)
        data_output['Year']=i
        list_output.append(data_output)
    data_output=pd.concat(list_output)
    fig = px.bar(data_output, x='Diem', y='counts', title="Pho diem theo khoi",text_auto=True,template='none')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2020]['Diem'], y=data_output[data_output['Year']==2020]['counts'],
                mode='lines',
                name='2020',line_shape='spline'))
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2021]['Diem'], y=data_output[data_output['Year']==2021]['counts'],
                mode='lines',
                name='2021',line_shape='spline'))
    fig.add_trace(go.Scatter(x=data_output[data_output['Year']==2022]['Diem'], y=data_output[data_output['Year']==2022]['counts'],
                mode='lines',
                name='2022',line_shape='spline'))
    fig.update_layout(width=980, height=500,template='none',title='So sánh phổ điểm của 3 năm gần nhất theo Khối')
    fig.update_xaxes(tickvals = data_output['Diem'].unique(),title = 'Điểm')
    fig.update_layout(
        legend=dict(
        orientation="h",
        yanchor="top",y=1.1)
        )
    fig.update_yaxes(title = 'Tổng số sinh viên')
    
    return fig 

@callback(
    Output(component_id='table_daihoc', component_property='data'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='Khoi_cua_ban_b1', component_property='value'),
    Input(component_id='Diem_cua_ban', component_property='value'),
    Input(component_id='Truong_cua_ban_b1', component_property='value')
)
def table_diemdaihoc(year_chosen,khoi_chosen,diem_cua_ban,truong_cua_ban):
    output = diemchuan[diemchuan['Điểm chuẩn']<=diem_cua_ban]
    if khoi_chosen!=None:
        output = output[output['Tổ hợp môn'].str.contains(khoi_chosen)]
    if truong_cua_ban!=None:
        output = output[output['Tên trường'].str.lower().str.contains(truong_cua_ban.lower())]
    output = output.sort_values('Điểm chuẩn',ascending=False)
    return output.to_dict('records')

@callback(
    Output(component_id='table_trungbinh', component_property='data'),
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='Truong_cua_ban_b2', component_property='value')
)
def table_diemtrungbinh(year_chosen,khoi_chosen,truong_cua_ban):
    if khoi_chosen in Khoi_dict.keys():
        df1 = df[df['Year']==year_chosen]
        data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
        data['Diem'] = data.sum(axis=1).round()
    else:
        df1 = df[df['Year']==year_chosen]
        data = df1[~df1[Khoi_dict['A00']].isnull().any(axis=1)][Khoi_dict['A00']]
        data['Diem'] = data.sum(axis=1).round()
    diem_cua_ban= data['Diem'].mean()
    diem_cua_ban_ab=diem_cua_ban+3
    diem_cua_ban_bl=diem_cua_ban-3
    output = diemchuan[(diemchuan['Điểm chuẩn']<=diem_cua_ban_ab)&(diemchuan['Điểm chuẩn']>=diem_cua_ban_bl)]
    if truong_cua_ban!=None:
        output = output[output['Tên trường'].str.lower().str.contains(truong_cua_ban.lower())]
    output = output.sort_values('Điểm chuẩn',ascending=False)
    return output.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# import pkg_resources
# installed_packages = pkg_resources.working_set
# installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
# print(installed_packages_list)