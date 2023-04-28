#Import library
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
dt=dt.rename(columns={'Year':'Năm'})
dt = dt[1:]

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
custom_colors = [ '#2C74B3','#19A7CE', '#82AAE3', '#91D8E4','#BFEAF5','#DFF6FF','#EAFDFC']

# Initialize the app
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(className='row', children='PHÂN TÍCH ĐIỂM THI THPT QUỐC GIA',
             style={'fontWeight': 'bold','textAlign': 'center', 'color': '#00aeef', 'fontSize': 35,'fontWeight': 'bold'}),
    
    html.Div(className='row', children=[
        dcc.Dropdown(options=[i for i in tinh_dict.keys()],value='Toàn Quốc',  id='controls-tinh', style={'marginRight':'10px','width':'100%'}),
        dcc.Dropdown(options=[i for i in range(2017,2023)],value=2022,  id='controls-year', style={'marginRight':'10px','width':'100%'})
    ]),
    html.Div(className='row', children='PHÂN TÍCH TỔNG QUAN',
             style={'fontWeight': 'bold','textAlign': 'center', 'color': '#00aeef', 'fontSize': 25}),
    html.Div(className='row', children=[
        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),
        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHTN', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHTN', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHXH', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHXH', style={'paddingTop': '.3rem','text-align':'center'}),
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi KHTN+KHXH', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi KHTN + KHXH', style={'paddingTop': '.3rem','text-align':'center'}),
        
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),   

        html.Div(children=[
            html.H3(id='Tổng số sinh viên thi ít hơn 3 môn', style={'fontWeight': 'bold','text-align':'center'}),
            html.Label('Tổng số sinh viên thi ít hơn 3 môn', style={'paddingTop': '.3rem','text-align':'center'}),
        
        ], className="two columns number-stat-box",style={'background-color':'#CCE5FF'}),

    ], style={'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

    # ]),
    html.Div(className='row', children=[
        html.Div(className = 'one clomuns',children=[]),
        html.Div(className='three columns', children=[
            html.Br(),
            html.Br(),
            html.Label('Thống kê điểm trung bình qua các năm toàn quốc',style={'fontWeight': 'bold','text-align':'center','fontSize':'17px'}),
            html.Br(),
            dash_table.DataTable(dt.to_dict('records'), [{"name": i, "id": i} for i in dt.columns],
                                style_header={'backgroundColor': '#CCE5FF','color': 'black','fontWeight': 'bold'},
                                style_cell_conditional=[{'if': {'column_id': 'Năm'},'textAlign': 'left','fontWeight': 'bold'}],
                                #  style_cell={'padding': '5px'},
                                style_data ={'font-size':'14px'}
                                 )
        ]),
        html.Div(className='eight columns', children=[
            dcc.Graph(figure={}, id='mon_thi-graph',style={"width": "100%","height": "100%","align" : "center"})
            
        ])
    ]),
    html.Div(children=[]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure={},id='ti_le_diem',style={"width": "100%","height": "100%",'display': 'flex', 'justify-content': 'center','margin-left':'25%'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='mon_khong_thi-graph',style={"width": "100%","height": "100%",'display': 'flex', 'justify-content': 'center','margin-left':'25%'})
        ])
    ]),
    html.Div(className='row', children='PHÂN TÍCH PHỔ ĐIỂM',
             style={'fontWeight': 'bold','textAlign': 'center', 'color': '#00aeef', 'fontSize': 25}),
    html.Br(),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD'],value='Toán',  id='controls-mon'),
            dcc.Graph(figure={}, id='mon-graph'),
            dash_table.DataTable(page_size=10, id='tabel_mon',style_header={'backgroundColor': '#CCE5FF','color': 'black','fontWeight': 'bold'},style_data ={'font-size':'14px'})
            
        ]),
        html.Div(className='six columns', children=[
            dcc.Dropdown(options=[i for i in Khoi_dict.keys()],value='A00',  id='controls-khoi'),
            dcc.Graph(figure={}, id='khoi-graph'),
            dash_table.DataTable(page_size=10, id='tabel_khoi',style_header={'backgroundColor': '#CCE5FF','color': 'black','fontWeight': 'bold'},style_data ={'font-size':'14px'})
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
    html.Div(className='row', children='THỐNG KÊ ĐIỂM CHUẨN CÁC TRƯỜNG ĐẠI HỌC',
             style={'fontWeight': 'bold','textAlign': 'center', 'color': '#00aeef', 'fontSize': 25}),
    html.Br(),
    html.Div(className='row', children=[
        html.Div(className='columns', children=[
            html.I('Nhập tổng điểm của bạn:'),
            dcc.Input(id="Diem_cua_ban", type="number", placeholder='Nhập điểm của bạn',value=24, style={'marginRight':'10px','width':'10%'}),
            dcc.Input(id="Truong_cua_ban_b1", type="text", placeholder='Nhập trường bạn cần tìm', style={'marginRight':'10px','width':'32%'}),
            dcc.Input(id="Khoi_cua_ban_b1", type="text", placeholder='Nhập khối của bạn', style={'marginRight':'10px','width':'32%'}),
            html.Br(),
            html.I('* chỉ hiện thị điểm chuẩn nhỏ hơn hoặc bằng tổng điểm của bạn,(lưu ý khối A sẽ nhập A00, khối B : B00,.. )', style={'color':'#00aeef','font-size': '12px'}),
            html.Br(),
            html.Br(),
            html.Label('Tìm kiếm điểm chuẩn',style={'fontWeight': 'bold','text-align':'center','fontSize':'17px'}),
            dash_table.DataTable(style_header={'backgroundColor': '#CCE5FF','color': 'black','fontWeight': 'bold'},style_data={'whiteSpace': 'normal','height': 'auto',},page_size=10,
                                 id='table_daihoc',style_cell={'fontSize': '14px'})
            # html.I('* chỉ hiện thị điểm chuẩn nhỏ hơn hoặc bằng tổng điểm của bạn', style={'color':'red','font-size': '12px'})
        ]),
    html.Div(className='row', children=[
        dcc.Input(id="Truong_cua_ban_b2", type="text", placeholder='Nhập trường bạn cần tìm', style={'width':'32%'}),
        dcc.Input(id="controls-sosanh", type="number", placeholder='Nhập số điểm chênh lệch so với điểm trung bình', style={'width':'25%'}),
        dcc.Input(id="controls-khoitrungbinh", type="text", placeholder='Nhập khối thi của bạn', style={'width':'30%'}),
        html.Br(),
        html.Label(id='chu thich',style={'color':'#00aeef','font-size': '12px'}),
        # html.I('* hiện thị điểm chuẩn của các trường trong khoảng +-3 điểm so với điểm trung bình của Khối', style={'color':'#00aeef','font-size': '12px'}),
        # html.Br(),
        html.Br(),
        html.Label('So sánh phổ điểm theo khối và điểm chuẩn của các trường Đại Học',style={'fontWeight': 'bold','text-align':'center','fontSize':'17px'}),
        dash_table.DataTable(style_header={'backgroundColor': '#CCE5FF','color': 'black','fontWeight': 'bold'},style_data={'whiteSpace': 'normal','height': 'auto',},
                                 page_size=10, id='table_trungbinh',style_cell={'fontSize': '14px'})
        ])
    ])
])

