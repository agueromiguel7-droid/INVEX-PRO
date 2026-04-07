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
    st.markdown("### 📁 Información Detallada del Proyecto")
    
    # A. IDENTIFICACIÓN GENERAL
    with st.expander("A. IDENTIFICACIÓN GENERAL"):
        st.write(f"**Nombre de la oportunidad:** {row.get('Nombre de la oportunidad', 'N/A')}")
        st.write(f"**Sector / Industria:** {row.get('Sector / Industria', 'N/A')}")
        st.write(f"**Ubicación (Región – Ciudad):** {row.get('Ubicación (Región – Ciudad)', 'N/A')}")
        st.write(f"**Fecha de evaluación:** {row.get('Fecha de evaluación', 'N/A')}")
        st.write(f"**Elaborado por:** {row.get('Elaborado por', 'N/A')}")

    # B. DESCRIPCIÓN EJECUTIVA DE LA OPORTUNIDAD
    with st.expander("B. DESCRIPCIÓN EJECUTIVA DE LA OPORTUNIDAD", expanded=True):
        st.info(f"**Resumen:** {row.get('Resumen del negocio / proyecto (máx. 10 líneas)', 'N/A')}")
        st.write(f"**Tipo de oportunidad:** {row.get('Tipo de oportunidad', 'N/A')}")
        st.write(f"**Describir Otros:** {row.get('Describir Otros', 'N/A')}")
        st.write(f"**Alcance del proyecto:** {row.get('Alcance del proyecto', 'N/A')}")
        st.write(f"**Ventaja competitiva principal:** {row.get('Ventaja competitiva principal', 'N/A')}")
        st.write(f"**Estado actual de madurez:** {row.get('Estado actual de madurez', 'N/A')}")

    # C. CARACTERÍSTICAS DE LA INVERSIÓN
    with st.expander("C. CARACTERÍSTICAS DE LA INVERSIÓN"):
        st.write(f"**Monto de inversión estimado (MMUSD):** {row.get('Monto de inversión estimado (MMUSD)', 'N/A')}")
        st.write(f"**Tipo de inversión:** {row.get('Tipo de inversión', 'N/A')}")
        st.write(f"**Clase de estimación:** {row.get('Clase de estimación (Si es proyecto nuevo)', 'N/A')}")
        st.write(f"**% Participación inversionista:** {row.get('% Participación inversionista', 'N/A')}")
        st.write(f"**% Participación socios actuales:** {row.get('% Participación socios actuales', 'N/A')}")
        st.write(f"**Tipo de acuerdo(si aplica):** {row.get('Tipo de acuerdo', 'N/A')}")
        st.write(f"**¿Compra total o parcial?:** {row.get('¿Compra total o parcial?', 'N/A')}")
        st.write(f"**% de adquisición:** {row.get('% de adquisición', 'N/A')}")

    # D. INDICADORES FINANCIEROS
    with st.expander("D. INDICADORES FINANCIEROS (Rangos Esperados)"):
        st.write(f"**TIR (%):** {row.get('TIR (%)', 'N/A')}")
        st.write(f"**VPN (MMUSD):** {row.get('VPN (MMUSD)', 'N/A')}")
        st.write(f"**Tiempo de recuperación (años):** {row.get('Tiempo de recuperación (años)', 'N/A')}")
        st.write(f"**Vida útil estimada del proyecto:** {row.get('Vida útil estimada del proyecto', 'N/A')}")
        st.write(f"**Sensibilidad (escenarios):** {row.get('Sensibilidad (escenarios)', 'N/A')}")
        st.write(f"**Precio base (MMUSD):** {row.get('Precio base (MMUSD)', 'N/A')}")
        st.write(f"**Volumen proyectado:** {row.get('Volumen proyectado', 'N/A')}")
        st.write(f"**CAPEX (MMUSD):** {row.get('CAPEX (MMUSD)', 'N/A')}")
        st.write(f"**OPEX (MMUSD):** {row.get('OPEX (MMUSD)', 'N/A')}")
        st.write(f"**Tasa de descuento utilizada:** {row.get('Tasa de descuento utilizada', 'N/A')}")

    # E. ESTUDIO DE MERCADO
    with st.expander("E. ESTUDIO DE MERCADO"):
        st.write(f"**Demanda identificada:** {row.get('Demanda identificada', 'N/A')}")
        st.write(f"**Segmento objetivo:** {row.get('Segmento objetivo', 'N/A')}")
        st.write(f"**Competencia relevante:** {row.get('Competencia relevante', 'N/A')}")
        st.write(f"**Barreras de entrada:** {row.get('Barreras de entrada', 'N/A')}")
        st.write(f"**Ventana de oportunidad (timing):** {row.get('Ventana de oportunidad (timing)', 'N/A')}")
        st.write(f"**Conclusión del estudio de mercado:** {row.get('Conclusión del estudio de mercado', 'N/A')}")

    # F. PROBABILIDAD Y FIRMEZA DE LA OPORTUNIDAD
    with st.expander("F. PROBABILIDAD Y FIRMEZA DE LA OPORTUNIDAD"):
        st.write(f"**Probabilidad estimada de concreción (%):** {row.get('Probabilidad estimada de concreción (%)', 'N/A')}")
        st.write(f"**Nivel de firmeza:** {row.get('Nivel de firmeza', 'N/A')}")
        st.write(f"**Factores críticos para cierre:** {row.get('Factores críticos para cierre', 'N/A')}")
        st.write(f"**Dependencias externas:** {row.get('Dependencias externas', 'N/A')}")

    # G. ANÁLISIS DE RIESGO
    with st.expander("G. ANÁLISIS DE RIESGO"):
        st.write(f"**Nivel de riesgo global:** {row.get('Nivel de riesgo global', 'N/A')}")
        st.write(f"**Riesgo Técnico:** {row.get('Riesgo Técnico', 'N/A')}")
        st.write(f"**Mitigaciones Riesgo Técnico:** {row.get('Mitigaciones Riesgo Técnico', 'N/A')}")
        st.write(f"**Riesgo Financiero:** {row.get('Riesgo Financiero', 'N/A')}")
        st.write(f"**Mitigaciones Riesgo Financiero:** {row.get('Mitigaciones Riesgo Financiero', 'N/A')}")
        st.write(f"**Riesgo Regulatorio:** {row.get('Riesgo Regulatorio', 'N/A')}")
        st.write(f"**Mitigación Riesgo Regulatorio:** {row.get('Mitigación Riesgo Regulatorio', 'N/A')}")
        st.write(f"**Riesgo Mercado:** {row.get('Riesgo Mercado', 'N/A')}")
        st.write(f"**Mitigación Riesgo Mercado:** {row.get('Mitigación Riesgo Mercado', 'N/A')}")

    # H. ENTORNO Y SERVICIOS CONEXOS
    with st.expander("H. ENTORNO Y SERVICIOS CONEXOS"):
        st.write(f"**Servicio Energía Estimado (USD):** {row.get('Servicio Energía Estimado (USD)', 'N/A')}")
        st.write(f"**Servicio Agua Estimado (USD):** {row.get('Servicio Agua Estimado (USD)', 'N/A')}")
        st.write(f"**Servicio Gas Estimado (USD):** {row.get('Servicio Gas Estimado (USD)', 'N/A')}")
        st.write(f"**Costo de vida en la zona:** {row.get('Costo de vida en la zona', 'N/A')}")
        st.write(f"**Acceso a educación:** {row.get('Acceso a educación', 'N/A')}")
        st.write(f"**Infraestructura logística:** {row.get('Infraestructura logística', 'N/A')}")
        st.write(f"**Disponibilidad de talento humano:** {row.get('Disponibilidad de talento humano', 'N/A')}")
        
    # I. CONCLUSIÓN Y RECOMENDACIÓN
    with st.expander("I. CONCLUSIÓN Y RECOMENDACIÓN"):
        st.write(f"**Evaluación integral:** {row.get('Evaluación integral', 'N/A')}")
        st.write(f"**Recomendación:** {row.get('Recomendación', 'N/A')}")
        st.write(f"**Próximos pasos:** {row.get('Próximos pasos', 'N/A')}")
        st.write(f"**Fecha estimada de decisión final:** {row.get('Fecha estimada de decisión final', 'N/A')}")

    # J. DATOS DEL CONTACTO PRINCIPAL
    with st.expander("J. DATOS DEL CONTACTO PRINCIPAL"):
        st.write(f"**Nombre:** {row.get('Nombre', 'N/A')}")
        st.write(f"**Cargo:** {row.get('Cargo', 'N/A')}")
        st.write(f"**Empresa:** {row.get('Empresa', 'N/A')}")
        st.write(f"**Teléfono:** {row.get('Teléfono', 'N/A')}")
        st.write(f"**Correo:** {row.get('Correo', 'N/A')}")

with col_side:
    st.markdown("<h3 style='margin-top: 0;'>💵 Financial Overview</h3>", unsafe_allow_html=True)
    
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
