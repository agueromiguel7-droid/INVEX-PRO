# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import data_manager as dm
import i18n

lang = st.session_state.get("language", "es")

st.set_page_config(page_title=i18n.t("Gestor de Proyectos", lang), page_icon="🛠️", layout="wide")

# Validacion de seguridad RBAC
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error(i18n.t("Acceso denegado. No tienes permisos para ver esta página.", lang))
    st.stop()

st.title(i18n.t("🛠️ Gestor de Proyectos", lang))
st.markdown(i18n.t("Panel de administración para agregar o actualizar oportunidades de inversión.", lang))

# Cargar datos
df = dm.load_data()

# --- Formulario de Nuevo Proyecto ---
with st.form("nuevo_proyecto_form", clear_on_submit=True):
    st.subheader(i18n.t("Crear Nuevo Proyecto", lang))
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input(f"{i18n.t('Nombre de la oportunidad', lang)}*", max_chars=100)
        sector = st.selectbox(f"{i18n.t('Sector / Industria', lang)}*", ["Agrícola", "Inmobiliario", "Tecnología", "Salud", "Manufactura", "Otro"])
        ubicacion = st.text_input(f"{i18n.t('Ubicación (Región – Ciudad)', lang)}*")
        fecha = st.date_input(i18n.t("Fecha de evaluación", lang))
    
    with col2:
        tipo_op = st.selectbox(f"{i18n.t('Tipo de oportunidad', lang)}*", ["Venta Total", "Venta Parcial", "Asociación Estratégica", "Préstamo", "Búsqueda de Capital"])
        alcance = st.text_input(i18n.t("Alcance del proyecto", lang))
        elaborado_por = st.text_input(i18n.t("Elaborado por", lang))
        estado_madurez = st.selectbox(i18n.t("Estado actual de madurez", lang), ["Idea", "Perfil", "Pre-factibilidad", "Factibilidad", "Operación"])

    st.text_area(f"{i18n.t('Resumen del negocio / proyecto (máx. 10 líneas)', lang)}*", key="resumen", max_chars=500, help=i18n.t("Resumen ejecutivo del proyecto", lang))
    st.text_area(i18n.t("Ventaja competitiva principal", lang), key="ventaja")

    st.markdown("---")
    st.subheader(i18n.t("Indicadores Financieros", lang))
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        inversion = st.number_input(f"{i18n.t('Monto de inversión estimado (MMUSD)', lang)}*", min_value=0.0, step=0.1)
        capex = st.number_input(i18n.t("CAPEX (MMUSD)", lang), min_value=0.0, step=0.1)
        opex = st.number_input(i18n.t("OPEX (MMUSD)", lang), min_value=0.0, step=0.1)
        
    with col_f2:
        tir = st.number_input(i18n.t("TIR (%)", lang), min_value=0.0, max_value=100.0, step=0.5)
        vpn = st.number_input(i18n.t("VPN (MMUSD)", lang), value=0.0, step=0.1)
        t_recup = st.number_input(i18n.t("Tiempo de recuperación (años)", lang), min_value=0.0, step=0.5)
        
    with col_f3:
        vida_util = st.number_input(i18n.t("Vida útil estimada del proyecto", lang), min_value=0, step=1)
        prob_cierre = st.number_input(i18n.t("Probabilidad estimada de concreción (%)", lang), min_value=0, max_value=100, step=5)
        tasa_desc = st.number_input(i18n.t("Tasa de descuento utilizada", lang), min_value=0.0, step=1.0, value=10.0)
        
    st.markdown("---")
    st.subheader(i18n.t("Riesgos y Mercado", lang))
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        nivel_riesgo = st.selectbox(i18n.t("Nivel de riesgo global", lang), ["Bajo", "Medio", "Alto", "Crítico"])
        r_tecnico = st.text_input(i18n.t("Riesgo Técnico", lang))
        m_tecnico = st.text_area(i18n.t("Mitigaciones Riesgo Técnico", lang), height=68)
        r_financiero = st.text_input(i18n.t("Riesgo Financiero", lang))
        m_financiero = st.text_area(i18n.t("Mitigaciones Riesgo Financiero", lang), height=68)
        r_regulatorio = st.text_input(i18n.t("Riesgo Regulatorio", lang))
        m_regula = st.text_area(i18n.t("Mitigación Riesgo Regulatorio", lang), height=68)
        r_mercado = st.text_input(i18n.t("Riesgo Mercado", lang))
        m_mercado = st.text_area(i18n.t("Mitigación Riesgo Mercado", lang), height=68)
        
    with col_r2:
        mercado_obj = st.text_input(i18n.t("Segmento objetivo", lang))
        barreras = st.text_area(i18n.t("Barreras de entrada", lang), height=68)
        conclu_mercado = st.text_area(i18n.t("Conclusión del estudio de mercado", lang), height=68)
        st.markdown(f"**{i18n.t('H. ENTORNO Y SERVICIOS CONEXOS', lang)}**")
        s_energia = st.text_input(i18n.t("Servicio Energía Estimado (USD)", lang))
        s_agua = st.text_input(i18n.t("Servicio Agua Estimado (USD)", lang))
        s_gas = st.text_input(i18n.t("Servicio Gas Estimado (USD)", lang))

    st.markdown("---")
    st.subheader(i18n.t("Imagen del Proyecto", lang))
    imagen = st.file_uploader(i18n.t("Subir archivo", lang), type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button(i18n.t("Guardar Proyecto", lang), use_container_width=True)
    
    if submitted:
        if not nombre or not sector or not ubicacion or not st.session_state.resumen:
             st.error(i18n.t("Por favor completa todos los campos obligatorios (*) marcados.", lang))
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
                    st.success(f"{i18n.t('Guardado Exitoso!', lang)} {nombre} ID: {nuevo_id}")
                 else:
                    st.error(i18n.t("Ocurrió un error al persistir los cambios.", lang))
                     
             except Exception as e:
                 st.error(f"Error procesando formulario: {e}")
