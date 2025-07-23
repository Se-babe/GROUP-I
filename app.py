import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("Life_Expectancy_Data.csv")
df.columns = df.columns.str.strip()
df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce")

# Feature engineering: Calculate global stats
global_avg_life = df['Life expectancy'].mean()
highest_life_country = df.loc[df['Life expectancy'].idxmax()]['Country']
lowest_gdp_country = df.loc[df['GDP'].idxmin()]['Country']
highest_mortality_country = df.loc[df['Adult Mortality'].idxmax()]['Country']

# Latest year data for choropleth map
latest_df = df.sort_values("Year").groupby("Country").tail(1)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = " Life Expectancy Dashboard"

# Enhanced color palette
colors = {
    'primary': '#1e3a8a',      # Deep blue
    'secondary': '#7c3aed',    # Purple
    'accent': '#06b6d4',       # Cyan
    'success': '#10b981',      # Green
    'warning': '#f59e0b',      # Amber
    'danger': '#ef4444',       # Red
    'background': '#f8fafc',   # Light gray-blue
    'card': '#ffffff',         # White
    'text': '#1f2937',         # Dark gray
    'text_light': '#6b7280'    # Light gray
}

card_style = {
    "background": f"linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%)",
    "padding": "20px",
    "margin": "10px",
    "borderRadius": "15px",
    "boxShadow": "0px 8px 25px rgba(0, 0, 0, 0.15)",
    "textAlign": "center",
    "width": "22%",
    "color": "#ffffff",
    "border": "none"
}

