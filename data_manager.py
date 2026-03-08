# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import os
from streamlit_gsheets import GSheetsConnection

IMAGES_DIR = "imagenes_proyectos"

def load_data():
    """Carga y procesa los datos desde la hoja de Google Sheets"""
    try:
        # Crea la conexión a Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Lee la pestaña 'Datos_Extraidos' con un caché de 5 minutos
        df = conn.read(worksheet="Datos_Extraidos", ttl="5m")
        
        # Limpiar filas completamente vacías que GSheets suele regresar
        df = df.dropna(how="all")
        
        # Asegurarse de que exista una columna ID de proyecto
        if not df.empty and "ID_Proyecto" not in df.columns:
            df.insert(0, "ID_Proyecto", [f"PRJ-{str(i).zfill(3)}" for i in range(1, len(df) + 1)])
            save_data(df)
            
        return df
    except Exception as e:
        st.error(f"Error al cargar la base de datos de proyectos desde Google Sheets: {e}")
        return pd.DataFrame()

def save_data(df):
    """Guarda el DataFrame de vuelta a Google Sheets"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Actualiza toda la pestaña
        conn.update(worksheet="Datos_Extraidos", data=df)
        # Limpia la cache interna de streamlit para forzar lectura de lo nuevo
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al guardar los datos en Google Sheets: {e}")
        return False



def get_next_project_id(df):

    """Genera el siguiente ID correlativo (ej. PRJ-004)"""

    if df.empty or "ID_Proyecto" not in df.columns:

        return "PRJ-001"

        

    # Extraer los numeros

    try:

        ids = df["ID_Proyecto"].astype(str)

        # Buscar los que empiecen con PRJ-

        numeros = []

        for id_str in ids:

            if str(id_str).startswith('PRJ-'):

                nums = ''.join(filter(str.isdigit, id_str))

                if nums:

                    numeros.append(int(nums))

        

        if numeros:

            next_num = max(numeros) + 1

            return f"PRJ-{str(next_num).zfill(3)}"

    except Exception:

        pass

        

    # Fallback si no hay correlativo entendible

    return f"PRJ-{str(len(df) + 1).zfill(3)}"



def save_project_image(image_file, project_id):

    """Guarda un archivo subido en el directorio de imagenes"""

    if image_file is None:

        return None

        

    # Crear directorio si no existe

    if not os.path.exists(IMAGES_DIR):

        os.makedirs(IMAGES_DIR)

        

    # Extraer extension

    ext = os.path.splitext(image_file.name)[1]

    filename = f"{project_id}{ext}"

    filepath = os.path.join(IMAGES_DIR, filename)

    

    with open(filepath, "wb") as f:

        f.write(image_file.getbuffer())

        

    return filepath



def get_project_image_path(project_id):

    """Busca la imagen asociada a un proyecto, si existe"""

    if not os.path.exists(IMAGES_DIR):

        return None

        

    for file in os.listdir(IMAGES_DIR):

        if file.startswith(str(project_id)):

            return os.path.join(IMAGES_DIR, file)

            

    # Fallback a un placeholder si no hay imagen (O usa la imagen del logo)

    return "mi_logo.png" if os.path.exists("mi_logo.png") else None

