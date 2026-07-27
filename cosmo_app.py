import streamlit as st
from supabase import create_client, Client

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="Cosmo App — Cotizaciones", layout="wide")

# Inicializar la conexión usando las credenciales seguras de Streamlit
# (Asegúrate de tenerlas configuradas en tu archivo .streamlit/secrets.toml)
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📊 Monitoreo de Cotizaciones — Cosmo App")
st.markdown("---")

# ==========================================
# 2. FILTROS DE BÚSQUEDA GLOBAL (PROCESADOS EN EL SERVIDOR)
# ==========================================
st.subheader("🔍 Filtros de búsqueda masiva")
col_filtro1, col_filtro2 = st.columns(2)

with col_filtro1:
    # Busca coincidencias de texto en las 11,303 filas
    busqueda_empresa = st.text_input("Buscar por nombre de empresa:")

with col_filtro2:
    # Permite escribir una provincia específica para filtrar la base entera
    busqueda_prov = st.text_input("Filtrar por Provincia (código / prov):")


# ==========================================
# 3. LÓGICA DE PAGINACIÓN DE VISUALIZACIÓN
# ==========================================
REGISTROS_POR_PAGINA = 50

# Mantener el estado de la página actual en la sesión del navegador
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 0

# Si el usuario escribe un nuevo filtro, reiniciamos la paginación a la página 0
if "ultimo_filtro_empresa" not in st.session_state:
    st.session_state.ultimo_filtro_empresa = ""
if "ultimo_filtro_prov" not in st.session_state:
    st.session_state.ultimo_filtro_prov = ""

if busqueda_empresa != st.session_state.ultimo_filtro_empresa or busqueda_prov != st.session_state.ultimo_filtro_prov:
    st.session_state.pagina_actual = 0
    st.session_state.ultimo_filtro_empresa = busqueda_empresa
    st.session_state.ultimo_filtro_prov = busqueda_prov

# Calcular rangos numéricos para la cláusula .range() de Supabase
inicio_rango = st.session_state.pagina_actual * REGISTROS_POR_PAGINA
fin_rango = inicio_rango + REGISTROS_POR_PAGINA - 1


# ==========================================
# 4. EJECUCIÓN DE LA CONSULTA EN SUPABASE
# ==========================================
try:
    # Iniciamos la consulta base apuntando a tu tabla de la nube
    query = supabase.table("cotizaciones_tbl").select("*")
    
    # Aplicar filtro de empresa si contiene texto (ignora mayúsculas/minúsculas)
    if busqueda_empresa:
        query = query.ilike("empresa", f"%{busqueda_empresa}%")
        
    # Aplicar filtro de provincia si contiene texto
    if busqueda_prov:
        query = query.ilike("prov", f"%{busqueda_prov}%")
        
    # Acotamos el resultado al bloque de la página actual (ej: filas 0 a 49)
    respuesta = query.range(inicio_rango, fin_rango).execute()
    datos_renderizar = respuesta.data

    # ==========================================
    # 5. RENDERIZADO DE INTERFAZ Y BOTONERA
    # ==========================================
    st.markdown("### Resultados")
    
    # Validar si la consulta arrojó registros con los filtros aplicados
    if not datos_renderizar:
        st.warning("No se encontraron registros que coincidan con los criterios de búsqueda.")
    else:
        # Botones de navegación Anterior / Siguiente
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        
        with col_nav1:
            if st.button("⬅️ Anterior") and st.session_state.pagina_actual > 0:
                st.session_state.pagina_actual -= 1
                st.rerun()
                
        with col_nav2:
            st.markdown(
                f"<center style='padding-top:10px;'>Mostrando registros del <b>{inicio_rango + 1}</b> al <b>{inicio_rango + len(datos_renderizar)}</b></center>", 
                unsafe_allow_html=True
            )
            
        with col_nav3:
            # Si el bloque está lleno, asumimos que quedan más registros en el servidor
            if len(datos_renderizar) == REGISTROS_POR_PAGINA:
                if st.button("Siguiente ➡️"):
                    st.session_state.pagina_actual += 1
                    st.rerun()

        # Desplegar la tabla interactiva de Streamlit ocupando todo el ancho
        st.dataframe(datos_renderizar, use_container_width=True)

except Exception as e:
    st.error(f"Error crítico al conectar o consultar Supabase: {e}")
