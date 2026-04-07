# -*- coding: utf-8 -*-
import streamlit as st
import os

# Configuracion de pagina
st.set_page_config(
    page_title="INVEX Pro",
    page_icon="mi_logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Corporativos (Inspirados en Stitch)
def inyectar_css():
    st.markdown("""
        <style>
        /* Variables de color de Grupo Reliarisk (basado en mocupuq Stitch) */
        :root {
            --primary-color: #144bb8;
            --bg-color: #f7f9fa;
        }
        
        /* Estilos generales */
        body {
            background-color: var(--bg-color);
        }
        
        /* Estilo para los titulos */
        h1, h2, h3 {
            color: var(--primary-color) !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Estilo de la barra lateral */
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid #e0e0e0;
        }
        
        /* Botones primarios */
        .stButton button {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
        }
        .stButton button:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            opacity: 0.9 !important;
        }
        
        /* Ajuste para que los links de navegacion se vean bien */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

def ocultar_sidebar():
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] { display: none; }
            [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)

from streamlit_gsheets import GSheetsConnection
import bcrypt
import pandas as pd
from datetime import datetime
import i18n

def login():
    lang = st.session_state.get("language", "es")
    d1, col, d2 = st.columns([1, 1.2, 1])
    with col:
        # Intenta cargar el logo si existe
        if os.path.exists("mi_logo.png"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("mi_logo.png", use_container_width=True)
            
        st.markdown(f"<h2 style='text-align: center;'>{i18n.t('Acceso a Invex Pro', lang)}</h2>", unsafe_allow_html=True)
        st.write(i18n.t("Por favor, introduce tus credenciales para acceder al portafolio de inversiones.", lang))
        
        with st.form("login_form"):
            username = st.text_input(i18n.t("Usuario", lang))
            password = st.text_input(i18n.t("Contraseña", lang), type="password")
            submitted = st.form_submit_button(i18n.t("Ingresar", lang))
            
            if submitted:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    users_df = conn.read(worksheet="invexpro_usuarios", ttl="5m")
                    users_df = users_df.dropna(subset=['username'])
                except Exception as e:
                    st.error(f"Error conectando con la base de datos de usuarios: {e}")
                    return
                
                # Buscamos el usuario
                user_match = users_df[users_df['username'].astype(str).str.strip() == username.strip()]
                
                if not user_match.empty:
                    user_record = user_match.iloc[0]
                    
                    # 1. Verificar si está activo
                    is_active_raw = str(user_record.get('active', '')).strip().upper()
                    if not (is_active_raw in ['TRUE', '1', '1.0', 'YES', 'SÍ', 'SI', 'VERDADERO']):
                        st.error("Este usuario se encuentra inactivo.")
                        return
                        
                    # 2. Verificar expiración
                    exp_date_val = user_record.get('expiration_date', '')
                    if pd.notna(exp_date_val) and str(exp_date_val).strip():
                        try:
                            if isinstance(exp_date_val, pd.Timestamp):
                                exp_date = exp_date_val.date()
                            else:
                                exp_date = datetime.strptime(str(exp_date_val).split()[0], "%Y-%m-%d").date()
                                
                            if datetime.now().date() > exp_date:
                                st.error("Su acceso ha expirado.")
                                return
                        except Exception:
                            pass
                            
                    # 3. Verificar contraseña cifrada
                    stored_hash = str(user_record.get('password_hash', '')).strip()
                    
                    try:
                        is_valid_pwd = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
                    except ValueError:
                        st.error("Error estructural en la contraseña de la base de datos.")
                        return
                        
                    if is_valid_pwd:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = str(user_record.get('access_type', 'inversor')).lower().strip()
                        st.session_state["name"] = str(user_record.get('name', username))
                        st.rerun()
                    else:
                        st.error(i18n.t("Credenciales incorrectas", lang))
                else:
                    st.error(i18n.t("Credenciales incorrectas", lang))

def main():
    inyectar_css()
    
    # Inicializar el estado de sesion
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "language" not in st.session_state:
        st.session_state["language"] = "es"
        
    lang = st.session_state["language"]

    if not st.session_state["logged_in"]:
        ocultar_sidebar()
        login_pg = st.Page(login, title=i18n.t("Acceso a Invex Pro", lang), icon="🔐")
        pg = st.navigation([login_pg], position="hidden")
        pg.run()
        return
        
    # Navegacion condicional (Usuario loggeado)
    pages = [
        st.Page("views/1_Galeria_de_Inversiones.py", title=i18n.t("Galería de Inversiones", lang), icon="📊"),
        st.Page("views/4_Analisis_Comparativo.py", title=i18n.t("Análisis Comparativo", lang), icon="📈"),
        st.Page("views/3_Detalle_Proyecto.py", title=i18n.t("Detalle de Proyecto", lang), icon="📑"),
    ]
    
    if st.session_state.get("role") == "admin":
        pages.append(st.Page("views/2_Gestor_de_Proyectos.py", title=i18n.t("Gestor de Proyectos", lang), icon="🛠️"))
    
    # IMPORTANTE: Usamos position="hidden" para ocultar el menu automatico y hacerlo manualmente
    pg = st.navigation(pages, position="hidden")
    
    # --- RENDERIZADO MANUAL DE LA BARRA LATERAL ---
    
    # 1. LOGO Y NOMBRE AL TOPE (GARANTIZADO)
    if os.path.exists("mi_logo.png"):
        c1, c2, c3 = st.sidebar.columns([0.2, 0.6, 0.2])
        with c2:
            st.image("mi_logo.png", use_container_width=True)
    
    st.sidebar.markdown(f"<h1 style='text-align: center; color: #144bb8; font-size: 1.8rem; margin-top: -10px; margin-bottom: 0;'>{i18n.t('Invex Pro', lang)}</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #e0e0e0; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)
    
    # 2. LINKS DE NAVEGACIÓN
    for p in pages:
        st.sidebar.page_link(p, label=p.title, icon=p.icon)
    
    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0 0.5rem 0;'>", unsafe_allow_html=True)
    
    # 3. IDIOMA Y USUARIO
    current_lang_idx = 0 if lang == "es" else 1
    new_lang_pref = st.sidebar.radio(
        i18n.t("Idioma / Language", lang), 
        ["Español", "English"], 
        index=current_lang_idx,
        key="lang_selector"
    )
    
    if ("es" if new_lang_pref == "Español" else "en") != lang:
        st.session_state["language"] = "es" if new_lang_pref == "Español" else "en"
        st.rerun()

    st.sidebar.write(f"{i18n.t('Bienvenido', lang)}, **{st.session_state.get('name', '')}**")
    
    if st.sidebar.button(i18n.t("Cerrar Sesión", lang)):
        st.session_state["logged_in"] = False
        st.session_state.clear()
        st.rerun()
        
    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0 0.5rem 0;'>", unsafe_allow_html=True)
             
    # Ejecutar la pagina seleccionada
    pg.run()

if __name__ == "__main__":
    main()
