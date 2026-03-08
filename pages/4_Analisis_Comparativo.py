# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import data_manager as dm
import re

st.set_page_config(page_title="Análisis Comparativo", page_icon="📈", layout="wide")

st.title("📈 Análisis Comparativo y Priorización")
st.markdown("Visualiza y compara el portafolio actual de oportunidades de inversión jerarquizado por Riesgo, Valor Presente Neto (VPN) y Rentabilidad (TIR).")

# Cargar Datos
df = dm.load_data()

if df.empty:
    st.error("No hay datos disponibles en el portafolio para realizar el análisis comparativo.")
    st.stop()

# --- Funciones de limpieza de datos ---
# Dado que algunas columnas como Inversión, VPN o TIR vienen como rangos (ej. "4 a 6" o "20 a 25"), 
# necesitamos extraer un valor numérico representativo (el promedio o el tope) para poder graficar.
def parse_numeric(val, method='avg'):
    if pd.isna(val) or val == 'N/A' or str(val).strip() == '':
        return 0.0
        
    s = str(val).replace(',', '')
    # Buscar todos los números (incluyendo decimales) en la celda
    numeros = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    
    if not numeros: return 0.0
    
    nums_float = [float(n) for n in numeros]
    
    if len(nums_float) == 1:
        return nums_float[0]
    elif len(nums_float) >= 2:
        if method == 'avg':
            return sum(nums_float) / len(nums_float)
        elif method == 'max':
            return max(nums_float)
        elif method == 'min':
            return min(nums_float)
    return 0.0

# Preparamos una copia del dataframe con los valores numéricos limpios para los gráficos
plot_df = df.copy()

# Parsear Inversión (para el tamaño de las burbujas)
plot_df['Inversion_Num'] = plot_df['Monto de inversión estimado (MMUSD)'].apply(lambda x: parse_numeric(x, 'avg'))
# Si algún proyecto no tiene inversión parseable, asignarle un tamaño mínimo visual
plot_df['Inversion_Num'] = plot_df['Inversion_Num'].replace(0, 0.5)

# Parsear VPN (Eje Y)
plot_df['VPN_Num'] = plot_df['VPN (MMUSD)'].apply(lambda x: parse_numeric(x, 'avg'))

# Parsear TIR (Eje Y)
plot_df['TIR_Num'] = plot_df['TIR (%)'].apply(lambda x: parse_numeric(x, 'avg'))

# Normalizar texto de riesgos para categorizar
def normalize_risk(r):
    r_str = str(r).strip().lower()
    if 'alto' in r_str or 'crítico' in r_str or 'high' in r_str: return 'Alto / Crítico'
    if 'medio' in r_str or 'medium' in r_str: return 'Medio'
    if 'bajo' in r_str or 'low' in r_str: return 'Bajo'
    return 'No Definido'

plot_df['Riesgo_Cat'] = plot_df['Nivel de riesgo global'].apply(normalize_risk)

# Paleta de colores para los riesgos
color_discrete_map = {
    'Bajo': '#10b981',           # verde
    'Medio': '#f59e0b',          # naranja/amarillo
    'Alto / Crítico': '#ef4444', # rojo
    'No Definido': '#94a3b8'     # gris
}

# Orden lógico del eje X para los riesgos
category_orders = {"Riesgo_Cat": ["Bajo", "Medio", "Alto / Crítico", "No Definido"]}

# --- Renderización de Gráficos ---

tab1, tab2, tab3 = st.tabs(["📊 VPN vs Riesgo", "📈 TIR vs Riesgo", "🎯 Matriz de Priorización (TIR vs VPN)"])

