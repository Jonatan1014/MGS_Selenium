from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import math
import os

def dividir_archivo_excel(ruta_archivo, filas_por_grupo, ruta_destino):
    # Cargar el archivo Excel original
    df = pd.read_excel(ruta_archivo, header=None)

    # Calcular el número total de grupos
    total_grupos = math.ceil(len(df) / filas_por_grupo)

    # Iterar sobre los grupos y guardar cada uno en un nuevo archivo Excel
    for i in range(total_grupos):
        inicio = i * filas_por_grupo
        fin = (i + 1) * filas_por_grupo

        grupo_df = df.iloc[inicio:fin]

        # Si es el último grupo, llenar las filas faltantes con "NULL"
        if i == total_grupos - 1:
            filas_faltantes = filas_por_grupo - len(grupo_df)
            for _ in range(filas_faltantes):
                grupo_df = grupo_df.append(['NULL'] * len(df.columns), ignore_index=True)

        # Crear un nuevo archivo Excel para cada grupo
        nuevo_archivo = os.path.join(ruta_destino, f"grupo_{i + 1}.xlsx")
        workbook = Workbook()
        sheet = workbook.active

        for r_idx, row in enumerate(dataframe_to_rows(grupo_df, index=False), 1):
            for c_idx, value in enumerate(row, 1):
                sheet.cell(row=r_idx, column=c_idx, value=value)

        # Eliminar la primera fila si no es el primer grupo
        if i != 0:
            sheet.delete_rows(1)

        # Guardar el grupo en un nuevo archivo Excel
        workbook.save(filename=nuevo_archivo)

        print(f"Grupo {i + 1} guardado en {nuevo_archivo}")

# Ejemplo de uso
ruta_archivo_original = r"C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\pruebas.xlsx"  # Reemplaza con tu ruta y nombre de archivo
filas_por_grupo = 250
ruta_destino = r"C:\Users\farud\OneDrive\Escritorio\MGS_Selenium\Excel"  # Reemplaza con tu ruta de destino

dividir_archivo_excel(ruta_archivo_original, filas_por_grupo, ruta_destino)