# Layout
app.layout = html.Div([
    html.H1("🌍 Life Expectancy Insights Dashboard By Group i", style={
        'textAlign': 'center',
        'background': f'linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%)',
        'color': '#ffffff',
        'padding': '25px',
        'marginBottom': '30px',
        'borderRadius': '20px',
        'boxShadow': '0px 10px 30px rgba(0, 0, 0, 0.2)',
        'fontSize': '2.5em',
        'fontWeight': 'bold'
    }),

    # Summary cards
    html.Div([
        html.Div([
            html.H4("Average Life Expectancy", style={'color': '#ffffff', 'fontSize': '1.1em'}),
            html.P(f"{global_avg_life:.2f} years", style={'color': '#ffffff', 'fontSize': '1.5em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["success"]} 0%, {colors["accent"]} 100%)'}),

        html.Div([
            html.H4(" Highest Life Expectancy Country", style={'color': '#ffffff', 'fontSize': '1.1em'}),
            html.P(highest_life_country, style={'color': '#ffffff', 'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["warning"]} 0%, {colors["success"]} 100%)'}),

        html.Div([
            html.H4(" Highest Adult Mortality", style={'color': '#ffffff', 'fontSize': '1.1em'}),
            html.P(highest_mortality_country, style={'color': '#ffffff', 'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["danger"]} 0%, {colors["warning"]} 100%)'}),

        html.Div([
            html.H4("Lowest GDP Country", style={'color': '#ffffff', 'fontSize': '1.1em'}),
            html.P(lowest_gdp_country, style={'color': '#ffffff', 'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["secondary"]} 0%, {colors["primary"]} 100%)'})
    ], style={"display": "flex", "justifyContent": "space-around"}),

    html.Br(),

    html.Div([
        html.Label("Select Country:", style={
            "fontWeight": "bold", 
            "fontSize": "18px", 
            "color": colors['primary'],
            "marginBottom": "10px"
        }),
        dcc.Dropdown(
            options=[{"label": c, "value": c} for c in sorted(df["Country"].unique())],
            value="Uganda",
            id="country-dropdown",
            placeholder="Choose a country",
            style={
                "fontSize": "16px",
                "borderRadius": "10px",
                "border": f"2px solid {colors['accent']}"
            }
        ),
    ], style={
        "width": "50%", 
        "margin": "auto", 
        "marginBottom": "30px",
        "padding": "20px",
        "backgroundColor": colors['card'],
        "borderRadius": "15px",
        "boxShadow": "0px 5px 15px rgba(0, 0, 0, 0.1)"
    }),

    html.Br(),

    dcc.Graph(id="life-expectancy-trend", config={"displayModeBar": False}),

    html.Div([
        html.Div([
            dcc.Graph(id="scatter-gdp-schooling", config={"displayModeBar": False})
        ], style={"width": "50%", "padding": "10px"}),

        html.Div([
            dcc.Graph(id="heatmap-correlation", config={"displayModeBar": False})
        ], style={"width": "50%", "padding": "10px"})
    ], style={"display": "flex", "flexWrap": "wrap"}),

    html.Br(),

    html.Div([
        dcc.Graph(id="ranked-life-expectancy", config={"displayModeBar": False})
    ], style={"width": "100%", "padding": "10px"}),

    html.Br(),

    dcc.Graph(
        id="choropleth-map",
        figure=px.choropleth(
            latest_df,
            locations="Country",
            locationmode="country names",
            color="Life expectancy",
            title=" Life Expectancy by Country (Choropleth)",
            color_continuous_scale="Plasma"
        )
    ),

    html.Footer(
        "© 2025 Group i – Life Expectancy Analysis Dashboard | Makerere University",
        style={
            "textAlign": "center",
            "padding": "20px",
            "marginTop": "40px",
            "background": f"linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%)",
            "color": "#ffffff",
            "fontSize": "16px",
            "fontWeight": "bold",
            "borderRadius": "15px 15px 0 0"
        }
    )

], style={
    "padding": "20px",
    "background": f"linear-gradient(135deg, {colors['background']} 0%, #e0f2fe 100%)",
    "fontFamily": "Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
    "minHeight": "100vh"
})

@app.callback(Output("life-expectancy-trend", "figure"), Input("country-dropdown", "value"))
def update_life_expectancy_plot(selected_country):
    dff = df[df["Country"] == selected_country]
    fig = px.line(dff, x="Year", y="Life expectancy", title=f" Life Expectancy Over Time: {selected_country}", markers=True, line_shape="spline")
    fig.update_traces(line=dict(color=colors['primary'], width=4), marker=dict(size=8, color=colors['accent']))
    fig.update_layout(
        plot_bgcolor="#ffffff", 
        paper_bgcolor="#ffffff", 
        font=dict(color=colors['text'], size=12), 
        title_font_size=20,
        title_font_color=colors['primary'],
        xaxis=dict(gridcolor='#e5e7eb', linecolor=colors['text_light']),
        yaxis=dict(gridcolor='#e5e7eb', linecolor=colors['text_light']),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

@app.callback(Output("scatter-gdp-schooling", "figure"), Input("country-dropdown", "value"))
def scatter_gdp_schooling(_):
    fig = px.scatter_3d(df, x="GDP", y="Schooling", z="Life expectancy", color="Status", title="💰 GDP vs  Schooling vs  Life Expectancy", opacity=0.7)
    fig.update_layout(
        scene=dict(
            xaxis_title='GDP (USD)', 
            yaxis_title='Schooling (Years)', 
            zaxis_title='Life Expectancy (Years)',
            bgcolor='#f8fafc'
        ), 
        plot_bgcolor="#ffffff", 
        paper_bgcolor="#ffffff", 
        title_font_size=18,
        title_font_color=colors['primary'],
        font=dict(color=colors['text'])
    )
    fig.update_traces(marker=dict(size=5))
    return fig

@app.callback(Output("heatmap-correlation", "figure"), Input("country-dropdown", "value"))
def heatmap_correlation(_):
    corr = df.select_dtypes(include='number').corr()
    fig = px.imshow(corr, text_auto=True, title=" Correlation Heatmap", color_continuous_scale="RdYlBu_r", aspect="auto")
    fig.update_layout(
        title_font_size=18, 
        title_font_color=colors['primary'],
        xaxis_tickangle=45, 
        plot_bgcolor="#ffffff", 
        paper_bgcolor="#ffffff",
        font=dict(color=colors['text'])
    )
    return fig

@app.callback(Output("ranked-life-expectancy", "figure"), Input("country-dropdown", "value"))
def ranked_life_expectancy(_):
    latest = df.sort_values('Year').groupby('Country').tail(1)
    ranked = latest.sort_values('Life expectancy', ascending=False)
    fig = px.bar(ranked.head(20), x="Country", y="Life expectancy", color="Status", title="Countries Ranked by Life Expectancy (Latest Year)", text="Life expectancy")
    fig.update_layout(
        xaxis_tickangle=45, 
        plot_bgcolor="#ffffff", 
        paper_bgcolor="#ffffff", 
        title_font_size=18, 
        title_font_color=colors['primary'],
        font=dict(color=colors['text'])
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    return fig

if __name__ == "__main__":
    app.run(debug=True)