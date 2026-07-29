import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA GLOBAL
# ==========================================
st.set_page_config(
    page_title="Cosmo App — Panel de Control", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar la pantalla por defecto en la sesión si no existe
if "seccion_activa" not in st.session_state:
    st.session_state.seccion_activa = "cotizaciones"

st.title("🚀 Sistema de Gestión Integrado — Cosmo App")
st.markdown("---")

# ==========================================
# 2. MENU EN BARRA LATERAL (TRES BOTONES)
# ==========================================
st.sidebar.markdown("### 🗺️ Navegación Principal")

# Botón 1: Cotizaciones (Llama a cosmo_coti.py)
if st.sidebar.button("📊 Cotizaciones", use_container_width=True, type="primary" if st.session_state.seccion_activa == "cotizaciones" else "secondary"):
    st.session_state.seccion_activa = "cotizaciones"
    st.rerun()

# Botón 2: Clientes (Llama a cosmo_cli.py)
if st.sidebar.button("👥 Clientes", use_container_width=True, type="primary" if st.session_state.seccion_activa == "clientes" else "secondary"):
    st.session_state.seccion_activa = "clientes"
    st.rerun()

# Botón 3: Seguimientos (Llama a cosmo_seg.py)
if st.sidebar.button("📋 Seguimientos", use_container_width=True, type="primary" if st.session_state.seccion_activa == "seguimientos" else "secondary"):
    st.session_state.seccion_activa = "seguimientos"
    st.rerun()

st.sidebar.markdown("---")


# ==========================================
# 3. ENRUTADOR DINÁMICO DE ARCHIVOS MODULARES
# ==========================================

if st.session_state.seccion_activa == "cotizaciones":
    st.subheader("📍 Historial y Métricas de Cotizaciones")
    try:
        # Importa el archivo exacto solicitado
        import cosmo_coti
    except ModuleNotFoundError:
        st.error("⚠️ No se encontró el archivo 'cosmo_coti.py' en la raíz de tu proyecto.")

elif st.session_state.seccion_activa == "clientes":
    st.subheader("📍 Gestión y Registro de Clientes")
    try:
        import cosmo_cli
    except ModuleNotFoundError:
        st.error("⚠️ No se encontró el archivo 'cosmo_cli.py' en la raíz de tu proyecto.")

elif st.session_state.seccion_activa == "seguimientos":
    st.subheader("📍 Cronología de Seguimientos")
    try:
        import cosmo_seg
    except ModuleNotFoundError:
        st.error("⚠️ No se encontró el archivo 'cosmo_seg.py' en la raíz de tu proyecto.")
