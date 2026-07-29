import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA GLOBAL
# ==========================================
st.set_page_config(
    page_title="Cosmo App — Evaluación Estética", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar la pantalla por defecto en la sesión si no existe
if "seccion_activa" not in st.session_state:
    st.session_state.seccion_activa = "📊 Cotizaciones"

# Selector técnico para cambiar de estilo estético en tiempo real
st.sidebar.markdown("### 🛠️ Configuración Visual")
tipo_navegacion = st.sidebar.radio(
    "Elegí qué maquetación evaluar:",
    ["Botonera Superior (Horizontal)", "Barra Lateral (Vertical)"]
)
st.sidebar.markdown("---")

# ==========================================
# 2. IMPLEMENTACIÓN: BARRA LATERAL (VERTICAL)
# ==========================================
if tipo_navegacion == "Barra Lateral (Vertical)":
    st.sidebar.markdown("### 🗺️ Navegación Principal")
    
    # Creamos tres botones físicos verticales acoplados a la izquierda
    if st.sidebar.button("📊 Cotizaciones", use_container_width=True):
        st.session_state.seccion_activa = "📊 Cotizaciones"
        st.rerun()
        
    if st.sidebar.button("👥 Clientes", use_container_width=True):
        st.session_state.seccion_activa = "👥 Clientes"
        st.rerun()
        
    if st.sidebar.button("📋 Seguimientos", use_container_width=True):
        st.session_state.seccion_activa = "📋 Seguimientos"
        st.rerun()

# ==========================================
# 3. IMPLEMENTACIÓN: BOTONERA SUPERIOR (HORIZONTAL)
# ==========================================
st.title("🚀 Sistema de Gestión Integrado — Cosmo App")

if tipo_navegacion == "Botonera Superior (Horizontal)":
    # Creamos tres botones físicos distribuidos a lo ancho de la pantalla superior
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Resaltamos el botón activo con un borde usando markdown secundario de Streamlit
        if st.button("📊 Cotizaciones", use_container_width=True, type="secondary" if st.session_state.seccion_activa != "📊 Cotizaciones" else "primary"):
            st.session_state.seccion_activa = "📊 Cotizaciones"
            st.rerun()
            
    with col2:
        if st.button("👥 Clientes", use_container_width=True, type="secondary" if st.session_state.seccion_activa != "👥 Clientes" else "primary"):
            st.session_state.seccion_activa = "👥 Clientes"
            st.rerun()
            
    with col3:
        if st.button("📋 Seguimientos", use_container_width=True, type="secondary" if st.session_state.seccion_activa != "📋 Seguimientos" else "primary"):
            st.session_state.seccion_activa = "📋 Seguimientos"
            st.rerun()

st.markdown("---")

# ==========================================
# 4. ENRUTADOR DINÁMICO DE ARCHIVOS MODULARES
# ==========================================
st.subheader(f"📍 Sección actual: {st.session_state.seccion_activa}")

# Indicador visual para la evaluación estética
st.info(f"Evaluando diseño: **{tipo_navegacion}**")

if st.session_state.seccion_activa == "📊 Cotizaciones":
    try:
        import cosmo_cot
    except ModuleNotFoundError:
        st.warning("⚠️ Módulo de Cotizaciones listo para procesar ('cosmo_cot.py' no detectado aún).")

elif st.session_state.seccion_activa == "👥 Clientes":
    try:
        import cosmo_cli
    except ModuleNotFoundError:
        st.warning("⚠️ Módulo de Clientes listo para procesar ('cosmo_cli.py' no detectado aún).")

elif st.session_state.seccion_activa == "📋 Seguimientos":
    try:
        import cosmo_seg
    except ModuleNotFoundError:
        st.warning("⚠️ Módulo de Seguimientos listo para procesar ('cosmo_seg.py' no detectado aún).")
