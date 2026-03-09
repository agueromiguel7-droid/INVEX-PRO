# -*- coding: utf-8 -*-
import streamlit as st
import os

# Configuracion de pagina
st.set_page_config(
    page_title="Invex Pro",
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
        </style>
    """, unsafe_allow_html=True)

def ocultar_sidebar():
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] {
                display: none;
            }
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

from streamlit_gsheets import GSheetsConnection
import bcrypt
import pandas as pd
from datetime import datetime

def login():
    d1, col, d2 = st.columns([1, 1.2, 1])
    with col:
        # Intenta cargar el logo si existe
        if os.path.exists("mi_logo.png"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("mi_logo.png", use_container_width=True)
            
        st.markdown("<h2 style='text-align: center;'>Acceso a Invex Pro</h2>", unsafe_allow_html=True)
        st.write("Por favor, introduce tus credenciales para acceder al portafolio de inversiones.")
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar")
            
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
                    # Aceptar como verdadero variaciones comunes en Google Sheets (incluída 'VADERO', 'SI', '1.0')
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
                            pass # Tratar de continuar si el formato de la fecha es inválido
                            
                    # 3. Verificar contraseña cifrada
                    stored_hash = str(user_record.get('password_hash', '')).strip()
                    
                    try:
                        is_valid_pwd = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
                    except ValueError:
                        # Ocurre si el stored_hash no tiene el formato de bcrypt válido
                        st.error("Error estructural en la contraseña de la base de datos.")
                        return
                        
                    if is_valid_pwd:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = str(user_record.get('access_type', 'inversor')).lower().strip()
                        st.session_state["name"] = str(user_record.get('name', username))
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")
                else:
                    st.error("Credenciales incorrectas")

def main():
    inyectar_css()
    
    # Inicializar el estado de sesion
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        ocultar_sidebar()
        # Si no esta loggeado, usar st.navigation unicamente con la pagina de login
        login_pg = st.Page(login, title="Acceder a Invex Pro", icon="🔐")
        pg = st.navigation([login_pg])
        pg.run()
        return
        
    # Navegacion condicional (Usuario loggeado)
    st.sidebar.title("Invex Pro")
    if os.path.exists("mi_logo.png"):
        c1, c2, c3 = st.sidebar.columns([1, 3, 1])
        with c2:
            st.image("mi_logo.png", use_container_width=True)
        
    st.sidebar.write(f"Bienvenido, **{st.session_state.get('name', '')}**")
    
    # Declarar paginas disponibles
    pages = []
    
    # Paginas para Inversor (y Admin)
    pages.append(st.Page("views/1_Galeria_de_Inversiones.py", title="Galería de Inversiones", icon="📊"))
    pages.append(st.Page("views/4_Analisis_Comparativo.py", title="Análisis Comparativo", icon="📈"))
    pages.append(st.Page("views/3_Detalle_Proyecto.py", title="Detalle de Proyecto", icon="📑"))
    
    # Paginas exclusivas de Admin
    if st.session_state.get("role") == "admin":
        pages.append(st.Page("views/2_Gestor_de_Proyectos.py", title="Gestor de Proyectos", icon="🛠️"))
    
    # Renderizar el menu lateral
    pg = st.navigation(pages)
    
    # Boton de logout
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["logged_in"] = False
        st.session_state.clear() # Limpiamos toda la sesion
        st.rerun()
        
    # Ejecutar la pagina seleccionada
    pg.run()

if __name__ == "__main__":
    main()
