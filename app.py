from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 1. Initialize Dash
app = Dash(__name__)

# 2. Load & Clean Data
df = pd.read_csv("formatted_data.csv")

# Force clean sales column to ensure it's a number
if df['sales'].dtype == 'object':
    df['sales'] = df['sales'].astype(str).str.replace(r'[\$,]', '', regex=True).str.strip()
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")

# 3. UI Layout with clean CSS
app.layout = html.Div(style={'backgroundColor': '#f0f2f5', 'minHeight': '100vh', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'}, children=[
    
    # Professional Header
    html.Div(style={
        'backgroundColor': '#1a2a6c', 
        'padding': '30px', 
        'borderRadius': '12px', 
        'marginBottom': '25px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.2)'
    }, children=[
        html.H1("Pink Morsel Sales Analysis Dashboard", 
                style={'textAlign': 'center', 'color': 'white', 'margin': '0', 'textTransform': 'uppercase'})
    ]),

    # Region Filter Section
    html.Div(style={
        'textAlign': 'center', 
        'marginBottom': '25px', 
        'backgroundColor': 'white', 
        'padding': '15px', 
        'borderRadius': '10px',
        'border': '1px solid #dcdde1'
    }, children=[
        html.Label("Select Region: ", style={'fontWeight': 'bold', 'marginRight': '15px', 'fontSize': '18px'}),
        dcc.RadioItems(
            id='region-picker',
            options=[{'label': f' {i.capitalize()} ', 'value': i} for i in ['north', 'east', 'south', 'west', 'all']],
            value='all',
            inline=True,
            style={'display': 'inline-block', 'fontSize': '16px'}
        )
    ]),

    # Main Visualization
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='sales-graph')
    ]),

    # Insights Container
    html.Div(style={
        'marginTop': '30px', 
        'padding': '25px', 
        'backgroundColor': '#ffffff', 
        'borderRadius': '12px', 
        'borderTop': '8px solid #f39c12',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.05)'
    }, children=[
        html.H2("Soul Foods Business Insights", style={'color': '#1a2a6c', 'marginTop': '0'}),
        html.P("Our analysis focuses on the impact of the price hike implemented on January 15, 2021:"),
        html.Ul(style={'fontSize': '16px', 'lineHeight': '1.6', 'color': '#2f3640'}, children=[
            html.Li("The line chart confirms that revenue stayed consistent or improved post-price hike."),
            html.Li("Regional data indicates that customers are relatively price-insensitive to the Pink Morsel product."),
            html.Li("The increase from $3 to $5 successfully improved overall profitability across all areas.")
        ])
    ])
])

# 4. Callback for interactivity
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    # Filter data
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region.lower()]

    # Create line plot
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        title=f"Sales Performance Trend ({selected_region.upper()})",
        labels={"sales": "Total Sales (USD)", "date": "Date"},
        template="plotly_white"
    )
    
    # Styling the chart to make it clean
    fig.update_layout(
        transition_duration=300,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial", size=12, color="#2f3640")
    )
    fig.update_yaxes(tickprefix="$", gridcolor="#f5f6fa")
    fig.update_xaxes(gridcolor="#f5f6fa")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)