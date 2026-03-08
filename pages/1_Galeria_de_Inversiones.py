# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import data_manager as dm

st.set_page_config(page_title="Galería de Inversiones", page_icon="📊", layout="wide")

st.title("📊 Portafolio de Inversiones")
st.markdown("Explora las oportunidades de inversión disponibles.")

# Cargar datos
df = dm.load_data()

if df.empty:
    st.info("No hay proyectos cargados actualmente en la base de datos.")
    st.stop()

# --- Zona de Filtros ---
st.markdown("### Filtros")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    sectores = ["Todos"] + sorted(df["Sector / Industria"].dropna().unique().tolist())
    sector_sel = st.selectbox("Sector / Industria", sectores)

with col_f2:
    tipos = ["Todos"] + sorted(df["Tipo de oportunidad"].dropna().unique().tolist())
    tipo_sel = st.selectbox("Tipo de oportunidad", tipos)

with col_f3:
    # Extraer el primer numero de la cadena (para soportar rangos de texto como "4 a 6" o "25 - 45")
    df_monto_str = df["Monto de inversión estimado (MMUSD)"].astype(str).str.replace(',', '.')
    df["Monto_num"] = df_monto_str.str.extract(r'(\d+\.?\d*)', expand=False)
    df["Monto_num"] = pd.to_numeric(df["Monto_num"], errors='coerce').fillna(0)
    
    # Filtro por monto (Min - Max) usando la columna numerica extraida
    min_inv = float(df["Monto_num"].min()) if not df["Monto_num"].empty else 0.0
    max_inv = float(df["Monto_num"].max()) if not df["Monto_num"].empty else 100.0
    
    if min_inv == max_inv:
        min_inv = 0.0
        
    monto_sel = st.slider("Rango de Inversión (MMUSD)", 
                          min_value=min_inv, 
                          max_value=max_inv, 
                          value=(min_inv, max_inv))

# --- Aplicar Filtros ---
df_filtrado = df.copy()

if sector_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Sector / Industria"] == sector_sel]
    
if tipo_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo de oportunidad"] == tipo_sel]
    
df_filtrado = df_filtrado[
    (df_filtrado["Monto_num"] >= monto_sel[0]) & 
    (df_filtrado["Monto_num"] <= monto_sel[1])
]

# --- Mostrar Galeria ---
st.markdown("### Resultados")
st.write(f"Mostrando {len(df_filtrado)} proyecto(s)")

# Crear un grid de cuadriculas (ej. 3 por fila)
cards_per_row = 3
if not df_filtrado.empty:
    for i in range(0, len(df_filtrado), cards_per_row):
        cols = st.columns(cards_per_row)
        for j, col in enumerate(cols):
            if i + j < len(df_filtrado):
                row = df_filtrado.iloc[i + j]
                project_id = row.get("ID_Proyecto", row.get("Numero de Proyecto", ""))
                
                with col:
                    st.markdown("""
                        <div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 20px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    """, unsafe_allow_html=True)
                    
                    # Imagen
                    img_path = dm.get_project_image_path(project_id)
                    if img_path:
                        st.image(img_path, use_container_width=True)
                    else:
                        st.markdown("<div style='height: 150px; background-color: #f0f2f6; display: flex; align-items: center; justify-content: center; color: #a0aab2;'>Sin Imagen</div>", unsafe_allow_html=True)
                    
                    # Datos
                    st.markdown(f"#### {row.get('Nombre de la oportunidad', 'Sin Título')}")
                    st.caption(f"📍 {row.get('Ubicación (Región – Ciudad)', 'N/A')}")
                    st.markdown(f"**Sector:** {row.get('Sector / Industria', 'N/A')}")
                    st.markdown(f"**Inversión Est.:** ${row.get('Monto de inversión estimado (MMUSD)', 0)} MMUSD")
                    
                    tir = row.get('TIR (%)', 'N/A')
                    if pd.notna(tir):
                        st.markdown(f"**TIR:** {tir}%")
                    
                    # Boton para ver detalle
                    if st.button("Ver Detalle Ficha", key=f"btn_det_{project_id}", use_container_width=True):
                        st.session_state["proyecto_seleccionado"] = project_id
                        st.switch_page("pages/3_Detalle_Proyecto.py")
                        
                    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Ningún proyecto coindice con los filtros.")
