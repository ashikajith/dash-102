#- 'python dash_demo.py' to run -#

#--- CONFIG 1 ---#
#imports
from dash import Dash, html, dcc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output #for callbacks

#create app
app = Dash(__name__) #this is creating flask application

#define colors
colors = {'background':'#96b6ab', 'text':'#936c7c'}

#--- DATA ---#
#creating random data for scatter
np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

#read in .csv for graph callback
df = pd.read_csv('gapminderDataFiveYear.csv')

#--- DASHBOARD ELEMENTS ---#
#- Defined outside of app -#
#markdown block
markdown_text = '''
### Dash apps can be written in Markdown
Markdown includes syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
'''

#single callback connector from a core compn to a html compn
@app.callback(Output(component_id='div-sing-callb', component_property='children'), #decorator, affects children property inside empty div
            [Input(component_id='sing-callb',component_property='value')])
def update_output_div(input_value):
    return "You entered: {}".format(input_value)

#options for graph callback
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})

#update figure function for graph callback
@app.callback(Output('graph-callb', 'figure' ),
             Input('year-picker', 'value'))
def update_figure(selected_year):

    filtered_df = df[df['year']==selected_year] #data only for selected year from dropdown
    traces=[] #empty list to fill in for loop

    for contintent_name in filtered_df['continent'].unique():
        df_by_contintent = filtered_df[filtered_df['continent']==contintent_name]
        traces.append(go.Scatter(
            x = df_by_contintent['gdpPercap'],
            y = df_by_contintent['lifeExp'],
            mode = 'markers',
            opacity = 0.7,
            marker = {'size':15},
            name = contintent_name
            )
        )
    #return dict that goes inside graph call
    return {'data':traces,
            'layout':go.Layout(
                title='Life Exp against GDP',
                xaxis={'title':'GDP Per Cap',
                        'type':'log'
                },
                yaxis={'title':'Life Expectancy'
                }
            )
    }



#--- WEB APP ---#
app.layout = html.Div([ # < < this creates division in dashboard to insert objs
                        #below are 2 more divisions inside the main division
                        #they are used to break up spaces on the web page
                        html.H1('This is a heading',
                                style={
                                    'textAlign':'center',
                                    'color':colors['text']
                                    #styling for html components: we pass a style dictionary with CSS calls
                                }
                        ),
                        html.Div('This is a division',
                                style={
                                    'color':colors['text']
                                }
                        ),
                        #drop down
                        html.Label('Dropdown',
                                    style={
                                        'color':colors['text']
                                    }
                        ),
                        dcc.Dropdown(options=[
                                        {'label':'Bristol Massive',
                                        'value':'Bristol'},
                                        {'label':'Beantown',
                                        'value':'Boston'}
                                    ],
                                    value='Brsitol', #default value
                        ),
                        #markdown block
                        dcc.Markdown(markdown_text,
                        ),
                        #single callback
                        dcc.Input(id='sing-callb', #takes in some text
                                  value='Initial Text',
                                  type='text'
                        ),
                        html.Div(id='div-sing-callb' #an empty div
                        ),
                        #graph callback
                        dcc.Graph(id = 'graph-callb'
                        ),
                        dcc.Dropdown(id='year-picker',
                                     options=year_options,
                                     value=df['year'].min()
                        ),
                        #bar chart
                        dcc.Graph(id='bar chart',
                                    figure = {'data': [
                                                    {'x':[1,2,3], 'y':[2,4,5], 'type':'bar', 'name':'SF'},
                                        ],
                                        'layout':{
                                            'plot_bgcolour':colors['background'],
                                            'paper_bgcolor':colors['background'],
                                            'font':{'color':colors['text']},
                                            'title':'BAR'
                                            #styling for core components: we put it inside a 'layout' dictionary
                                        }
                                    }
                        ),
                        #scatterplot
                        dcc.Graph(  id='scatterplot',
                                    figure = {'data':[
                                                go.Scatter(
                                                    x=random_x,
                                                    y=random_y,
                                                    mode='markers',
                                                    marker = {
                                                        'size':12,
                                                        'color':'rgb(51,235,42)',
                                                        'symbol':'pentagon',
                                                        'line':{'width':2}
                                                    }
                                                )
                                        ],
                                                'layout':go.Layout(title='Scatter Plot',
                                                                    xaxis = {'title':'X-AXIS'}
                                                )
                                    }
                        )
    ],
    style={'backgroundColor':colors['background']}
)

#--- CONFIG 2 ---#
#run app
if __name__ == '__main__': #checks if youre running the script
    app.run_server(debug=True) #grabs application obj and runs server