import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

path=r"./lab3-datasets/google-play-store-apps/googleplaystore.csv"
df = pd.read_csv(path)

categories = df['Category'].unique()
types=['Free','Paid','All']
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
            animate=True),
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

    # rating-price折线图 和 installs-size折线图
    html.Div([
        html.Div([
            dcc.Graph(
                id='rating-price',
                animate=True
            ),
        ],
        style={'width':'50%','display':'inline-block'}
        ),

        html.Div([
            dcc.Graph(
                id='installs-size',
                animate=True
            ),
        ],
        style={'width':'50%','display': 'inline-block'}
        ),
    ]),

    # reviews-installs, rating-installs, rating-reviews 散点图
    html.Div([
        html.Div([
        dcc.Graph(
            id='reviews-installs',
            animate=True
        ),
        ],
            style={'width':'30%','display':'inline-block'}
        ),

html.Div([
        dcc.Graph(
            id='rating-installs',
            animate=True
        ),],
    style={'width':'30%','display':'inline-block'}),

        html.Div([
        dcc.Graph(
            id='rating-reviews',
            animate=True
        )],
            style={'width':'30%','display':'inline-block'})
    ]),

])

# 通用散点图绘制
def create_scatter(x_values, x_title, y_values, y_title,text):
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
                margin={
                    'l': 40,
                    'b': 30,
                    't': 10,
                    'r': 0
                },
                height=450,
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
    print(category,type)
    dff=df[(df['Category']==category) & (df['Type']==type)]

    content_rating_list=list(content_rates)
    content_rating_values=[]
    for i in range(len(content_rating_list)):
        content_rating_values.append(0)
    for index,row in dff.iterrows():
        print(row['Content Rating'],content_rating_list.index(row['Content Rating']))
        content_rating_values[content_rating_list.index(row[8])]+=1
    print(content_rating_values)

    trace=go.Pie(
        labels=content_rating_list,
        values=content_rating_values
    )
    return {
        'data':[trace],
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

# rating-price散点图
@app.callback(
    dash.dependencies.Output('rating-price', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RP_series(category, type, radio):
    print(category,type,radio)
    dff = df[(df['Category'] == category) & (df['Content Rating']==radio)]

    ratings,prices,names=[],[],[]
    for index, row in dff.iterrows():
        ratings.append(row['Rating'])
        prices.append(row['Price'])
        names.append(row['App'])

    return {
        'data': [
            go.Scatter(
                x=prices,
                y=ratings,
                text=names,
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
                    'title': 'Price',
                },
                yaxis={
                    'title': 'Rating',
                },
                margin={
                    'l': 40,
                    'b': 30,
                    't': 10,
                    'r': 0
                },
                height=450,
                hovermode='closest')
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
    print(category,type,radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)]

    installs,sizes=[],[]
    for index,row in dff.iterrows():
        installs.append(row['Installs'])
        sizes.append(row['Size'])

    return {
        'data': [{
            "x": sizes,  # x轴为软件价格分类
            "y": installs,  # y轴为软件价格列表
            "mode": "lines+markers",
            'type': 'Scatter',
            'name': 'Line'
        }],
        'layout':
            go.Layout(
                margin={
                    'l': 130,
                    'b': 50,
                    't': 50,
                    'r': 40
                },
                height=300,
                hovermode='closest')
    }

    # return {
    #     'data': [
    #         go.Scatter(
    #             x=sizes,
    #             y=installs,
    #             mode='markers',
    #             marker={
    #                 'size': 15,
    #                 'opacity': 0.5,
    #                 'line': {
    #                     'width': 0.5,
    #                     'color': 'white'
    #                 }
    #             }
    #         )
    #     ],
    #     'layout':
    #         go.Layout(
    #             xaxis={
    #                 'title': 'Size',
    #             },
    #             yaxis={
    #                 'title': 'Installs',
    #             },
    #             margin={
    #                 'l': 40,
    #                 'b': 30,
    #                 't': 10,
    #                 'r': 0
    #             },
    #             height=450,
    #             hovermode='closest')
    # }

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

    return create_scatter(installs, 'Installs',reviews,'Reivews',names)

# rating-installs散点图
@app.callback(
    dash.dependencies.Output('rating-installs', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RI_scatters(category, type, radio):
    print(category, type, radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]

    ratings,installs,names=[],[],[]
    for index, row in dff.iterrows():
        ratings.append(row['Rating'])
        installs.append(row['Installs'])
        names.append(row['App'])

    return create_scatter(installs, 'Installs',ratings,'Rating',names)


# rating-reviews散点图
@app.callback(
    dash.dependencies.Output('rating-reviews', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio','value')
    ]
)
def update_RI_scatters(category, type, radio):
    print(category, type, radio)
    dff = df[(df['Category'] == category) & (df['Content Rating'] == radio)&(df['Type']==type)]

    ratings,reviews,names=[],[],[]
    for index, row in dff.iterrows():
        ratings.append(row['Rating'])
        reviews.append(row['Reviews'])
        names.append(row['App'])

    return create_scatter(reviews, 'Review',ratings,'Rating',names)

# html.Div([
#         html.Div([
#             dcc.Graph(
#                 id='content-rating-graph',
#                 animate=True),
#                 ],
#             style={'display':'inline-block','width':'30%'}),
#
#         html.Div([
#             dcc.Tabs(id="tabs",children=[
#                 dcc.Tab(label="Rating",
#                         children=[
#                             html.Div([
#                                 dcc.Graph(
#                                     id='rating-wc',
#                                     animate=True),
#                             ],
#                             style={'display':'inline-block','width':'50%'})
#                         ]),
#                 dcc.Tab(label="Installs",
#                         children=[
#                             html.Div([
#                                 dcc.Graph(
#                                     id='installs-wc',
#                                     animate=True),
#                             ],
#                             style={'display': 'inline-block', 'width': '50%'})
#                         ]),
#             ]),
#             ],
# style={'display': 'inline-block', 'width': '50%'})
#
#     ])



# app.layout = html.Div([
#     html.Div([
#
#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-xaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Fertility rate, total (births per woman)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-xaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ],
#         style={'width': '49%', 'display': 'inline-block'}),
#
#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-yaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Life expectancy at birth, total (years)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-yaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
#     ], style={
#         'borderBottom': 'thin lightgrey solid',
#         'backgroundColor': 'rgb(250, 250, 250)',
#         'padding': '10px 5px'
#     }),
#
#     html.Div([
#         dcc.Graph(
#             id='crossfilter-indicator-scatter',
#             hoverData={'points': [{'customdata': 'Japan'}]}
#         )
#     ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#     html.Div([
#         dcc.Graph(id='x-time-series'),
#         dcc.Graph(id='y-time-series'),
#     ], style={'display': 'inline-block', 'width': '49%'}),
#
#     html.Div(dcc.Slider(
#         id='crossfilter-year--slider',
#         min=df['Year'].min(),
#         max=df['Year'].max(),
#         value=df['Year'].max(),
#         step=None,
#         marks={str(year): str(year) for year in df['Year'].unique()}
#     ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
# ])

# @app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])
#
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]
#
#     return {
#         'data': [go.Scatter(
#             x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#             text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             mode='markers',
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'}
#             }
#         )],
#         'layout': go.Layout(
#             xaxis={
#                 'title': xaxis_column_name,
#                 'type': 'linear' if xaxis_type == 'Linear' else 'log'
#             },
#             yaxis={
#                 'title': yaxis_column_name,
#                 'type': 'linear' if yaxis_type == 'Linear' else 'log'
#             },
#             margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
#             height=450,
#             hovermode='closest'
#         )
#     }
#
# def create_time_series(dff, axis_type, title):
#     return {
#         'data': [go.Scatter(
#             x=dff['Year'],
#             y=dff['Value'],
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 225,
#             'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }],
#             'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
#             'xaxis': {'showgrid': False}
#         }
#     }
#
# @app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)
#
# @app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)
#
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')