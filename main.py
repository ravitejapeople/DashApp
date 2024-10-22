import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json


with open('data.json') as f:
    data = json.load(f)


df = pd.DataFrame(data)

app = dash.Dash(__name__)
server=app.server

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'}, children=[
    html.H1("US State Demographics", style={'textAlign': 'center', 'color': '#333'}),
    
    html.Div(style={'margin': '20px 0'}),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in df['State']],
        value=df['State'][0], 
        clearable=False,
        style={'width': '50%', 'margin': '0 auto'}
    ),
    
    html.Div(style={'margin': '20px 0'}),
    
    html.H2("Demographic Distribution for Selected State", style={'textAlign': 'center'}),
    
    dcc.Graph(id='pie-chart', style={'display': 'inline-block', 'width': '48%'}),
    
    dcc.Graph(id='bar-chart', style={'display': 'inline-block', 'width': '48%'}),
    
    html.Div(style={'margin': '20px 0'}),
    
    dcc.Graph(id='race-bar-chart', style={'display': 'inline-block', 'width': '48%'}),
    
    dcc.Graph(id='race-percentage-bar-chart', style={'display': 'inline-block', 'width': '48%'}),
    
    html.Div(style={'margin': '20px 0'}),
    
    html.H2("Overall States Population Analysis", style={'textAlign': 'center'}),
    
    dcc.Graph(id='scatter-plot', style={'width': '100%', 'height': '400px'})
])

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('race-bar-chart', 'figure'),
     Output('race-percentage-bar-chart', 'figure'),
     Output('scatter-plot', 'figure')],
    Input('state-dropdown', 'value')
)
def update_graphs(selected_state):
    state_data = df[df['State'] == selected_state].iloc[0]
    
    pie_fig = px.pie(
        values=[state_data['Hispanic'], state_data['NonHispanic']],
        names=['Hispanic', 'Non-Hispanic'],
        title=f'Hispanic vs Non-Hispanic Population in {selected_state}'
    )
    
    bar_fig = px.bar(
        x=[state_data['State']], 
        y=[state_data['Total']],
        title='Total Population'
    )
    
    race_data = ['WhiteTotal', 'BlackTotal', 'IndianTotal', 'AsianTotal', 'OtherTotal']
    race_values = [state_data[race] for race in race_data]
    
    race_bar_fig = px.bar(
        x=race_data,
        y=race_values,
        title=f'Population Distribution by Race in {selected_state}',
        labels={'x': 'Race', 'y': 'Population'}
    )
    
    race_percentage_data = ['WhiteTotalPerc', 'BlackTotalPerc', 'IndianTotalPerc', 'AsianTotalPerc', 'OtherTotalPerc']
    race_percentage_values = [state_data[perc] for perc in race_percentage_data]
    
    race_percentage_bar_fig = px.bar(
        x=race_percentage_data,
        y=race_percentage_values,
        title=f'Population Percentage by Race in {selected_state}',
        labels={'x': 'Race', 'y': 'Percentage'}
    )

    scatter_fig = px.scatter(
        df,
        x='WhiteTotalPerc',  
        y='Total',         
        title='Total Population vs. Percentage of White Population (All States)',
        labels={'Total': 'Total Population', 'WhiteTotalPerc': 'Percentage of White Population'},
        hover_name='State'
    )

    return pie_fig, bar_fig, race_bar_fig, race_percentage_bar_fig, scatter_fig


if __name__ == '__main__':
    app.run_server(debug=True)
