import dash 
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Rutas de los archivos
file_path = r"C:\Users\malonso\Documents\NAC SPORT DATA\Dashboard\241102 Tuc Rugby vs Palermo Bajo.xlsx"
output_html_path = r"C:\Users\malonso\source\repos\rugby_dashboard.html"
logo_url = "https://www.clubpalermobajo.com.ar/wp-content/uploads/2015/05/logo_palermobajo.png"

# Intentar cargar los datos desde el archivo Excel
try:
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    df.columns = df.columns.str.strip()  # Limpiar espacios adicionales en los nombres de columnas
    df = df.set_index('Categorias/Variables')  # Establecer la primera columna como índice
except Exception as e:
    print(f"Error al cargar el archivo Excel: {e}")
    df = pd.DataFrame()  # Crear un DataFrame vacío en caso de error

# Filtrar la categoría "Totales" de los gráficos
df_sin_totales = df.drop("Totales", axis=0, errors='ignore')

# Calcular los porcentajes de Lineout y Scrum ganados
lineout_ganados = df_sin_totales.loc["Lineout propio", "Ganado"]
lineout_totales = df_sin_totales.loc["Lineout propio", "Ganado"] + df_sin_totales.loc["Lineout propio", "Perdido"]
porcentaje_lineout_ganado = int((lineout_ganados / lineout_totales * 100)) if lineout_totales != 0 else 0

scrum_ganados = df_sin_totales.loc["Scrum propio", "Ganado"]
scrum_totales = df_sin_totales.loc["Scrum propio", "Ganado"] + df_sin_totales.loc["Scrum propio", "Perdido"]
porcentaje_scrum_ganado = int((scrum_ganados / scrum_totales * 100)) if scrum_totales != 0 else 0

# Cálculos de los porcentajes para los gráficos
scrum_ganados_rival = df.loc['Scrum rival', 'Ganado']
scrum_totales_rival = df.loc['Scrum rival', 'Ganado'] + df.loc['Scrum rival', 'Perdido']


lineout_ganados_rival = df.loc['Lineout rival', 'Ganado']
lineout_totales_rival = df.loc['Lineout rival', 'Ganado'] + df.loc['Lineout rival', 'Perdido']


# Calcular los porcentajes
porcentaje_scrum_rival = int((scrum_ganados_rival / scrum_totales * 100)) if scrum_totales != 0 else 0
porcentaje_lineout_rival = int((lineout_ganados_rival / lineout_totales_rival * 100)) if lineout_totales_rival != 0 else 0


# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Crear un DataFrame filtrado sin las columnas "Ganado" y "Perdido"
df_filtrado = df.drop(columns=["Ganado", "Perdido"], errors="ignore")

