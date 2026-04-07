# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import data_manager as dm
import plotly.graph_objects as go
import os
import base64
import i18n

lang = st.session_state.get("language", "es")

st.set_page_config(page_title=i18n.t("Detalle de Proyecto", lang), page_icon="📑", layout="wide")

# --- Inyeccion de CSS para Mimetizar a Stitch ---
# Basado en la captura: tarjetas blancas con sombra, texto sutil, metricas grandes azules/oscuras, y badges redondeados.
st.markdown("""
<style>
.metric-card {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.metric-title {
    color: #5c6c7b;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}
.metric-value {
    color: #144bb8;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 5px;
}
.metric-subtitle {
    color: #8c9ea8;
    font-size: 0.75rem;
}
.badge-green {
    background-color: #d1fae5;
    color: #065f46;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 700;
    float: right;
}
.risk-meter {
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

if "proyecto_seleccionado" not in st.session_state:
    st.warning(i18n.t("Debe seleccionar un proyecto desde la galería de inversiones.", lang))
    if st.button(i18n.t("Volver a la Galería", lang)):
        st.switch_page("views/1_Galeria_de_Inversiones.py")
    st.stop()

project_id = st.session_state["proyecto_seleccionado"]

# Cargar datos
raw_df = dm.load_data()
df = i18n.translate_df(raw_df, lang)
if df.empty:
    st.error("Error al cargar la base de datos.")
    st.stop()
    
# Encontrar el proyecto seleccionado
proyecto = df[df["ID_Proyecto"] == project_id]
if proyecto.empty:
    proyecto = df[df["Numero de Proyecto"] == project_id]

if proyecto.empty:
    st.error(f"No se encontró el proyecto con ID: {project_id}")
    st.stop()

row = proyecto.iloc[0]

# --- Boton Volver Header ---
if st.button(i18n.t("Volver a la Galería", lang)):
    st.switch_page("views/1_Galeria_de_Inversiones.py")
    
# --- Encabezado Tipo Hero (Stitch) ---
# Intentar usar la imagen de fondo tipo banner si existe
img_path = dm.get_project_image_path(project_id)
if img_path and os.path.exists(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
    <div style="border-radius: 12px; overflow: hidden; position: relative; height: 200px; margin-bottom: 20px;">
        <div style="position: absolute; width: 100%; height: 100%; background-image: url(data:image/png;base64,{encoded_string}); background-size: cover; background-position: center;"></div>
        <div style="position: absolute; width: 100%; height: 100%; background: linear-gradient(to right, rgba(0,0,0,0.8), rgba(0,0,0,0.2));"></div>
        <div style="position: absolute; bottom: 20px; left: 20px; color: white;">
            <span style="background-color: #144bb8; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; margin-bottom: 10px; display: inline-block;">{str(row.get('Sector / Industria', 'PROJECT')).upper()}</span>
            <div style="color: #f8f9fa; margin: 0; font-size: 2.5rem; line-height: 1.1; font-weight: bold; font-family: 'Inter', sans-serif;">{row.get('Nombre de la oportunidad', 'Sin Título')}</div>
            <p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;">📍 {row.get('Ubicación (Región – Ciudad)', 'N/A')} | 🏷️ {row.get('Tipo de oportunidad', 'N/A')}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.header(row.get('Nombre de la oportunidad', 'Sin Título'))
    st.subheader(f"📍 {row.get('Ubicación (Región – Ciudad)', 'N/A')} | 🏷️ {row.get('Sector / Industria', 'N/A')}")
    
# --- Contenido del Proyecto ---
col_main, col_side = st.columns([1.5, 1])

with col_main:
    st.markdown(f"### 📁 {i18n.t('Información Detallada del Proyecto', lang)}")
    
    # A. IDENTIFICACIÓN GENERAL
    with st.expander(i18n.t("A. IDENTIFICACIÓN GENERAL", lang)):
        st.write(f"**{i18n.t('Nombre de la oportunidad', lang)}:** {row.get('Nombre de la oportunidad', 'N/A')}")
        st.write(f"**{i18n.t('Sector / Industria', lang)}:** {row.get('Sector / Industria', 'N/A')}")
        st.write(f"**{i18n.t('Ubicación (Región – Ciudad)', lang)}:** {row.get('Ubicación (Región – Ciudad)', 'N/A')}")
        st.write(f"**{i18n.t('Fecha de evaluación', lang)}:** {row.get('Fecha de evaluación', 'N/A')}")
        st.write(f"**{i18n.t('Elaborado por', lang)}:** {row.get('Elaborado por', 'N/A')}")

    # B. DESCRIPCIÓN EJECUTIVA DE LA OPORTUNIDAD
    with st.expander(i18n.t("B. DESCRIPCIÓN EJECUTIVA DE LA OPORTUNIDAD", lang), expanded=True):
        st.info(f"**{i18n.t('Resumen', lang)}:** {row.get('Resumen del negocio / proyecto (máx. 10 líneas)', 'N/A')}")
        st.write(f"**{i18n.t('Tipo de oportunidad', lang)}:** {row.get('Tipo de oportunidad', 'N/A')}")
        st.write(f"**{i18n.t('Describir Otros', lang)}:** {row.get('Describir Otros', 'N/A')}")
        st.write(f"**{i18n.t('Alcance del proyecto', lang)}:** {row.get('Alcance del proyecto', 'N/A')}")
        st.write(f"**{i18n.t('Ventaja competitiva principal', lang)}:** {row.get('Ventaja competitiva principal', 'N/A')}")
        st.write(f"**{i18n.t('Estado actual de madurez', lang)}:** {row.get('Estado actual de madurez', 'N/A')}")

    # C. CARACTERÍSTICAS DE LA INVERSIÓN
    with st.expander(i18n.t("C. CARACTERÍSTICAS DE LA INVERSIÓN", lang)):
        st.write(f"**{i18n.t('Monto de inversión estimado (MMUSD)', lang)}:** {row.get('Monto de inversión estimado (MMUSD)', 'N/A')}")
        st.write(f"**{i18n.t('Tipo de inversión', lang)}:** {row.get('Tipo de inversión', 'N/A')}")
        st.write(f"**{i18n.t('Clase de estimación', lang)}:** {row.get('Clase de estimación (Si es proyecto nuevo)', 'N/A')}")
        st.write(f"**{i18n.t('% Participación inversionista', lang)}:** {row.get('% Participación inversionista', 'N/A')}")
        st.write(f"**{i18n.t('% Participación socios actuales', lang)}:** {row.get('% Participación socios actuales', 'N/A')}")
        st.write(f"**{i18n.t('Tipo de acuerdo(si aplica)', lang)}:** {row.get('Tipo de acuerdo', 'N/A')}")
        st.write(f"**{i18n.t('¿Compra total o parcial?', lang)}:** {row.get('¿Compra total o parcial?', 'N/A')}")
        st.write(f"**{i18n.t('% de adquisición', lang)}:** {row.get('% de adquisición', 'N/A')}")

    # D. INDICADORES FINANCIEROS
    with st.expander(i18n.t("D. INDICADORES FINANCIEROS (Rangos Esperados)", lang)):
        st.write(f"**{i18n.t('TIR (%)', lang)}:** {row.get('TIR (%)', 'N/A')}")
        st.write(f"**{i18n.t('VPN (MMUSD)', lang)}:** {row.get('VPN (MMUSD)', 'N/A')}")
        st.write(f"**{i18n.t('Tiempo de recuperación (años)', lang)}:** {row.get('Tiempo de recuperación (años)', 'N/A')}")
        st.write(f"**{i18n.t('Vida útil estimada del proyecto', lang)}:** {row.get('Vida útil estimada del proyecto', 'N/A')}")
        st.write(f"**{i18n.t('Sensibilidad (escenarios)', lang)}:** {row.get('Sensibilidad (escenarios)', 'N/A')}")
        st.write(f"**{i18n.t('Precio base (MMUSD)', lang)}:** {row.get('Precio base (MMUSD)', 'N/A')}")
        st.write(f"**{i18n.t('Volumen proyectado', lang)}:** {row.get('Volumen proyectado', 'N/A')}")
        st.write(f"**{i18n.t('CAPEX (MMUSD)', lang)}:** {row.get('CAPEX (MMUSD)', 'N/A')}")
        st.write(f"**{i18n.t('OPEX (MMUSD)', lang)}:** {row.get('OPEX (MMUSD)', 'N/A')}")
        st.write(f"**{i18n.t('Tasa de descuento utilizada', lang)}:** {row.get('Tasa de descuento utilizada', 'N/A')}")

    # E. ESTUDIO DE MERCADO
    with st.expander(i18n.t("E. ESTUDIO DE MERCADO", lang)):
        st.write(f"**{i18n.t('Demanda identificada', lang)}:** {row.get('Demanda identificada', 'N/A')}")
        st.write(f"**{i18n.t('Segmento objetivo', lang)}:** {row.get('Segmento objetivo', 'N/A')}")
        st.write(f"**{i18n.t('Competencia relevante', lang)}:** {row.get('Competencia relevante', 'N/A')}")
        st.write(f"**{i18n.t('Barreras de entrada', lang)}:** {row.get('Barreras de entrada', 'N/A')}")
        st.write(f"**{i18n.t('Ventana de oportunidad (timing)', lang)}:** {row.get('Ventana de oportunidad (timing)', 'N/A')}")
        st.write(f"**{i18n.t('Conclusión del estudio de mercado', lang)}:** {row.get('Conclusión del estudio de mercado', 'N/A')}")

    # F. PROBABILIDAD Y FIRMEZA DE LA OPORTUNIDAD
    with st.expander(i18n.t("F. PROBABILIDAD Y FIRMEZA DE LA OPORTUNIDAD", lang)):
        st.write(f"**{i18n.t('Probabilidad estimada de concreción (%)', lang)}:** {row.get('Probabilidad estimada de concreción (%)', 'N/A')}")
        st.write(f"**{i18n.t('Nivel de firmeza', lang)}:** {row.get('Nivel de firmeza', 'N/A')}")
        st.write(f"**{i18n.t('Factores críticos para cierre', lang)}:** {row.get('Factores críticos para cierre', 'N/A')}")
        st.write(f"**{i18n.t('Dependencias externas', lang)}:** {row.get('Dependencias externas', 'N/A')}")

    # G. ANÁLISIS DE RIESGO
    with st.expander(i18n.t("G. ANÁLISIS DE RIESGO", lang)):
        st.write(f"**{i18n.t('Nivel de riesgo global', lang)}:** {row.get('Nivel de riesgo global', 'N/A')}")
        st.write(f"**{i18n.t('Riesgo Técnico', lang)}:** {row.get('Riesgo Técnico', 'N/A')}")
        st.write(f"**{i18n.t('Mitigaciones Riesgo Técnico', lang)}:** {row.get('Mitigaciones Riesgo Técnico', 'N/A')}")
        st.write(f"**{i18n.t('Riesgo Financiero', lang)}:** {row.get('Riesgo Financiero', 'N/A')}")
        st.write(f"**{i18n.t('Mitigaciones Riesgo Financiero', lang)}:** {row.get('Mitigaciones Riesgo Financiero', 'N/A')}")
        st.write(f"**{i18n.t('Riesgo Regulatorio', lang)}:** {row.get('Riesgo Regulatorio', 'N/A')}")
        st.write(f"**{i18n.t('Mitigación Riesgo Regulatorio', lang)}:** {row.get('Mitigación Riesgo Regulatorio', 'N/A')}")
        st.write(f"**{i18n.t('Riesgo Mercado', lang)}:** {row.get('Riesgo Mercado', 'N/A')}")
        st.write(f"**{i18n.t('Mitigación Riesgo Mercado', lang)}:** {row.get('Mitigación Riesgo Mercado', 'N/A')}")

    # H. ENTORNO Y SERVICIOS CONEXOS
    with st.expander(i18n.t("H. ENTORNO Y SERVICIOS CONEXOS", lang)):
        st.write(f"**{i18n.t('Servicio Energía Estimado (USD)', lang)}:** {row.get('Servicio Energía Estimado (USD)', 'N/A')}")
        st.write(f"**{i18n.t('Servicio Agua Estimado (USD)', lang)}:** {row.get('Servicio Agua Estimado (USD)', 'N/A')}")
        st.write(f"**{i18n.t('Servicio Gas Estimado (USD)', lang)}:** {row.get('Servicio Gas Estimado (USD)', 'N/A')}")
        st.write(f"**{i18n.t('Costo de vida en la zona', lang)}:** {row.get('Costo de vida en la zona', 'N/A')}")
        st.write(f"**{i18n.t('Acceso a educación', lang)}:** {row.get('Acceso a educación', 'N/A')}")
        st.write(f"**{i18n.t('Infraestructura logística', lang)}:** {row.get('Infraestructura logística', 'N/A')}")
        st.write(f"**{i18n.t('Disponibilidad de talento humano', lang)}:** {row.get('Disponibilidad de talento humano', 'N/A')}")
        
    # I. CONCLUSIÓN Y RECOMENDACIÓN
    with st.expander(i18n.t("I. CONCLUSIÓN Y RECOMENDACIÓN", lang)):
        st.write(f"**{i18n.t('Evaluación integral', lang)}:** {row.get('Evaluación integral', 'N/A')}")
        st.write(f"**{i18n.t('Recomendación', lang)}:** {row.get('Recomendación', 'N/A')}")
        st.write(f"**{i18n.t('Próximos pasos', lang)}:** {row.get('Próximos pasos', 'N/A')}")
        st.write(f"**{i18n.t('Fecha estimada de decisión final', lang)}:** {row.get('Fecha estimada de decisión final', 'N/A')}")

    # J. DATOS DEL CONTACTO PRINCIPAL
    with st.expander(i18n.t("J. DATOS DEL CONTACTO PRINCIPAL", lang)):
        st.write(f"**{i18n.t('Nombre', lang)}:** {row.get('Nombre', 'N/A')}")
        st.write(f"**{i18n.t('Cargo', lang)}:** {row.get('Cargo', 'N/A')}")
        st.write(f"**{i18n.t('Empresa', lang)}:** {row.get('Empresa', 'N/A')}")
        st.write(f"**{i18n.t('Teléfono', lang)}:** {row.get('Teléfono', 'N/A')}")
        st.write(f"**{i18n.t('Correo', lang)}:** {row.get('Correo', 'N/A')}")

with col_side:
    st.markdown(f"<h3 style='margin-top: 0;'>💵 {i18n.t('Financial Overview', lang)}</h3>", unsafe_allow_html=True)
    
    # -- Tarjeta TIR --
    tir_val = row.get('TIR (%)', 'N/A')
    tir_display = f"{tir_val * 100:.1f}%" if isinstance(tir_val, float) and tir_val < 1 else f"{tir_val}%" if pd.notna(tir_val) else "N/A"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TIR <span class="badge-green">HIGH RETURN</span></div>
        <div style="text-align: center;">
            <div class="metric-value" style="font-size: 2.2rem;">{tir_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    plot_col1, plot_col2 = st.columns(2)
    # -- Tarjeta VPN --
    vpn_val = row.get('VPN (MMUSD)', 0)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">VPN (NPV)</div>
        <div class="metric-value">${vpn_val}M</div>
        <div class="metric-subtitle">USD NET VALUE</div>
    </div>
    """, unsafe_allow_html=True)
    
    # -- Tarjeta Tiempo de Recuperacion --
    t_rec = row.get('Tiempo de recuperación (años)', 'N/A')
    t_str = f"{t_rec} Years" if pd.notna(t_rec) else "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">PAYBACK PERIOD</div>
        <!-- Simulacion de Timeline simple -->
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #8c9ea8; margin-bottom: 5px;">
            <span>YR 0</span>
            <span>YR 5</span>
            <span>YR 10</span>
        </div>
        <div style="width: 100%; height: 8px; background-color: #e2e8f0; border-radius: 4px; margin-bottom: 15px; position: relative;">
            <div style="position: absolute; left: 30%; width: 20%; height: 100%; background-color: #144bb8; border-radius: 4px;"></div>
        </div>
        <div style="text-align: center;">
            <span style="background-color: #e6f0fa; color: #144bb8; border: 1px solid #c9def5; padding: 4px 15px; border-radius: 12px; font-weight: 600; font-size: 0.85rem;">{t_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # -- Tarjeta Nivel de Riesgo --
    riesgo = str(row.get('Nivel de riesgo global', 'Medium')).capitalize()
    color_riesgo = "#144bb8" # blue por defecto
    if "Alto" in riesgo or "High" in riesgo or "Crítico" in riesgo: color_riesgo = "#ef4444"
    elif "Medio" in riesgo or "Medium" in riesgo: color_riesgo = "#f59e0b"
    elif "Bajo" in riesgo or "Low" in riesgo: color_riesgo = "#10b981"
    
    def format_val(val):
        if pd.isna(val): return "N/A"
        return str(val)

    r_tecnico = format_val(row.get('Riesgo Técnico', 'N/A'))
    r_financiero = format_val(row.get('Riesgo Financiero', 'N/A'))
    r_regulatorio = format_val(row.get('Riesgo Regulatorio', 'N/A'))
    r_mercado = format_val(row.get('Riesgo Mercado', 'N/A'))
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📊 RISK ANALYSIS</div>
        <div class="risk-meter" style="text-align: center; margin-bottom: 15px;">
            <h2 style="color: {color_riesgo}; margin: 10px 0 5px 0;">{riesgo}</h2>
            <div class="metric-subtitle">Risk Profile Index</div>
        </div>
        <div style="font-size: 0.85rem; color: #334155; text-align: left; background-color: #f8fafc; padding: 10px; border-radius: 8px;">
            <p style="margin-bottom: 8px; color: #144bb8; font-weight: 600;">Principales riesgos identificados:</p>
            <ul style="padding-left: 15px; margin-top: 0; margin-bottom: 0;">
                <li style="margin-bottom: 4px;"><strong>Técnico:</strong> {r_tecnico}</li>
                <li style="margin-bottom: 4px;"><strong>Financiero:</strong> {r_financiero}</li>
                <li style="margin-bottom: 4px;"><strong>Regulatorio:</strong> {r_regulatorio}</li>
                <li><strong>Mercado:</strong> {r_mercado}</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")
# Contact Footer Mockup
st.markdown(f"""
<div style="background-color: #144bb8; color: white; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; cursor: pointer;">
    👤 Contactar a {row.get('Elaborado por', 'Gustavo Vegas')}
</div>
""", unsafe_allow_html=True)
