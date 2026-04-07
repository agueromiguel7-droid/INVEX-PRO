# -*- coding: utf-8 -*-
import pandas as pd

# Translation mapping (Spanish key -> English translation)
TRANSLATIONS = {
    # Main Sidebar & Navigation
    "Bienvenido": "Welcome",
    "Invex Pro": "Invex Pro",
    "Cerrar Sesión": "Sign Out",
    "Galería de Inversiones": "Investment Gallery",
    "Análisis Comparativo": "Comparative Analysis",
    "Detalle de Proyecto": "Project Details",
    "Gestor de Proyectos": "Project Manager",
    "Idioma / Language": "Language",

    # View: 1_Galeria_de_Inversiones
    "📊 Portafolio de Inversiones": "📊 Investment Portfolio",
    "Explora las oportunidades de inversión disponibles.": "Explore available investment opportunities.",
    "No hay proyectos cargados actualmente en la base de datos.": "No projects currently loaded in the database.",
    "### Filtros": "### Filters",
    "Sector / Industria": "Sector / Industry",
    "Tipo de oportunidad": "Asset Type", # As requested by user
    "Rango de Inversión (MMUSD)": "Investment Range (MMUSD)",
    "Todos": "All",
    "### Resultados": "### Results",
    "Mostrando": "Showing",
    "proyecto(s)": "project(s)",
    "Sin Imagen": "No Image",
    "Sin Título": "Untitled",
    "**Sector:**": "**Sector:**",
    "**Inversión Est.:**": "**Est. Investment:**",
    "**TIR:**": "**IRR:**",
    "Ver Detalle Ficha": "View Details",
    "Ningún proyecto coindice con los filtros.": "No projects match the selected filters.",

    # Sectors (Dynamic Values)
    "Logistica": "Logistics",
    "Agro-Industrial ": "Agro-Industrial",
    "Servicios de Seguridad": "Security Services",
    "Alimentos": "Food",
    "Turismo e Industrial": "Tourism & Industrial",
    "Servicios - Petróleo": "Oilfield Services",
    "Logistica y Almacenamiento": "Logistics & Storage",
    "Ganadero": "Livestock",
    "Lacteos": "Dairy",
    "Agroindustria / Producción de alimentos": "Agribusiness / Food Production",
    "Minería y Metalurgia (hierro, escandio, sílice)": "Mining and Metallurgy (iron, scandium, silica)",
    "Agropecuaria de producción avícola": "Poultry Farming",
    "Industria alimentaria de procesamiento de carnes": "Meat Processing Food Industry",
    
    # Asset Types (Dynamic Values)
    "Compra total": "Full Acquisition",
    "Otro": "Other",
    "Expansión": "Expansion",
    "Proyecto nuevo": "Greenfield / New Project",
    
    # Risks (Dynamic Values)
    "Medio": "Medium",
    "Alto": "High",
    "Bajo": "Low",
    "Alto / Crítico": "High / Critical",
    "No Definido": "Undefined",

    # Column mappings (to dynamically translate DF keys if needed for displaying)
    "ID_Proyecto": "Project_ID",
    "Numero de Proyecto": "Project Number",
    "Nombre de la oportunidad": "Opportunity Name",
    "Ubicación (Región – Ciudad)": "Location (Region - City)",
    "Fecha de evaluación": "Evaluation Date",
    "Elaborado por": "Prepared by",
    "Resumen del negocio": "Business Summary",
    "Monto de inversión estimado (MMUSD)": "Estimated Investment (MMUSD)",
    "VPN (MMUSD)": "NPV (MMUSD)",
    "TIR (%)": "IRR (%)",
    "Nivel de riesgo global": "Global Risk Level",
    "Nombre": "Name",
    "Cargo": "Position",
    "Empresa": "Company",
    "Teléfono": "Phone",
    "Correo": "Email",

    # View: 2_Gestor_de_Proyectos
    "🛠️ Gestor de Proyectos": "🛠️ Project Manager",
    "Panel de administración para agregar o actualizar oportunidades de inversión.": "Administration panel to add or update investment opportunities.",
    "Operación a realizar": "Operation to perform",
    "Crear Nuevo Proyecto": "Create New Project",
    "Actualizar Proyecto Existente": "Update Existing Project",
    "Seleccione el Proyecto": "Select Project",
    "Datos de Identificación": "Identification Data",
    "Información del Proyecto": "Project Information",
    "Datos Financieros y Riesgo": "Financial and Risk Data",
    "Contacto (Opcional)": "Contact (Optional)",
    "Imagen del Proyecto": "Project Image",
    "Subir archivo": "Upload file",
    "Guardar Proyecto": "Save Project",

    # View: 3_Detalle_Proyecto
    "📑 Detalle de Proyecto": "📑 Project Details",
    "Volver a la Galería": "Back to Gallery",
    "Debe seleccionar un proyecto desde la galería de inversiones.": "You must select a project from the investment gallery.",
    "Ficha del Proyecto:": "Project Profile:",
    "Ubicación:": "Location:",
    "Evaluado el:": "Evaluated on:",
    "Por:": "By:",
    "Resumen Ejecutivo": "Executive Summary",
    "📋 Información General": "📋 General Information",
    "**Tipo de Oportunidad:**": "**Asset Type:**",
    "**Nivel de Riesgo Global:**": "**Global Risk Level:**",
    "💰 Información Financiera": "💰 Financial Information",
    "**Monto de Inversión Est.:**": "**Est. Investment Amount:**",
    "**TIR Esperada:**": "**Expected IRR:**",
    "**Valor Presente Neto (VPN):**": "**Net Present Value (NPV):**",
    "MMUSD": "MMUSD",
    "📞 Contacto del Responsable": "📞 Representative Contact",
    "**Nombre:**": "**Name:**",
    "**Cargo:**": "**Position:**",
    "**Empresa:**": "**Company:**",
    "**Email:**": "**Email:**",
    "**Teléfono:**": "**Phone:**",

    # View: 4_Analisis_Comparativo
    "📈 Análisis Comparativo y Priorización": "📈 Comparative Analysis & Prioritization",
    "Visualiza y compara el portafolio actual de oportunidades de inversión jerarquizado por Riesgo, Valor Presente Neto (VPN) y Rentabilidad (TIR).": "Visualize and compare the current portfolio of investment opportunities ranked by Risk, Net Present Value (NPV), and Profitability (IRR).",
    "No hay datos disponibles en el portafolio para realizar el análisis comparativo.": "No data available in the portfolio for comparative analysis.",
    "📊 VPN vs Riesgo": "📊 NPV vs Risk",
    "📈 TIR vs Riesgo": "📈 IRR vs Risk",
    "🎯 Matriz de Priorización (TIR vs VPN)": "🎯 Prioritization Matrix (IRR vs NPV)",
    "Valor Presente Neto (VPN) por Perfil de Riesgo": "Net Present Value (NPV) by Risk Profile",
    "La burbuja representa el Monto Estimado de Inversión (MMUSD).": "Bubble size represents the Estimated Investment Amount (MMUSD).",
    "El tamaño de la burbuja representa el Monto Estimado de Inversión (MMUSD).": "Bubble size represents the Estimated Investment Amount (MMUSD).",
    "Tasa Interna de Retorno (TIR) por Perfil de Riesgo": "Internal Rate of Return (IRR) by Risk Profile",
    "Matriz de Atractividad: Rentabilidad vs Valor": "Attractiveness Matrix: Profitability vs Value",
    "Proyectos en el **cuadrante superior derecho** (Alta TIR, Alto VPN) representan las oportunidades más atractivas. El color indica su nivel de riesgo.": "Projects in the **upper right quadrant** (High IRR, High NPV) represent the most attractive opportunities. The color indicates their risk level.",
    "Valor Presente Neto (MMUSD)": "Net Present Value (MMUSD)",
    "Nivel de Riesgo Global": "Global Risk Level",
    "Inversión (MMUSD)": "Investment (MMUSD)",
    "TIR Esperada (%)": "Expected IRR (%)",
    "Valor Presente Neto Promedio (MMUSD)": "Average Net Present Value (MMUSD)",
    "Tasa Interna de Retorno (%)": "Internal Rate of Return (%)",
    "Riesgo Global": "Global Risk",
    "Alta Prioridad": "High Priority",
    "📋 Resumen Tabular": "📋 Tabular Summary",
    
    # Generic
    "Guardado Exitoso!": "Successfully Saved!",
    "Error al guardar:": "Error saving:",

    # Extras
    "Acceso a Invex Pro": "Invex Pro Login",
    "Por favor, introduce tus credenciales para acceder al portafolio de inversiones.": "Please enter your credentials to access the investment portfolio.",
    "Usuario": "Username",
    "Contraseña": "Password",
    "Ingresar": "Sign In",
    "Este usuario se encuentra inactivo.": "This user is inactive.",
    "Su acceso ha expirado.": "Your access has expired.",
    "Credenciales incorrectas": "Incorrect credentials.",
    "Error conectando con la base de datos de usuarios:": "Error connecting to the users database:",
}

def t(text, lang="es"):
    """
    Returns the translation of 'text' if 'lang' is 'en' (English).
    Otherwise returns the original text in Spanish.
    Defaults to original if translation is not found.
    """
    if not text:
        return text
        
    text_str = str(text).strip()
    
    if str(lang).lower().startswith('en'):
        return TRANSLATIONS.get(text_str, text)
    return text

def translate_df(df, lang="es"):
    """
    Translates categorical columns within a pandas DataFrame.
    It translates values based on English language if requested.
    """
    if str(lang).lower().startswith('es') or df.empty:
        return df

    # We do a deep copy to avoid replacing original cached DF
    df_trans = df.copy()

    # Columns we know have categorical data that needs translating
    cat_columns = ["Sector / Industria", "Tipo de oportunidad", "Nivel de riesgo global"]
    
    for col in cat_columns:
        if col in df_trans.columns:
            df_trans[col] = df_trans[col].apply(lambda x: t(x, lang) if pd.notna(x) else x)
            
    # Note: We won't translate the column header names here because the underlying
    # Views rely on exact python dictionary strings to retrieve rows.
    # Instead, we will map column headers only when displayed.
    return df_trans
