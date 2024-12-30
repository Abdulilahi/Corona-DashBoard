import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import dash
# import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {
        "href":"https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        "rel":"stylesheet",
        "integrity":"sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3",
        "crossorigin":"anonymous"

    }
]

patients=pd.read_csv("IndividualDetails.csv")
total=patients.shape[0]
active=patients[patients["current_status"]=='Hospitalized'].shape[0]
recovered=patients[patients["current_status"]=='Recovered'].shape[0]
deceased=patients[patients["current_status"]=='Deceased'].shape[0]
migrated=patients[patients["current_status"]=='Migrated'].shape[0]

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'},
    {'label':'Migrated','value':'Migrated'}
]
daybyday=patients["diagnosed_date"].value_counts().reset_index()

patients['age'] = pd.to_numeric(patients['age'], errors='coerce')
patients = patients.dropna(subset=['age'])
labels = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
patients['age_group'] = pd.cut(patients['age'], bins=10, labels=labels)
df=patients["age_group"].value_counts().reset_index()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("CORONA VIRUS PANDEMIC", style={'color': '#fff', 'text-align': 'center','padding':'50px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases",className="text-light text-center"),
                    html.H4(total,className='text-light text-center')
                ], className="card-body")
            ], className="card bg-danger")
        ], className="col-sm",),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases",className="text-light text-center"),
                    html.H4(active,className="text-light text-center")
                ], className="card-body")
            ], className="card bg-info")
        ], className="col-sm"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases",className="text-light text-center"),
                    html.H4(recovered,className="text-light text-center")
                ], className="card-body")
            ], className="card bg-warning")
        ], className="col-sm"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths",className="text-light text-center"),
                    html.H4(deceased,className="text-light text-center")
                ], className="card-body")
            ], className="card bg-success")#style={'background-color': 'green', 'height': '100px', 'width': '200px'})
        ], className="col-sm"),
        # ], className="row"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Migrated",className="text-light text-center"),
                    html.H4(migrated,className="text-light text-center")
                ], className="card-body")
            ], className="card bg-secondary")#style={'background-color': 'green', 'height': '100px', 'width': '200px'})
        ], className="col-sm")
        ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(id="bar-graph",figure={'data':[go.Bar(x=daybyday["diagnosed_date"],y=daybyday["count"])],'layout':go.Layout(title='Day To Day Analysis',xaxis={'title':'No of Cases'},yaxis={'title':'dates'})})
        ],className="col-md-6",style={'padding':'30px'}),
        html.Div([
            dcc.Graph(id="pie-graph",figure={'data':[go.Pie(values=df['count'],labels=df['age_group'])],'layout':go.Layout(title='AgeGroups')})
        ],className="col-md-6",style={'padding':'30px'}),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="picker",options=options,value='All'),
                    dcc.Graph(id="bar")
                ],className="card-body")
            ],className="card")
        ],className="col-md-12")
    ], className="row",style={'padding':'30px'} )
], className='container')


@app.callback(Output('bar', 'figure'), [Input("picker", 'value')])
def update_graph(type):
    if type == 'All':
        pbar = patients["detected_state"].value_counts().reset_index()
        pbar.columns = ['detected_state', 'count']
        return {'data': [go.Bar(x=pbar["detected_state"],y=pbar['count'])],
                'layout': go.Layout(title="State Total Count")}
    else:
        # Filter the dataset based on the selected status
        npat = patients[patients["current_status"] == type]

        # Get the value counts for "detected_state" after filtering by type
        pbar = npat["detected_state"].value_counts().reset_index()

        pbar.columns = ['detected_state', 'count']
        return {'data': [go.Bar(x=pbar["detected_state"],y=pbar['count'])],
                'layout': go.Layout(title=f"{type} State Count")}


if __name__ == "__main__":
    app.run_server(debug=True)