with tab1:
    st.subheader("Valor Presente Neto (VPN) por Perfil de Riesgo")
    st.markdown("El tamaño de la burbuja representa el Monto Estimado de Inversión (MMUSD).")
    
    fig_vpn = px.scatter(
        plot_df, 
        x="Riesgo_Cat", 
        y="VPN_Num", 
        size="Inversion_Num",
        color="Riesgo_Cat",
        hover_name="Nombre de la oportunidad",
        hover_data={
            "Riesgo_Cat": False, 
            "VPN_Num": ':.2f',
            "Inversion_Num": ':.2f',
            "TIR_Num": ':.1f',
            "Sector / Industria": True
        },
        labels={
            "VPN_Num": "Valor Presente Neto (MMUSD)",
            "Riesgo_Cat": "Nivel de Riesgo Global",
            "Inversion_Num": "Inversión (MMUSD)",
            "TIR_Num": "TIR (%)"
        },
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
        size_max=40,
        template="plotly_white"
    )
    
    fig_vpn.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(211, 211, 211, 0.4)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(211, 211, 211, 0.4)')
    )
    st.plotly_chart(fig_vpn, use_container_width=True)

with tab2:
    st.subheader("Tasa Interna de Retorno (TIR) por Perfil de Riesgo")
    st.markdown("El tamaño de la burbuja representa el Monto Estimado de Inversión (MMUSD).")
    
    fig_tir = px.scatter(
        plot_df, 
        x="Riesgo_Cat", 
        y="TIR_Num", 
        size="Inversion_Num",
        color="Riesgo_Cat",
        hover_name="Nombre de la oportunidad",
        hover_data={
            "Riesgo_Cat": False, 
            "TIR_Num": ':.1f',
            "VPN_Num": ':.2f',
            "Inversion_Num": ':.2f',
            "Sector / Industria": True
        },
        labels={
            "TIR_Num": "TIR Esperada (%)",
            "Riesgo_Cat": "Nivel de Riesgo Global",
            "Inversion_Num": "Inversión (MMUSD)",
            "VPN_Num": "VPN (MMUSD)"
        },
        color_discrete_map=color_discrete_map,
        category_orders=category_orders,
        size_max=40,
        template="plotly_white"
    )
    
    fig_tir.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(211, 211, 211, 0.4)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(211, 211, 211, 0.4)')
    )
    st.plotly_chart(fig_tir, use_container_width=True)

with tab3:
    st.subheader("Matriz de Atractividad: Rentabilidad vs Valor")
    st.markdown("Proyectos en el **cuadrante superior derecho** (Alta TIR, Alto VPN) representan las oportunidades más atractivas. El color indica su nivel de riesgo.")
    
    # Calcular promedios para trazar las líneas divisorias de los cuadrantes
    promedio_tir = plot_df['TIR_Num'].mean()
    promedio_vpn = plot_df['VPN_Num'].mean()
    
    fig_matrix = px.scatter(
        plot_df, 
        x="VPN_Num", 
        y="TIR_Num", 
        size="Inversion_Num",
        color="Riesgo_Cat",
        hover_name="Nombre de la oportunidad",
        hover_data={
            "Riesgo_Cat": True, 
            "Inversion_Num": ':.2f',
            "TIR_Num": ':.1f',
            "VPN_Num": ':.2f'
        },
        labels={
            "VPN_Num": "Valor Presente Neto Promedio (MMUSD)",
            "TIR_Num": "Tasa Interna de Retorno (%)",
            "Riesgo_Cat": "Riesgo Global"
        },
        color_discrete_map=color_discrete_map,
        size_max=35,
        template="plotly_white"
    )
    
    # Agregar líneas divisorias de medias
    fig_matrix.add_hline(y=promedio_tir, line_dash="dash", line_color="gray", opacity=0.5)
    fig_matrix.add_vline(x=promedio_vpn, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Anotaciones de los cuadrantes
    fig_matrix.add_annotation(
        x=plot_df['VPN_Num'].max(), y=plot_df['TIR_Num'].max(),
        text="Alta Prioridad",
        showarrow=False, font=dict(color="green", size=12), opacity=0.7,
        xanchor="right", yanchor="top"
    )
    
    fig_matrix.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

# Footer con listado rápido
st.markdown("---")
st.markdown("### 📋 Resumen Tabular")
display_cols = ["ID_Proyecto", "Nombre de la oportunidad", "Sector / Industria", "Nivel de riesgo global", "TIR (%)", "VPN (MMUSD)", "Monto de inversión estimado (MMUSD)"]
st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
