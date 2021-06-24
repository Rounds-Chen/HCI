import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

path=r"./lab3-datasets/google-play-store-apps/googleplaystore.csv"
df = pd.read_csv(path)

categories = df['Category'].unique()
types=['Free','Paid']
content_rates=df['Content Rating'].unique()

app.layout=html.Div([
    # category
    html.Div([
        dcc.Dropdown(
            id="Category",
            options=[{'label': i, 'value': i} for i in categories],
            value='ART_AND_DESIGN'
        )],
        style={'width': '30%', 'display': 'inline-block','padding':'10px 50px'}),

    # type
    html.Div([
        dcc.Dropdown(
            id="Type",
            options=[{'label': i, 'value': i} for i in types],
            value='Free'
        )],
        style={'width': '30%', 'display': 'inline-block', 'padding': '10px 50px'}),

    # content-rating 饼状图
    html.Div([
        dcc.Graph(
            id='content-rating-graph',
            animate=False),
            ],
        style={'width':'50%'}),


    # content-rating radio-items
    html.Div([
        dcc.RadioItems(
            id='content-rating-radio',
            options=[
                {'label':i,'value':i} for i in content_rates
            ],
            value='Everyone',
            labelStyle={'padding':'0 20px','display': 'inline-block'}
        )
    ],
    style={'padding':'10px 50px','margin':'0 auto'}),

    # reviews-installs散点图 和 installs-size折线图
    html.Div([

html.Div([
        dcc.Graph(
            id='reviews-installs',
            animate=True
        ),
        ],
            style={'width':'40%','margin-top':'40px','display':'inline-block'}
        ),

        html.Div([
            dcc.Graph(
                id='installs-size',
                animate=True
            ),
        ],
        style={'width':'40%','margin-top':'40px','display': 'inline-block'}
        ),
    ]),

    # installs-rating, reviews-rating 柱状图
    html.Div([


html.Div([
        dcc.Graph(
            id='installs-rating',
            animate=True
        ),],
    style={'width':'40%','display':'inline-block','margin-top':'40px'}),

        html.Div([
        dcc.Graph(
            id='reviews-rating',
            animate=True
        )],
            style={'width':'40%','display':'inline-block','margin-top':'40px'})
    ]),

])

# 通用散点图绘制
def create_scatter(x_values, x_title, y_values, y_title,text,title):
    return {
        'data': [
            go.Scatter(
                x=x_values,
                y=y_values,
                text=text,
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {
                        'width': 0.5,
                        'color': 'white'
                    }
                })],
        'layout':
            go.Layout(
                xaxis={
                    'title': x_title,
                },
                yaxis={
                    'title': y_title,
                },
                title=title,
                margin={
                    'l': 130,
                    'b': 50,
                    't': 50,
                    'r': 40
                },
                height=500,
                hovermode='closest')
    }


# content-rating饼状图
@app.callback(
    dash.dependencies.Output('content-rating-graph','figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
    ])
def update_pie(category, type):
    dff=df[(df['Category']==category)&(df['Type']==type)]

    content_rating_list=list(content_rates)
    content_rating_values=[]
    for i in range(len(content_rating_list)):
        content_rating_values.append(0)
    for index,row in dff.iterrows():
        content_rating_values[content_rating_list.index(row[8])]+=1
    print('content_rating_values：',content_rating_values)

    print('更新饼图！')
    return {
        'data':[go.Pie(
        labels=content_rating_list,
        values=content_rating_values
    )],
        'layout':
            go.Layout(
                margin={
                    'l': 130,
                    'b': 30,
                    't': 50,
                    'r': 0
                },
                height=300,
                hovermode='closest'
            )
    }



# installs-size 折线图
@app.callback(
    dash.dependencies.Output('installs-size', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_IS_series(category,type,radio):
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]


    installs,sizes=[0,0,0,0,0,0,0,0],[]
    sizes = [
        '0~300k', '300k~600k', '600k~900k', '900k~25m', '25m~50m',
        '50m~75m', '75m~100m', 'Varies with device'
    ] # 单位m
    for index,row in dff.iterrows():
        print(row['Size'])
        if row['Size']=='Varies with device':
            installs[-1]+=row['Installs']
        elif row['Size'][-1]=='k':
            i=int(float(row['Size'][:-1])//300)
            print('软件大小：',row['Size'],'下标：',i)
            installs[i]+=row['Installs']
        else:
            i=int(float(row['Size'][:-1])//25)+3
            installs[i]+=row['Installs']
    print(installs)

    return {
        'data': [{
            "x": sizes,
            "y": installs,  
            "mode": "lines+markers",
            'type': 'Scatter',
            'name': 'Line'
        }],
        'layout':
            go.Layout(
                xaxis={
                    'title': 'Size',
                },
                yaxis={
                    'title': 'Installs',
                },
                title='Installs-Size',

                margin={
                    'l': 130,
                    'b': 50,
                    't': 50,
                    'r': 40
                },
                height=500,
                hovermode='closest')
    }


# reviews-installs散点图
@app.callback(
    dash.dependencies.Output('reviews-installs', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RI_scatters(category, type, radio):
    print(category, type, radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]


    reviews,installs,names=[],[],[]
    for index, row in dff.iterrows():
        reviews.append(row['Reviews'])
        installs.append(row['Installs'])
        names.append(row['App'])

    return create_scatter(installs, 'Installs',reviews,'Reivews',names,'Reviews-Installs')

# installs-rating柱状图
@app.callback(
    dash.dependencies.Output('installs-rating', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RI_scatters(category, type, radio):
    print(category, type, radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]



    installs=[0,0,0,0,0,0]
    ratings=['0~1','1~2','2~3','3~4','4~5','5+']
    for index, row in dff.iterrows():
        if not np.isnan(row['Rating']):
            installs[int(float(row['Rating']))]+=row['Installs']
    print(installs)

    return {
        'data': [
            go.Bar(
                x=ratings,
                y=installs,
            )
        ],
        'layout':
            go.Layout(
                xaxis={
                    'title': 'Rating',
                },
                yaxis={
                    'title': 'Installs',
                },
                title='Installs-Rating',
                margin={
                    'l': 130,
                    'b': 50,
                    't': 50,
                    'r': 40
                },
                height=500,
                hovermode='closest')
    }


# reviews-rating柱状图
@app.callback(
    dash.dependencies.Output('reviews-rating', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RI_scatters(category, type, radio):
    print(category, type, radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]

    reviews = [0, 0, 0, 0, 0,0]
    ratings = ['0~1', '1~2', '2~3', '3~4', '4~5','5+']
    for index, row in dff.iterrows():
        if not np.isnan(row['Rating']):
            reviews[int(float(row['Rating']))]+=row['Reviews']
    print(reviews)

    return {
        'data': [
            go.Bar(
                x=ratings,
                y=reviews,
            )
        ],
        'layout':
            go.Layout(
                xaxis={
                    'title': 'Rating',
                },
                yaxis={
                    'title': 'Reviews',
                },
                title='Reviews-Rating',
                margin={
                    'l': 130,
                    'b': 50,
                    't': 50,
                    'r': 40
                },
                height=500,
                hovermode='closest')
    }


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')