# Add controls to build the interaction
# All general analyst and spectrum
@callback(
    #Output
    Output(component_id='Tổng số sinh viên thi', component_property='children'),
    Output('Tổng số sinh viên thi KHTN', 'children'),
    Output('Tổng số sinh viên thi KHXH', 'children'),
    Output('Tổng số sinh viên thi KHTN+KHXH', 'children'),
    Output('Tổng số sinh viên thi ít hơn 3 môn', 'children'),
    Output(component_id='mon_thi-graph', component_property='figure'),
    Output(component_id='mon_khong_thi-graph', component_property='figure'),
    Output(component_id='ti_le_diem', component_property='figure'),
    Output(component_id='mon-graph', component_property='figure'),
    Output(component_id='tabel_mon', component_property='data'),
    Output(component_id='khoi-graph', component_property='figure'),
    Output(component_id='tabel_khoi', component_property='data'),
    Output(component_id='mon_line-graph', component_property='figure'),
    Output(component_id='khoi_line-graph', component_property='figure'),

    #Input
    Input(component_id='controls-year', component_property='value'),
    Input(component_id='controls-tinh', component_property='value'),
    Input(component_id='controls-khoi', component_property='value'),
    Input(component_id='controls-mon', component_property='value')
)

def define_value(year_chosen,tinh_chosen,khoi_chosen,mon_chosen):
    try:
        if tinh_chosen != None:
            tinh_chosen = tinh_chosen
        else:
            tinh_chosen = 'Toàn Quốc'
    except Exception as e:
        print(e)
        tinh_chosen = 'Toàn Quốc'
    if tinh_chosen =='Toàn Quốc' or tinh_chosen == None:
        df_tinh=df.copy()
        # df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    else:
        df_tinh=df[df['Mã Tỉnh']==tinh_dict[tinh_chosen]]
    df1 = df_tinh[df_tinh['Year']==year_chosen]

    #Text_value
    total = df1.shape[0]
    KHTN = df1[~df1[To_hop_dict['KHTN']].isnull().any(axis=1)].shape[0]
    KHXH = df1[~df1[To_hop_dict['KHXH']].isnull().any(axis=1)].shape[0]
    both = df1[~df1[To_hop_dict['both']].isnull().any(axis=1)].shape[0]
    null_fill = df1.isnull().sum(axis=1)
    less2 = null_fill[null_fill>6].shape[0]

    #Figure subject
    data_figire_subject= df1[[ 'Toán', 'Văn', 'Ngoại ngữ', 'Lý', 'Hóa', 'Sinh', 'Lịch sử','Địa lý', 'GDCD']].isnull().sum().reset_index()
    data_figire_subject.columns=['Môn','counts']
    data_figire_subject['counts']=df1.shape[0]-data_figire_subject['counts']
    fig_subject=px.bar(data_figire_subject,x='counts',y='Môn',title=f'<b>Số thí sinh thi các môn {tinh_chosen} {year_chosen}<b>', orientation='h',template='none')
    fig_subject.update_layout(font_family="Arial",
    yaxis=dict(categoryorder='total ascending'))
    fig_subject.update_traces(textposition='inside',textfont=dict(size=10))
    fig_subject.update_yaxes(title = '<b>Môn thi<b>')
    fig_subject.update_xaxes(title = '<b>Tổng số sinh viên thi<b>')

    #Figure number subject
    data_number_subject= 9-df1.isnull().sum(axis=1)
    data_number_subject = data_number_subject.value_counts().reset_index()
    data_number_subject.columns=['Số môn thi','counts']
    fig_number_subject=px.pie(data_number_subject,values='counts',names='Số môn thi',title=f'<b>Tỉ lệ thi số môn năm {tinh_chosen} {year_chosen}<b>',template='none', color_discrete_sequence = custom_colors,
                              hole=0.4)
    fig_number_subject.update_layout(legend_title='<b>Tổng số môn thi<b>',font_family="Arial",
                                  width=500, 
                                  legend=dict(traceorder='normal',font=dict(size=12))
                                  )
    
    #Figure range of block
    data_khoi = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
    data_khoi['Diem'] = data_khoi.sum(axis=1).round()
    data_khoi['Range_Điểm'] = np.where(data_khoi['Diem']<=15,'0-15',
                                  np.where(data_khoi['Diem']<=20,'15-20',
                                           np.where(data_khoi['Diem']<=24,'20-24',
                                                    np.where(data_khoi['Diem']<=27,'24-27',
                                                             '27-30'))))
    data_range_block = data_khoi['Range_Điểm'].value_counts().reset_index()
    data_range_block.columns = ['Diem', 'counts']
    fig_range_block = px.pie(data_range_block, values='counts', names='Diem', title=f"<b>Tỉ lệ điểm theo khối {khoi_chosen}<b>" ,template='none', color_discrete_sequence = custom_colors,hole=0.4)
    fig_range_block.update_layout(legend_title='<b>Tổng điểm khối thi<b>',font_family="Arial",width=500,
                                  legend=dict(traceorder='normal',font=dict(size=12))
                                  )
    
    #Figire subject bar
    data_mon = df1[~df1[mon_chosen].isnull()]
    if mon_chosen=='Văn':
        data_subject= (data_mon[mon_chosen]*4).round()/4
        data_subject=data_subject.value_counts().reset_index()
        data_subject.columns = ['Diem', 'counts']
    else:
        data_subject= data_mon[mon_chosen].value_counts().reset_index()
        data_subject.columns = ['Diem', 'counts']
    fig_subject_bar = px.bar(data_subject, x='Diem', y='counts', title=f"<b>Phổ điểm theo môn {mon_chosen}<b>",text_auto=True,template='none')
    fig_subject_bar.update_layout(font_family="Arial",#width=1000, height=500
                                  )
    fig_subject_bar.update_xaxes(tickvals = data_subject['Diem'].unique(),tickangle=90,title = '<b>Điểm<b>')
    fig_subject_bar.update_traces(
    textposition='inside',textfont=dict(
        size=100),textangle = 90)
    fig_subject_bar.update_yaxes(title = '<b>Tổng số sinh viên<b>')

    #Table subject
    table_subject = pd.DataFrame({"Thống kê":['Tổng số thí sinh',
                                       'Điểm trung bình',
                                       'Số thí sinh đạt điểm <=1',
                                       'Số thí sinh đạt điểm dưới trung bình(<5)',
                                       'Số sinh viên đạt điểm >9',
                                       'Số điểm nhiều thí sinh đạt nhất'],
                            "Số lượng":[data_mon.shape[0],
                                        round(data_mon[mon_chosen].mean(),2),
                                        data_mon[data_mon[mon_chosen]<=1].shape[0],
                                        data_mon[data_mon[mon_chosen]<5].shape[0],
                                        data_mon[data_mon[mon_chosen]>9].shape[0],
                                        data_mon[mon_chosen].value_counts().sort_values(ascending=False).index[0]],
                            "Tỉ lệ":['',
                                     '',
                                        f'{round(((data_mon[data_mon[mon_chosen]<=1].shape[0]/data_mon.shape[0])*100),2)}%',
                                        f'{round(((data_mon[data_mon[mon_chosen]<5].shape[0]/data_mon.shape[0])*100),2)}%',
                                        f'{round(((data_mon[data_mon[mon_chosen]>9].shape[0]/data_mon.shape[0])*100),2)}%',
                                     '']})
    #Figure block bar
    data_block = data_khoi.Diem.value_counts().reset_index()
    data_block.columns = ['Diem', 'counts']
    fig_block_bar = px.bar(data_block, x='Diem', y='counts', title=f"<b>Phổ điểm theo khối {khoi_chosen}<b>",text_auto=True,template='none')
    fig_block_bar.update_layout(font_family="Arial",#width=1000, height=500
                                )
    fig_block_bar.update_xaxes(tickvals = data_block['Diem'].unique(), title = '<b>Điểm<b>')
    fig_block_bar.update_traces(
    textposition='inside',textfont=dict(
        size=10))
    fig_block_bar.update_yaxes(title = '<b>Tổng số sinh viên<b>')

    #Table block
    table_block = pd.DataFrame({"Thống kê":['Tổng số thí sinh',
                                       'Điểm trung bình',
                                       'Số thí sinh đạt điểm <=10',
                                       'Số sinh viên đạt điểm >=27',
                                       'Số sinh viên đạt điểm từ 16-30 điểm',
                                       'Số điểm nhiều thí sinh đạt nhất'],
                            "Số lượng":[data_khoi.Diem.shape[0],
                                        data_khoi.Diem.mean().round(2),
                                        data_khoi.Diem[data_khoi.Diem <=10].shape[0],
                                        data_khoi.Diem[data_khoi.Diem >=27].shape[0],
                                        data_khoi.Diem[data_khoi.Diem >=16].shape[0],
                                        data_khoi.Diem.value_counts().sort_values(ascending=False).index[0]],
                             "Tỉ lệ":['',
                                     '',
                                        f'{round(((data_khoi.Diem[data_khoi.Diem <=10].shape[0]/data_khoi.Diem.shape[0])*100),2)}%',
                                        f'{round(((data_khoi.Diem[data_khoi.Diem >=27].shape[0]/data_khoi.Diem.shape[0])*100),2)}%',
                                        f'{round(((data_khoi.Diem[data_khoi.Diem >=16].shape[0]/data_khoi.Diem.shape[0])*100),2)}%',
                                        '']
                            })
    
    #Figure subject line
    list_output=[]
    for i in range(2020,2023):
        data = df[df['Year']==i]
        if mon_chosen=='Văn':
            data= (data[mon_chosen]*4).round()/4
        data_subject_line= data[mon_chosen].value_counts().reset_index()
        data_subject_line.columns = ['Diem', 'counts']
        data_subject_line = data_subject_line.sort_values(by="Diem", ascending=True)
        data_subject_line['Year']=i
        list_output.append(data_subject_line)
    data_subject_line=pd.concat(list_output)
    fig_subject_line = go.Figure()
    fig_subject_line.add_trace(go.Scatter(x=data_subject_line[data_subject_line['Year']==2020]['Diem'], y=data_subject_line[data_subject_line['Year']==2020]['counts'],
                mode='lines',
                name='2020'))
    fig_subject_line.add_trace(go.Scatter(x=data_subject_line[data_subject_line['Year']==2021]['Diem'], y=data_subject_line[data_subject_line['Year']==2021]['counts'],
                mode='lines',
                name='2021'))
    fig_subject_line.add_trace(go.Scatter(x=data_subject_line[data_subject_line['Year']==2022]['Diem'], y=data_subject_line[data_subject_line['Year']==2022]['counts'],
                mode='lines',
                name='2022'))
    fig_subject_line.update_layout(font_family="Arial",#width=1000, height=500,
                                   template='none',title="<b>So sánh phổ điểm của 3 năm gần nhất môn<b>"
    )
    fig_subject_line.update_xaxes(tickvals = data_subject_line['Diem'].unique(),tickangle=90,title = '<b>Điểm<b>')
    fig_subject_line.update_layout(
    legend=dict(
    orientation="h",
    yanchor="top",y=1.1)
    )
    fig_subject_line.update_yaxes(title = '<b>Tổng số sinh viên<b>')

    #Figure block line
    list_output=[]
    for i in range(2020,2023):
        df1 = df[df['Year']==i]
        data = df1[~df1[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
        data['Diem'] = data.sum(axis=1).round()
        data_block_line = data.Diem.value_counts().reset_index()
        data_block_line.columns = ['Diem', 'counts']
        data_block_line = data_block_line.sort_values(by="Diem", ascending=True)
        data_block_line['Year']=i
        list_output.append(data_block_line)
    data_block_line=pd.concat(list_output)
    fig_block_line = px.bar(data_block_line, x='Diem', y='counts', title="Pho diem theo khoi",text_auto=True,template='none')
    fig_block_line = go.Figure()
    fig_block_line.add_trace(go.Scatter(x=data_block_line[data_block_line['Year']==2020]['Diem'], y=data_block_line[data_block_line['Year']==2020]['counts'],
                mode='lines',
                name='2020',line_shape='spline'))
    fig_block_line.add_trace(go.Scatter(x=data_block_line[data_block_line['Year']==2021]['Diem'], y=data_block_line[data_block_line['Year']==2021]['counts'],
                mode='lines',
                name='2021',line_shape='spline'))
    fig_block_line.add_trace(go.Scatter(x=data_block_line[data_block_line['Year']==2022]['Diem'], y=data_block_line[data_block_line['Year']==2022]['counts'],
                mode='lines',
                name='2022',line_shape='spline'))
    fig_block_line.update_layout(font_family="Arial",#width=980, height=500,
                                 template='none',title='<b>So sánh phổ điểm của 3 năm gần nhất theo Khối<b>')
    fig_block_line.update_xaxes(tickvals = data_block_line['Diem'].unique(),title = '<b>Điểm<b>')
    fig_block_line.update_layout(
        legend=dict(
        orientation="h",
        yanchor="top",y=1.1)
        )
    fig_block_line.update_yaxes(title = '<b>Tổng số sinh viên<b>')
    return total, KHTN, KHXH, both, less2,fig_subject, fig_number_subject, fig_range_block, fig_subject_bar, table_subject.to_dict('records'), fig_block_bar, table_block.to_dict('records'), fig_subject_line, fig_block_line

#Statistics of benchmarks of universities

@callback(
    Output(component_id='table_daihoc', component_property='data'),
    # Input(component_id='controls-year', component_property='value'),
    Input(component_id='Khoi_cua_ban_b1', component_property='value'),
    Input(component_id='Diem_cua_ban', component_property='value'),
    Input(component_id='Truong_cua_ban_b1', component_property='value')
)
def table_diemdaihoc(khoi_chosen,diem_cua_ban,truong_cua_ban):
    output = diemchuan[diemchuan['Điểm chuẩn']<=diem_cua_ban]
    if khoi_chosen!=None:
        output = output[output['Tổ hợp môn'].str.contains(khoi_chosen)]
    if truong_cua_ban!=None:
        output = output[output['Tên trường'].str.lower().str.contains(truong_cua_ban.lower())]
    output = output.sort_values('Điểm chuẩn',ascending=False)
    return output.to_dict('records')

@callback(
    Output(component_id='table_trungbinh', component_property='data'),
    Output(component_id='chu thich', component_property='children'),
    # Input(component_id='controls-year', component_property='value'),
    Input(component_id ='controls-sosanh',component_property ='value'),
    Input(component_id='controls-khoitrungbinh', component_property='value'),
    Input(component_id='Truong_cua_ban_b2', component_property='value')
)
def table_diemtrungbinh(sosanh,khoi_chosen,truong_cua_ban):
    try:
        if khoi_chosen!=None:
            khoi_chosen = khoi_chosen
        else:
            khoi_chosen = 'A00'
    except Exception as e:
        print(e)
        khoi_chosen = 'A00'
    if khoi_chosen in Khoi_dict.keys():
        data = df[~df[Khoi_dict[khoi_chosen]].isnull().any(axis=1)][Khoi_dict[khoi_chosen]]
        data['Diem'] = data.sum(axis=1).round()
    else:
        data = df[~df[Khoi_dict['A00']].isnull().any(axis=1)][Khoi_dict['A00']]
        data['Diem'] = data.sum(axis=1).round()
    try:
        if sosanh!=None:
            sosanh = sosanh
        else:
            sosanh = 3
    except Exception as e:
        print(e)
        sosanh = 3
    diem_cua_ban= data['Diem'].mean()
    diem_cua_ban_ab=diem_cua_ban + sosanh
    diem_cua_ban_bl=diem_cua_ban - sosanh
    output = diemchuan[(diemchuan['Điểm chuẩn']<=diem_cua_ban_ab)&(diemchuan['Điểm chuẩn']>=diem_cua_ban_bl)]
    if truong_cua_ban!=None:
        output = output[output['Tên trường'].str.lower().str.contains(truong_cua_ban.lower())]
    output = output.sort_values('Điểm chuẩn',ascending=True)
    chu_thich = f'* Điểm trung bình của khối {khoi_chosen} năm 2022 là {round(diem_cua_ban,2)},(lưu ý khối A sẽ nhập A00, khối B : B00)'
    return output.to_dict('records'),chu_thich
if __name__ == '__main__': 
    app.run_server(debug=True)