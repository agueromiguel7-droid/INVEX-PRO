# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import data_manager as dm

st.set_page_config(page_title="Gestor de Proyectos", page_icon="🛠️", layout="wide")

# Validacion de seguridad RBAC
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("Acceso denegado. No tienes permisos para ver esta página.")
    st.stop()

st.title("🛠️ Gestor de Proyectos")
st.markdown("Agrega nuevas oportunidades de inversión al portafolio de Invex Pro.")

# Cargar datos
df = dm.load_data()

# --- Formulario de Nuevo Proyecto ---
with st.form("nuevo_proyecto_form", clear_on_submit=True):
    st.subheader("Datos Básicos")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre de la oportunidad*", max_chars=100)
        sector = st.selectbox("Sector / Industria*", ["Agrícola", "Inmobiliario", "Tecnología", "Salud", "Manufactura", "Otro"])
        ubicacion = st.text_input("Ubicación (Región – Ciudad)*")
        fecha = st.date_input("Fecha de evaluación")
    
    with col2:
        tipo_op = st.selectbox("Tipo de oportunidad*", ["Venta Total", "Venta Parcial", "Asociación Estratégica", "Préstamo", "Búsqueda de Capital"])
        alcance = st.text_input("Alcance del proyecto")
        elaborado_por = st.text_input("Elaborado por")
        estado_madurez = st.selectbox("Estado actual de madurez", ["Idea", "Perfil", "Pre-factibilidad", "Factibilidad", "Operación"])

    st.text_area("Resumen del negocio / proyecto*", key="resumen", max_chars=500, help="Resumen ejecutivo del proyecto")
    st.text_area("Ventaja competitiva principal", key="ventaja")

    st.markdown("---")
    st.subheader("Indicadores Financieros")
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        inversion = st.number_input("Monto Inversión (MMUSD)*", min_value=0.0, step=0.1)
        capex = st.number_input("CAPEX (MMUSD)", min_value=0.0, step=0.1)
        opex = st.number_input("OPEX (MMUSD)", min_value=0.0, step=0.1)
        
    with col_f2:
        tir = st.number_input("TIR (%)", min_value=0.0, max_value=100.0, step=0.5)
        vpn = st.number_input("VPN (MMUSD)", value=0.0, step=0.1)
        t_recup = st.number_input("T. Recuperación (años)", min_value=0.0, step=0.5)
        
    with col_f3:
        vida_util = st.number_input("Vida útil est. (Años)", min_value=0, step=1)
        prob_cierre = st.number_input("Prob. Cierre (%)", min_value=0, max_value=100, step=5)
        tasa_desc = st.number_input("Tasa de descuento (%)", min_value=0.0, step=1.0, value=10.0)
        
    st.markdown("---")
    st.subheader("Riesgos y Mercado")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        nivel_riesgo = st.selectbox("Nivel de riesgo global", ["Bajo", "Medio", "Alto", "Crítico"])
        r_tecnico = st.text_input("Riesgo Técnico")
        m_tecnico = st.text_area("Mitigaciones Riesgo Técnico", height=68)
        r_financiero = st.text_input("Riesgo Financiero")
        m_financiero = st.text_area("Mitigaciones Riesgo Financiero", height=68)
        r_regulatorio = st.text_input("Riesgo Regulatorio")
        m_regula = st.text_area("Mitigación Riesgo Regulatorio", height=68)
        r_mercado = st.text_input("Riesgo Mercado")
        m_mercado = st.text_area("Mitigación Riesgo Mercado", height=68)
        
    with col_r2:
        mercado_obj = st.text_input("Segmento objetivo")
        barreras = st.text_area("Barreras de entrada", height=68)
        conclu_mercado = st.text_area("Conclusión Est. Mercado", height=68)
        st.markdown("**Servicios Conexos Estimados (USD)**")
        s_energia = st.text_input("Energía")
        s_agua = st.text_input("Agua")
        s_gas = st.text_input("Gas")

    st.markdown("---")
    st.subheader("Archivo Multimedia")
    imagen = st.file_uploader("Sube una imagen representativa del proyecto (JPG/PNG)", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Guardar Proyecto Nuevo", use_container_width=True)
    
    if submitted:
        if not nombre or not sector or not ubicacion or not st.session_state.resumen:
             st.error("Por favor completa todos los campos obligatorios (*) marcados.")
        else:
             try:
                 nuevo_id = dm.get_next_project_id(df)
                 if imagen:
                     dm.save_project_image(imagen, nuevo_id)
                     
                 nueva_fila = {
                     "ID_Proyecto": nuevo_id,
                     "Numero de Proyecto": nuevo_id,
                     "Nombre de la oportunidad": nombre,
                     "Sector / Industria": sector,
                     "Ubicación (Región – Ciudad)": ubicacion,
                     "Fecha de evaluación": pd.to_datetime(fecha).strftime("%d/%m/%Y"),
                     "Tipo de oportunidad": tipo_op,
                     "Elaborado por": elaborado_por,
                     "Alcance del proyecto": alcance,
                     "Estado actual de madurez": estado_madurez,
                     "Resumen del negocio / proyecto (máx. 10 líneas)": st.session_state.resumen,
                     "Ventaja competitiva principal": st.session_state.ventaja,
                     "Monto de inversión estimado (MMUSD)": inversion,
                     "CAPEX (MMUSD)": capex,
                     "OPEX (MMUSD)": opex,
                     "TIR (%)": tir,
                     "VPN (MMUSD)": vpn,
                     "Tiempo de recuperación (años)": t_recup,
                     "Vida útil estimada del proyecto": vida_util,
                     "Probabilidad estimada de concreción (%)": prob_cierre,
                     "Tasa de descuento utilizada": tasa_desc,
                     "Nivel de riesgo global": nivel_riesgo,
                     "Riesgo Técnico": r_tecnico,
                     "Mitigaciones Riesgo Técnico": m_tecnico,
                     "Riesgo Financiero": r_financiero,
                     "Mitigaciones Riesgo Financiero": m_financiero,
                     "Riesgo Regulatorio": r_regulatorio,
                     "Mitigación Riesgo Regulatorio": m_regula,
                     "Riesgo Mercado": r_mercado,
                     "Mitigación Riesgo Mercado": m_mercado,
                     "Servicio Energía Estimado (USD)": s_energia,
                     "Servicio Agua Estimado (USD)": s_agua,
                     "Servicio Gas Estimado (USD)": s_gas,
                     "Segmento objetivo": mercado_obj,
                     "Barreras de entrada": barreras,
                     "Conclusión del estudio de mercado": conclu_mercado,
                 }
                 
                 for col in df.columns:
                     if col not in nueva_fila:
                         nueva_fila[col] = "N/A"
                         
                 df_nuevo = pd.DataFrame([nueva_fila])
                 df = pd.concat([df, df_nuevo], ignore_index=True)
                 
                 if dm.save_data(df):
                     st.success(f"Proyecto '{nombre}' creado exitosamente con ID: {nuevo_id}!")
                 else:
                     st.error("Ocurrió un error al persistir los cambios.")
                     
             except Exception as e:
                 st.error(f"Error procesando formulario: {e}")
