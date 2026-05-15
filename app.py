from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# 1. Load data
df = pd.read_csv("formatted_data.csv")

# 2. AGGRESSIVE DATA CLEANING
# Ensure sales is numerical. We strip whitespace, remove $, and convert.
if df['sales'].dtype == 'object':
    df['sales'] = df['sales'].astype(str).str.replace(r'[\$,]', '', regex=True).str.strip()
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

# 3. Date conversion
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

# UI Layout
app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '40px'}, children=[
    html.Div(style={
        'backgroundColor': '#2c3e50', 
        'padding': '20px', 
        'borderRadius': '10px', 
        'marginBottom': '30px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    }, children=[
        html.H1("Pink Morsel Sales Visualiser", 
                style={'textAlign': 'center', 'color': 'white', 'margin': '0', 'fontFamily': 'sans-serif'})
    ]),

    html.Div(style={'textAlign': 'center', 'marginBottom': '30px'}, children=[
        html.Label("Filter by Region: ", style={'fontWeight': 'bold', 'fontSize': '18px'}),
        dcc.RadioItems(
            id='region-picker',
            options=[
                {'label': ' North ', 'value': 'north'},
                {'label': ' East ', 'value': 'east'},
                {'label': ' South ', 'value': 'south'},
                {'label': ' West ', 'value': 'west'},
                {'label': ' All ', 'value': 'all'}
            ],
            value='all',
            inline=True,
            style={'display': 'inline-block', 'marginLeft': '10px'}
        )
    ]),

    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='sales-graph')
    ])
])

@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region.lower()]

    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Trend: {selected_region.capitalize()}",
        labels={"sales": "Total Sales ($)", "date": "Date"}
    )
    
    fig.update_layout(
        transition_duration=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0', tickprefix="$")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)