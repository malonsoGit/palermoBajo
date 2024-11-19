import pandas as pd

# Cargar el archivo Excel
file_path = r'C:\Users\malonso\Documents\NAC SPORT DATA\Dashboard\241102 Tuc Rugby vs Palermo Bajo.xlsx'
df = pd.read_excel(file_path)

# Mostrar las primeras filas para explorar el contenido
print(df.head())
