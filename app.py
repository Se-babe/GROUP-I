import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("Life_Expectancy_Data.csv")
df.columns = df.columns.str.strip()
df["BMI"] = pd.to_numeric(df["BMI"], errors="coerce")

# Feature engineering
global_avg_life = df['Life expectancy'].mean()
highest_life_country = df.loc[df['Life expectancy'].idxmax()]['Country']
lowest_gdp_country = df.loc[df['GDP'].idxmin()]['Country']
highest_mortality_country = df.loc[df['Adult Mortality'].idxmax()]['Country']
latest_df = df.sort_values("Year").groupby("Country").tail(1)

# Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Life Expectancy Dashboard"

colors = {
    'primary': '#1e3a8a',
    'secondary': '#7c3aed',
    'accent': '#06b6d4',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'background': '#f8fafc',
    'card': '#ffffff',
    'text': '#1f2937',
    'text_light': '#6b7280'
}

card_style = {
    "padding": "20px",
    "margin": "10px 0",
    "borderRadius": "15px",
    "boxShadow": "0px 8px 25px rgba(0, 0, 0, 0.15)",
    "textAlign": "center",
    "color": "#ffffff",
    "border": "none"
}

app.layout = dbc.Container([
    html.H1("\ud83c\udf0d Life Expectancy Insights Dashboard By Group i", style={
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

    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Average Life Expectancy"),
            html.P(f"{global_avg_life:.2f} years", style={'fontSize': '1.5em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["success"]} 0%, {colors["accent"]} 100%)'}), xs=12, sm=6, md=3),

        dbc.Col(html.Div([
            html.H4("Highest Life Expectancy Country"),
            html.P(highest_life_country, style={'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["warning"]} 0%, {colors["success"]} 100%)'}), xs=12, sm=6, md=3),

        dbc.Col(html.Div([
            html.H4("Highest Adult Mortality"),
            html.P(highest_mortality_country, style={'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["danger"]} 0%, {colors["warning"]} 100%)'}), xs=12, sm=6, md=3),

        dbc.Col(html.Div([
            html.H4("Lowest GDP Country"),
            html.P(lowest_gdp_country, style={'fontSize': '1.3em', 'fontWeight': 'bold'})
        ], style={**card_style, 'background': f'linear-gradient(135deg, {colors["secondary"]} 0%, {colors["primary"]} 100%)'}), xs=12, sm=6, md=3)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Select Country:", style={
                "fontWeight": "bold", "fontSize": "18px", "color": colors['primary']
            }),
            dcc.Dropdown(
                options=[{"label": c, "value": c} for c in sorted(df["Country"].unique())],
                value="Uganda",
                id="country-dropdown",
                placeholder="Choose a country",
                style={"fontSize": "16px", "borderRadius": "10px", "border": f"2px solid {colors['accent']}"}
            )
        ], width=12)
    ], className="mb-4"),

    dbc.Row([dbc.Col(dcc.Graph(id="life-expectancy-trend"), width=12)]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="scatter-gdp-schooling"), xs=12, md=6),
        dbc.Col(dcc.Graph(id="heatmap-correlation"), xs=12, md=6)
    ], className="mb-4"),

    dbc.Row([dbc.Col(dcc.Graph(id="ranked-life-expectancy"), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(
        id="choropleth-map",
        figure=px.choropleth(
            latest_df,
            locations="Country",
            locationmode="country names",
            color="Life expectancy",
            title=" Life Expectancy by Country (Choropleth)",
            color_continuous_scale="Plasma"
        )
    ), width=12)]),

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
], fluid=True, style={
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
