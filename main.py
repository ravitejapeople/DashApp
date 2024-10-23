import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json

with open('data.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)

app = dash.Dash(__name__)
server = app.server

dark_bg = '#323A3B'
card_bg = '#425361'  
text_color = '#FFFFFF'  
highlight_color = '#00D8FF'  
border_radius = '10px'  
hover_color = '#47476b'

color_palette = px.colors.sequential.Teal  

app.layout = html.Div(style={'fontFamily': 'cursive, sans-serif', 'backgroundColor': dark_bg, 'padding': '20px'}, children=[
    html.H1("US State Demographics", 
            style={
                'fontFamily': 'monospace',
                'textAlign': 'center', 
                'color': text_color, 
                'fontSize': '36px', 
                'padding': '20px', 
                'borderRadius': border_radius,
                'marginBottom': '20px'
            }),
    
    html.Div(style={'width': '30%', 'margin': '0 auto'}, children=[        
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['State']],
            value=df['State'][0],
            clearable=False,
            style={
                'color': '#333',
                'fontFamily': 'cursive',
            }
        )
    ]),

    html.Div([
        html.Div([dcc.Graph(id='pie-chart')], 
                 style={'backgroundColor': card_bg, 'padding': '20px', 'borderRadius': border_radius, 'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([dcc.Graph(id='bar-chart')], 
                 style={'backgroundColor': card_bg, 'padding': '20px', 'borderRadius': border_radius, 'width': '48%', 'display': 'inline-block', 'margin': '1%'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),  

    html.Div([
        html.Div([dcc.Graph(id='race-bar-chart')], 
                 style={'backgroundColor': card_bg, 'padding': '20px', 'borderRadius': border_radius, 'width': '48%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([dcc.Graph(id='race-percentage-bar-chart')], 
                 style={'backgroundColor': card_bg, 'padding': '20px', 'borderRadius': border_radius, 'width': '48%', 'display': 'inline-block', 'margin': '1%'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}) 
])

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('race-bar-chart', 'figure'),
     Output('race-percentage-bar-chart', 'figure')],
    Input('state-dropdown', 'value')
)
def update_graphs(selected_state):
    state_data = df[df['State'] == selected_state].iloc[0]
    
    pie_fig = px.pie(
        values=[state_data['Hispanic'], state_data['NonHispanic']],
        names=['Hispanic', 'Non-Hispanic'],
        title=f'Hispanic vs Non-Hispanic Population in {selected_state}',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    bar_fig = px.bar(
        x=[state_data['State']],
        y=[state_data['Total']],
        title='Total Population',
        color_discrete_sequence=px.colors.qualitative.Vivid 
    )
    
    race_data = ['WhiteTotal', 'BlackTotal', 'IndianTotal', 'AsianTotal', 'OtherTotal']
    race_values = [state_data[race] for race in race_data]
    
    race_bar_fig = px.bar(
        x=race_data,
        y=race_values,
        title=f'Population Distribution by Race in {selected_state}',
        labels={'x': 'Race', 'y': 'Population'},
        color_discrete_sequence=px.colors.qualitative.Safe  
    )
    
    race_percentage_data = ['WhiteTotalPerc', 'BlackTotalPerc', 'IndianTotalPerc', 'AsianTotalPerc', 'OtherTotalPerc']
    race_percentage_values = [state_data[perc] for perc in race_percentage_data]
    
    race_percentage_bar_fig = px.bar(
        x=race_percentage_data,
        y=race_percentage_values,
        title=f'Population Percentage by Race in {selected_state}',
        labels={'x': 'Race', 'y': 'Percentage'},
        color_discrete_sequence=px.colors.qualitative.Prism  
    )
    
    for fig in [pie_fig, bar_fig, race_bar_fig, race_percentage_bar_fig]:
        fig.update_layout(
            plot_bgcolor=card_bg,  
            paper_bgcolor=card_bg,
            font_color=text_color,
            font_family='cursive'  
        )

    return pie_fig, bar_fig, race_bar_fig, race_percentage_bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)
