from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# 1. Load data
df = pd.read_csv("formatted_data.csv")

# 2. Data Cleaning
if df['sales'].dtype == 'object':
    df['sales'] = df['sales'].astype(str).str.replace(r'[\$,]', '', regex=True).str.strip()
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

# 3. UI Layout
app.layout = html.Div(style={'backgroundColor': '#f4f7f6', 'minHeight': '100vh', 'padding': '40px', 'fontFamily': 'sans-serif'}, children=[
    
    # Header Section
    html.Div(style={
        'backgroundColor': '#2c3e50', 
        'padding': '30px', 
        'borderRadius': '15px', 
        'marginBottom': '30px',
        'boxShadow': '0 10px 20px rgba(0,0,0,0.15)'
    }, children=[
        html.H1("Soul Foods: Pink Morsel Sales Visualiser", 
                style={'textAlign': 'center', 'color': 'white', 'margin': '0'})
    ]),

    # Filter Section
    html.Div(style={'textAlign': 'center', 'marginBottom': '30px', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'}, children=[
        html.Label("Filter Analysis by Region: ", style={'fontWeight': 'bold', 'fontSize': '18px'}),
        dcc.RadioItems(
            id='region-picker',
            options=[{'label': f' {i.capitalize()} ', 'value': i} for i in ['north', 'east', 'south', 'west', 'all']],
            value='all',
            inline=True,
            style={'display': 'inline-block', 'marginLeft': '20px'}
        )
    ]),

    # Graph Section
    html.Div(style={'backgroundColor': 'white', 'padding': '25px', 'borderRadius': '15px', 'boxShadow': '0 8px 16px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='sales-graph')
    ]),

    # Insights Section (Chup-chaap insights yahan hain)
    html.Div(style={
        'marginTop': '40px', 
        'padding': '30px', 
        'backgroundColor': '#ffffff', 
        'borderRadius': '15px', 
        'borderLeft': '10px solid #27ae60',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.05)'
    }, children=[
        html.H2("Key Business Insights", style={'color': '#2c3e50', 'marginTop': '0'}),
        html.Ul(style={'fontSize': '16px', 'lineHeight': '1.8', 'color': '#4b5563'}, children=[
            html.Li("The price increase on January 15th, 2021, shows a steady increase in total sales revenue."),
            html.Li("Customer retention remained strong across all regions despite the $2.00 price hike."),
            html.Li("The product's resilience suggests that Pink Morsel has high brand loyalty.")
        ])
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
        title=f"Sales Performance Trend: {selected_region.upper()}",
        labels={"sales": "Total Sales (USD)", "date": "Timeline"},
        color_discrete_sequence=['#2980b9']
    )
    
    fig.update_layout(
        transition_duration=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    fig.update_yaxes(tickprefix="$")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)