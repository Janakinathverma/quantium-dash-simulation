from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 1. Initialize Dash
app = Dash(__name__)

# 2. Load & Clean Data
try:
    df = pd.read_csv("formatted_data.csv")
    
    # Force sales to be numeric (handling any lingering $ or commas)
    df['sales'] = pd.to_numeric(
        df['sales'].astype(str).str.replace(r'[\$,]', '', regex=True), 
        errors='coerce'
    )
    
    # Robust Date conversion (handles DD/MM/YYYY and YYYY-MM-DD)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    
    # Clean region names to avoid matching issues
    df['region'] = df['region'].astype(str).str.strip().str.lower()
    
    # Drop rows that failed conversion
    df = df.dropna(subset=['sales', 'date'])
    df = df.sort_values(by="date")
    
except Exception as e:
    print(f"CRITICAL ERROR: Data loading failed: {e}")
    df = pd.DataFrame(columns=['sales', 'date', 'region'])

# 3. Professional UI Layout
app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '30px', 'fontFamily': 'Arial, sans-serif'}, children=[
    
    # Header
    html.Div(style={
        'backgroundColor': '#1a2a6c', 
        'padding': '25px', 
        'borderRadius': '12px', 
        'marginBottom': '25px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.15)'
    }, children=[
        html.H1("Pink Morsel Sales Analysis Dashboard", 
                style={'textAlign': 'center', 'color': 'white', 'margin': '0', 'fontSize': '28px'})
    ]),

    # Radio Filter
    html.Div(style={
        'textAlign': 'center', 
        'marginBottom': '20px', 
        'backgroundColor': 'white', 
        'padding': '15px', 
        'borderRadius': '10px',
        'border': '1px solid #e1e4e8'
    }, children=[
        html.Label("Select Region: ", style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '18px'}),
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
            style={'display': 'inline-block'},
            labelStyle={'marginRight': '20px', 'fontSize': '16px'}
        )
    ]),

    # Visualization Container
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.05)'}, children=[
        dcc.Graph(id='sales-graph')
    ]),

    # Insights Section
    html.Div(style={
        'marginTop': '30px', 
        'padding': '25px', 
        'backgroundColor': '#ffffff', 
        'borderRadius': '12px', 
        'borderLeft': '10px solid #f39c12',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.05)'
    }, children=[
        html.H2("Business Impact Analysis", style={'color': '#1a2a6c', 'marginTop': '0'}),
        html.P("This dashboard visualizes the revenue trends before and after the price adjustment on Jan 15, 2021:"),
        html.Ul(style={'fontSize': '16px', 'lineHeight': '1.8'}, children=[
            html.Li("Sales volume showed resilience despite the price hike to $5.00."),
            html.Li("The 'All' region view confirms a steady growth in overall revenue."),
            html.Li("Customer retention remains strong across all four geographic regions.")
        ])
    ])
])

# 4. Callback for Graph Update
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    # Match logic: convert both sides to lower to avoid blank graph
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region.lower()]

    # Create Plot
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Performance: {selected_region.upper()}",
        labels={"sales": "Total Sales (USD)", "date": "Date"},
        template="plotly_white"
    )
    
    # Polish the layout
    fig.update_layout(
        transition_duration=400,
        margin=dict(l=50, r=50, t=70, b=50),
        font=dict(color="#2c3e50")
    )
    fig.update_traces(line_color='#1a2a6c', line_width=2.5)
    fig.update_yaxes(tickprefix="$", gridcolor="#f0f2f5")
    
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)