# Layout del dashboard
app.layout = html.Div([
    # Logo
    html.Div([
        html.Img(src=logo_url, style={
            "height": "auto",
            "width": "100%",
            "maxWidth": "200px",
            "position": "absolute",
            "top": "10px",
            "left": "50%",
            "transform": "translateX(-50%)",
            "zIndex": 10
        })
    ], style={"width": "100%"}),

    # Título
    html.H1("Dashboard de Rugby", style={"textAlign": "center", "marginTop": "120px"}),
    html.H2("Plantel Superior", style={"textAlign": "center", "marginTop": "10px"}),

    # Filtros
    html.Div([
        html.Label("Selecciona una categoría:"),
        dcc.Dropdown(
            id="dropdown-variable",
            options=[{"label": col, "value": col} for col in df_sin_totales.index],
            value=df_sin_totales.index[0] if not df_sin_totales.empty else None,
            style={"width": "100%", "maxWidth": "500px", "margin": "auto"}
        )
    ], style={"textAlign": "center", "marginTop": "20px"}),

    html.Div([
        html.Label("Selecciona un periodo:"),
        dcc.Dropdown(
            id="dropdown-periodo",
            options=[{"label": "1er tiempo", "value": "1er tiempo"}, {"label": "2o tiempo", "value": "2o tiempo"}],
            value="1er tiempo",
            style={"width": "100%", "maxWidth": "500px", "margin": "auto"}
        )
    ], style={"textAlign": "center", "marginTop": "20px"}),

    # Resultado
    html.Div(id="resultado-burbuja", style={
        "backgroundColor": "#BDC3C7",
        "padding": "20px",
        "borderRadius": "10px",
        "textAlign": "center",
        "fontSize": "18px",
        "fontWeight": "bold",
        "width": "25%",
        "minWidth": "250px",
        "maxWidth": "300px",
        "marginTop": "20px",
        "marginLeft": "auto",
        "marginRight": "auto"
    }),

    # Gráficos
    dcc.Graph(id="bar-chart", style={"marginTop": "40px"}),

    # Reorganizamos los gráficos de torta
    html.Div([
        html.Div([
            html.H3("Efectividad Scrum", style={"textAlign": "center"}),
            dcc.Graph(id="scrum-pie", style={"marginTop": "20px"})
        ], style={"width": "48%", "display": "inline-block", "boxSizing": "border-box"}),

        html.Div([
            html.H3("Efectividad Lineout", style={"textAlign": "center"}),
            dcc.Graph(id="lineout-pie", style={"marginTop": "20px"})
        ], style={"width": "48%", "display": "inline-block", "boxSizing": "border-box"})
    ], style={"display": "flex", "justifyContent": "space-between", "marginTop": "40px"}),

    # Añadimos los gráficos de torta para los datos del rival
    html.Div([
        html.Div([
            html.H3("Obtención Rival - Scrum", style={"textAlign": "center"}),
            dcc.Graph(id="scrum-rival-pie", style={"marginTop": "20px"})
        ], style={"width": "48%", "display": "inline-block", "boxSizing": "border-box"}),

        html.Div([
            html.H3("Obtención Rival - Lineout", style={"textAlign": "center"}),
            dcc.Graph(id="lineout-rival-pie", style={"marginTop": "20px"})
        ], style={"width": "48%", "display": "inline-block", "boxSizing": "border-box"})
    ], style={"display": "flex", "justifyContent": "space-between", "marginTop": "40px"}),

    # Tabla
    html.Div([
        html.Table(
            [html.Tr([html.Th("Categorías/Variables", style={"backgroundColor": "#800000", "color": "#FFD700", "padding": "10px"})] +
                     [html.Th(col, style={"backgroundColor": "#800000", "color": "#FFD700", "padding": "10px"}) for col in df_filtrado.columns])] +
            [html.Tr([html.Td(idx, style={"fontWeight": "bold", "padding": "10px", "backgroundColor": "#F5F5F5"})] +
                     [html.Td(f"{int(row[col]):,}" if pd.notnull(row[col]) and isinstance(row[col], (int, float)) else "-", style={"padding": "10px"}) for col in df_filtrado.columns])
             for idx, row in df_filtrado.iterrows()],
            style={"width": "100%", "margin": "auto", "border": "1px solid black", "borderCollapse": "collapse"}
        )
    ], style={"marginTop": "20px"}),

    # Botón de exportación
    html.Div([
        html.Button("Exportar a HTML", id="export-button", n_clicks=0, style={
            "backgroundColor": "#800000",
            "color": "white",
            "padding": "15px 32px",
            "fontSize": "16px",
            "borderRadius": "8px",
            "border": "none",
            "cursor": "pointer",
            "marginTop": "20px"
        }),
        html.Div(id="export-status", style={"marginTop": "10px"})
    ], style={"textAlign": "center", "marginTop": "20px"})
])


