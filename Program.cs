import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import openpyxl

# Leer los datos desde el archivo Excel usando pandas
file_path = "C:/Users/malonso/Documents/NAC SPORT DATA/Databases Nacsport/241102 Tuc Rugby vs Palermo Bajo.xlsx"
wb = openpyxl.load_workbook(file_path)
ws = wb.active

# Extraer las columnas y los datos
# Puedes ajustar las celdas según cómo estén los datos en el archivo Excel.
data = pd.DataFrame(ws.values)

# Crear gráficos con Plotly
# Puntos Totales - Gráfico de barras
fig_puntos_totales = px.bar(data, x=0, y=1, title="Puntos Totales por Equipo", labels={'0': 'Equipo', '1': 'Puntos'})

# Posesiones - Gráfico de líneas
fig_possession = px.line(data, x=0, y=2, title="Posesiones por Fase", labels={'0': 'Fase', '2': 'Duración'})

# Rucks y Mauls - Gráfico circular
fig_rucks_mauls = px.pie(data, names=3, title="Rucks y Mauls", labels={'3': 'Fase', '4': 'Rucks'})

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout del dashboard
app.layout = html.Div(children=[
    html.H1(children="Dashboard de Partido de Rugby - Tuc Rugby vs Palermo Bajo"),
    
    html.Div(children=[
        html.H2(children="Puntuación General"),
        dcc.Graph(figure=fig_puntos_totales),
    ], style={'padding': '10px'}),
    
    html.Div(children=[
        html.H2(children="Posesiones por Fase"),
        dcc.Graph(figure=fig_possession),
    ], style={'padding': '10px'}),
    
    html.Div(children=[
        html.H2(children="Rucks y Mauls"),
        dcc.Graph(figure=fig_rucks_mauls),
    ], style={'padding': '10px'}),
])

# Guardar el archivo HTML
output_path = "C:/Users/malonso/Documents/NAC SPORT DATA/Dashboard/Rugby_Dashboard.html"
app.run_server(debug=True, use_reloader=False)  # Esto abre el servidor local

# Exportar el dashboard a un archivo HTML
with open(output_path, 'w') as f:
    f.write(app.index())
