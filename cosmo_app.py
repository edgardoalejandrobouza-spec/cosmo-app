import streamlit as st
from supabase import create_client, Client

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="Cosmo App — Cotizaciones", layout="wide")

# Inicializar la conexión usando las credenciales seguras de Streamlit
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📊 Monitoreo de Cotizaciones — CosmoBio")
st.markdown("---")

# Lista de columnas reales disponibles en tu tabla para los menús desplegables
COLUMNAS_DISPONIBLES = [
    "empresa", 
    "prov", 
    "cotizacion", 
    "contacto", 
    "descripcion", 
    "estado", 
    "pliego", 
    "email", 
    "seguimiento"
]

# ==========================================
# 2. FILTROS DINÁMICOS CON MENÚS DESPLEGABLES
# ==========================================
st.subheader("🔍 Filtros de búsqueda masiva configurable")

# Crear dos bloques de filtros independientes
col_f1_col, col_f1_txt = st.columns([1, 2])
col_f2_col, col_f2_txt = st.columns([1, 2])

with col_f1_col:
    # El usuario elige la columna para el Filtro 1
    columna_filtro_1 = st.selectbox("Filtrar por (Columna 1):", COLUMNAS_DISPONIBLES, index=0) # Por defecto: empresa
with col_f1_txt:
    # El usuario escribe el texto a buscar en esa columna
    texto_filtro_1 = st.text_input(f"Escribe el término para buscar en '{columna_filtro_1}':", key="txt_f1")

with col_f2_col:
    # El usuario elige la columna para el Filtro 2
    columna_filtro_2 = st.selectbox("Filtrar por (Columna 2):", COLUMNAS_DISPONIBLES, index=1) # Por defecto: prov
with col_f2_txt:
    # El usuario escribe el texto a buscar en esa columna
    texto_filtro_2 = st.text_input(f"Escribe el término para buscar en '{columna_filtro_2}':", key="txt_f2")


# ==========================================
# 3. LÓGICA DE PAGINACIÓN DE VISUALIZACIÓN
# ==========================================
REGISTROS_POR_PAGINA = 50

# Mantener el estado de la página actual en la sesión del navegador
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 0

# Detectar cambios en las columnas elegidas o en los textos para resetear la paginación a 0
if "ultimo_txt_f1" not in st.session_state: st.session_state.ultimo_txt_f1 = ""
if "ultimo_col_f1" not in st.session_state: st.session_state.ultimo_col_f1 = ""
if "ultimo_txt_f2" not in st.session_state: st.session_state.ultimo_txt_f2 = ""
if "ultimo_col_f2" not in st.session_state: st.session_state.ultimo_col_f2 = ""

hubo_cambios = (
    texto_filtro_1 != st.session_state.ultimo_txt_f1 or
    columna_filtro_1 != st.session_state.ultimo_col_f1 or
    texto_filtro_2 != st.session_state.ultimo_txt_f2 or
    columna_filtro_2 != st.session_state.ultimo_col_f2
)

if hubo_cambios:
    st.session_state.pagina_actual = 0
    st.session_state.ultimo_txt_f1 = texto_filtro_1
    st.session_state.ultimo_col_f1 = columna_filtro_1
    st.session_state.ultimo_txt_f2 = texto_filtro_2
    st.session_state.ultimo_col_f2 = columna_filtro_2

# Calcular rangos numéricos para la cláusula .range() de Supabase
inicio_rango = st.session_state.pagina_actual * REGISTROS_POR_PAGINA
fin_rango = inicio_rango + REGISTROS_POR_PAGINA - 1


# ==========================================
# 4. EJECUCIÓN DE LA CONSULTA EN SUPABASE
# ==========================================
try:
    # Iniciamos la consulta base apuntando a tu tabla de la nube
    query = supabase.table("cotizaciones_tbl").select("*")
    
    # Aplicar el primer filtro dinámico si el usuario escribió algo
    if texto_filtro_1:
        query = query.ilike(columna_filtro_1, f"%{texto_filtro_1}%")
        
    # Aplicar el segundo filtro dinámico si el usuario escribió algo
    if texto_filtro_2:
        query = query.ilike(columna_filtro_2, f"%{texto_filtro_2}%")
        
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
# ==========================================
# 6. GRÁFICO DE BARRAS: COTIZACIONES POR AÑO
# ==========================================
st.markdown("---")
st.subheader("📈 Volumen de Cotizaciones por Año")

try:
    # 1. Consulta SQL optimizada enviada a Supabase para agrupar por año
    # Usamos date_part o EXTRACT para sacar el año de la fecha real de forma ultra veloz
    query_grafico = supabase.table("cotizaciones_tbl") \
        .select("fecha_de_inicio") \
        .not.is_("fecha_de_inicio", "null") \
        .execute()
    
    if query_grafico.data:
        import pandas as pd
        import altair as alt

        # 2. Convertimos a DataFrame de Pandas
        df_grafico = pd.DataFrame(query_grafico.data)
        
        # Convertimos la columna a tipo datetime en Pandas para extraer el año
        df_grafico["fecha_de_inicio"] = pd.to_datetime(df_grafico["fecha_de_inicio"])
        df_grafico["Año"] = df_grafico["fecha_de_inicio"].dt.year
        
        # 3. Agrupamos y contamos cuántas cotizaciones hay por cada año
        df_resumen = df_grafico.groupby("Año").size().reset_index(name="Cantidad")
        
        # Aseguramos que el Año se muestre como texto para que el gráfico no le ponga comas (ej: 2,026)
        df_resumen["Año"] = df_resumen["Año"].astype(str)

        # 4. Creamos el gráfico de barras interactivo con Altair
        grafico_barras = alt.Chart(df_resumen).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            color="#1f77b4" # Color azul estándar, podés cambiarlo por el de tu marca
        ).encode(
            x=alt.X("Año:N", title="Año de Inicio", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Cantidad:Q", title="Total de Cotizaciones"),
            tooltip=["Año", "Cantidad"] # Muestra los datos exactos al pasar el mouse por encima
        ).properties(
            width=800,
            height=400
        ).interactive() # Permite hacer zoom o arrastrar el gráfico

        # 5. Renderizamos el gráfico ocupando todo el ancho de la pantalla
        st.altair_chart(grafico_barras, use_container_width=True)
        
        # Muestra una pequeña tabla resumen abajo por si querés ver los números exactos
        with st.expander("📊 Ver tabla de datos numéricos del gráfico"):
            st.dataframe(df_resumen.set_index("Año"), use_container_width=True)
            
    else:
        st.info("No hay datos de fechas disponibles para armar el gráfico.")

except Exception as e_grafico:
    st.error(f"No se pudo generar el gráfico de barras: {e_grafico}")