# Callbacks para los gráficos y la exportación
@app.callback(
    [Output("bar-chart", "figure"),
     Output("lineout-pie", "figure"),
     Output("scrum-pie", "figure"),
     Output("lineout-rival-pie", "figure"),
     Output("scrum-rival-pie", "figure"),
     Output("resultado-burbuja", "children")],
    [Input("dropdown-variable", "value"), Input("dropdown-periodo", "value")]
)
def actualizar_dashboard(variable, periodo):
    if df.empty:
        return {}, {}, {}, {}, {}, "No se pudieron cargar los datos correctamente"

    # Gráfico de barras
    fig = px.bar(
        df_sin_totales.reset_index(),
        x="Categorias/Variables",
        y=periodo,
        title=f"Relación entre {variable} y {periodo}",
        text_auto=True,
        color="Categorias/Variables",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig.update_layout(
        title={"x": 0.5, "xanchor": "center"},
        xaxis_title="Categorías/Variables",
        yaxis_title="Valores",
        template="plotly_white",
        showlegend=False,
        margin={"l": 50, "r": 50, "t": 50, "b": 50}
    )

    # Gráficos de torta (PB y rival)
    lineout_pie_fig = {
        "data": [
            {"labels": ["Ganados", "Perdidos"], "values": [lineout_ganados, lineout_totales - lineout_ganados], "type": "pie",
             "marker": {"colors": ["#800000", "#FFD700"]}}
        ],
        "layout": {"title": f"Line Out PB: {porcentaje_lineout_ganado}%", "showlegend": True}
    }
    # Gráfico de torta para Lineout del rival
    lineout_rival_pie_fig = {
        "data": [
            {
                "labels": ["Ganados", "Perdidos"],
                "values": [lineout_ganados_rival, lineout_totales_rival - lineout_ganados_rival],
                "type": "pie",
                "marker": {"colors": ["#006400", "#2F4F4F"]}  # Verde oscuro y gris oscuro
            }
        ],
        "layout": {
            "title": f"Lineout Rival: {porcentaje_lineout_rival:.1f}%",
            "showlegend": True
        }
    }
    # Gráfico de torta para Scrum PB
    scrum_pie_fig = {
        "data": [
            {"labels": ["Ganados", "Perdidos"], "values": [scrum_ganados, scrum_totales - scrum_ganados], "type": "pie",
             "marker": {"colors": ["#800000", "#FFD700"]}}
        ],
        "layout": {"title": f"Scrum PB: {porcentaje_scrum_ganado}%", "showlegend": True}
    }



    # Gráfico de torta para Scrum del rival
    scrum_rival_pie_fig = {
        "data": [
            {
                "labels": ["Ganados", "Perdidos"],
                "values": [scrum_ganados_rival, scrum_totales_rival - scrum_ganados_rival],
                "type": "pie",
                "marker": {"colors": ["#006400", "#2F4F4F"]}  # Verde oscuro y gris oscuro
            }
        ],
        "layout": {
            "title": f"Scrum Rival: {porcentaje_scrum_rival:.1f}%",
            "showlegend": True
        }
    }

    # Resultado de la burbuja
    valor_burbuja = df_sin_totales.loc[variable, periodo]
    resultado_burbuja = f"{int(valor_burbuja):,}" if pd.notnull(valor_burbuja) else "No disponible"

    return fig, lineout_pie_fig, scrum_pie_fig, lineout_rival_pie_fig, scrum_rival_pie_fig, resultado_burbuja

@app.callback(
    Output("export-status", "children"),
    [Input("export-button", "n_clicks")]
)
def exportar_a_html(n_clicks):
    if n_clicks > 0:
        try:
            # Obtener los gráficos principales
            fig_bar, fig_lineout, fig_scrum, _ = actualizar_dashboard(
                df_sin_totales.index[0] if not df_sin_totales.empty else None,
                "1er tiempo"
            )

            # Crear subplots con diferentes tipos
            from plotly.subplots import make_subplots
            from plotly.io import write_html

            combined_fig = make_subplots(
                rows=3, cols=1, 
                subplot_titles=["Bar Chart", "Lineout Pie", "Scrum Pie"],
                specs=[[{"type": "xy"}], [{"type": "domain"}], [{"type": "domain"}]]  # Especificar tipos de subplot
            )

            # Agregar los gráficos al subplot
            combined_fig.add_traces(fig_bar.data, rows=1, cols=1)  # Gráfico de barras
            combined_fig.add_trace(fig_lineout["data"][0], row=2, col=1)  # Gráfico de torta Lineout
            combined_fig.add_trace(fig_scrum["data"][0], row=3, col=1)  # Gráfico de torta Scrum

            # Actualizar el diseño
            combined_fig.update_layout(
                height=900, 
                title_text="Dashboard Exportado"
            )

            # Exportar a HTML
            write_html(combined_fig, output_html_path)

            return "Exportado exitosamente a HTML!"
        except Exception as e:
            return f"Error al exportar: {e}"

    return "Haz clic en el botón para exportar."

# Ejecutar el servidor
if __name__ == '__main__':
    app.run_server(debug=False)
