import streamlit as st
from supabase import create_client, Client
import datetime

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="Cosmo App — Cotizaciones", layout="wide")

# Inicializar la conexión usando las credenciales seguras de Streamlit
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📊 Monitoreo de Cotizaciones — Cosmo App")
st.markdown("---")

# Lista de columnas reales de tipo texto disponibles para los filtros dinámicos
COLUMNAS_FILTRABLES = [
    "empresa", 
    "prov", 
    "cotizacion", 
    "descripcion", 
    "estado", 
    "seguimiento",
    "email"
]

# ==========================================
# 2. FORMULARIO PARA CARGAR NUEVO REGISTRO
# ==========================================
with st.expander("➕ Cargar Nueva Cotización", expanded=False):
    with st.form("nuevo_registro_form", clear_on_submit=True):
        st.markdown("### Ingrese los datos de la cotización")
        
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            ins_cotizacion = st.text_input("Número de Cotización *")
            ins_empresa = st.text_input("Empresa / Cliente *")
            ins_prov = st.text_input("Provincia (código / prov) *")
        with f_col2:
            ins_email = st.text_input("Email")
            ins_estado = st.text_input("Estado")
            ins_fecha_ini = st.date_input("Fecha de Inicio", datetime.date.today())
        with f_col3:
            ins_pliego = st.number_input("ID Pliego (Número)", min_value=0, value=0)
            ins_contacto = st.number_input("ID Contacto / Cliente (Número)", min_value=0, value=0)
            
        ins_desc = st.text_area("Descripción de la cotización")
        ins_seg = st.text_area("Seguimiento / Notas")
        
        st.markdown("<small>* Campos obligatorios</small>", unsafe_allow_html=True)
        btn_guardar = st.form_submit_button("💾 Guardar Cotización en Supabase")
        
        if btn_guardar:
            if not ins_cotizacion or not ins_empresa or not ins_prov:
                st.error("Por favor, complete los campos obligatorios.")
            else:
                nuevo_registro = {
                    "cotizacion": ins_cotizacion,
                    "empresa": ins_empresa,
                    "prov": ins_prov,
                    "email": ins_email if ins_email else None,
                    "estado": ins_estado if ins_estado else None,
                    "fecha_de_inicio": ins_fecha_ini.strftime("%Y-%m-%d"),
                    "pliego": ins_pliego if ins_pliego > 0 else None, 
                    "contacto": ins_contacto if ins_contacto > 0 else None,
                    "descripcion": ins_desc if ins_desc else None,
                    "seguimiento": ins_seg if ins_seg else None,
                    "envio": None,        
                    "presupuesto": None   
                }
                
                try:
                    supabase.table("cotizaciones_tbl").insert(nuevo_registro).execute()
                    st.success("¡Registro guardado con éxito!")
                    st.rerun()
                except Exception as error_insert:
                    st.error(f"Error al insertar: {error_insert}")

st.markdown("---")

# ==========================================
# 3. FILTROS DINÁMICOS CON MENÚS DESPLEGABLES
# ==========================================
st.subheader("🔍 Filtros de búsqueda masiva configurable")

col_f1_col, col_f1_txt = st.columns([1, 2])
col_f2_col, col_f2_txt = st.columns([1, 2])

with col_f1_col:
    columna_filtro_1 = st.selectbox("Filtrar por (Columna 1):", COLUMNAS_FILTRABLES, index=0)
with col_f1_txt:
    texto_filtro_1 = st.text_input(f"Escribe el término para buscar en '{columna_filtro_1}':", key="txt_f1")

with col_f2_col:
    columna_filtro_2 = st.selectbox("Filtrar por (Columna 2):", COLUMNAS_FILTRABLES, index=1)
with col_f2_txt:
    texto_filtro_2 = st.text_input(f"Escribe el término para buscar en '{columna_filtro_2}':", key="txt_f2")


# ==========================================
# 4. LÓGICA DE PAGINACIÓN DE VISUALIZACIÓN
# ==========================================
REGISTROS_POR_PAGINA = 50
if "pagina_actual" not in st.session_state: 
    st.session_state.pagina_actual = 0

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

inicio_rango = st.session_state.pagina_actual * REGISTROS_POR_PAGINA
fin_rango = inicio_rango + REGISTROS_POR_PAGINA - 1


# ==========================================
# 5. EJECUCIÓN DE LA CONSULTA Y RENDERIZADO
# ==========================================
try:
    query = supabase.table("cotizaciones_tbl").select("*")
    if texto_filtro_1: 
        query = query.ilike(columna_filtro_1, f"%{texto_filtro_1}%")
    if texto_filtro_2: 
        query = query.ilike(columna_filtro_2, f"%{texto_filtro_2}%")
    
    respuesta = query.range(inicio_rango, fin_rango).execute()
    datos_renderizar = respuesta.data

    st.markdown("### Resultados")
    if not datos_renderizar:
        st.warning("No se encontraron registros.")
    else:
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        with col_nav1:
            if st.button("⬅️ Anterior") and st.session_state.pagina_actual > 0:
                st.session_state.pagina_actual -= 1
                st.rerun()
        with col_nav2:
            st.markdown(f"<center style='padding-top:10px;'>Mostrando del <b>{inicio_rango + 1}</b> al <b>{inicio_rango + len(datos_renderizar)}</b></center>", unsafe_allow_html=True)
        with col_nav3:
            if len(datos_renderizar) == REGISTROS_POR_PAGINA:
                if st.button("Siguiente ➡️"):
                    st.session_state.pagina_actual += 1
                    st.rerun()

        st.dataframe(datos_renderizar, use_container_width=True)

except Exception as e:
    st.error(f"Error crítico al conectar o consultar Supabase: {e}")

# ==========================================
# 6. GRÁFICO DE BARRAS: COTIZACIONES POR AÑO
# ==========================================
st.markdown("---")
st.subheader("📊 Volumen de Cotizaciones por Año")

try:
    # 1. Bucle inteligente para traer TODOS los 11,303 registros por bloques
    todos_los_datos_grafico = []
    bloque_size = 1000
    inicio = 0

    while True:
        respuesta_bloque = (
            supabase.table("cotizaciones_tbl")
            .select("fecha_de_inicio")
            .not_.is_("fecha_de_inicio", "null")
            .range(inicio, inicio + bloque_size - 1)
            .execute()
        )
        
        if not respuesta_bloque.data:
            break
            
        todos_los_datos_grafico.extend(respuesta_bloque.data)
        inicio += bloque_size

    if todos_los_datos_grafico:
        import pandas as pd

        # 2. Convertimos a DataFrame de Pandas
        df_grafico = pd.DataFrame(todos_los_datos_grafico)
        df_grafico["fecha_de_inicio"] = pd.to_datetime(df_grafico["fecha_de_inicio"])
        
        # Extraemos el Año como número entero para el gráfico nativo
        df_grafico["Año"] = df_grafico["fecha_de_inicio"].dt.year
        
        # 3. Agrupamos, contamos y reseteamos el índice de forma limpia
        df_resumen = df_grafico.groupby("Año").size().reset_index(name="Cantidad de Cotizaciones")
        
        # Configurar el Año como índice numérico puro
        df_resumen = df_resumen.set_index("Año")

        # 4. Renderizamos con st.bar_chart especificando la columna exacta a dibujar
        st.bar_chart(df_resumen, use_container_width=True)
        
        # Mantener tu tabla resumen abierta abajo
        with st.expander("📊 Ver tabla de datos numéricos del gráfico"):
            st.dataframe(df_resumen, use_container_width=True)
            
    else:
        st.info("No se encontraron registros con fechas válidas en toda la base de datos.")

except Exception as e_grafico:
    st.error(f"No se pudo generar el gráfico de barras: {e_grafico}")

# ==========================================
# 7. GRÁFICO DE BARRAS: VOLUMEN POR PROVEEDOR
# ==========================================
st.markdown("---")
st.subheader("🏢 Volumen de Cotizaciones por Proveedor")

try:
    # 1. Bucle inteligente para traer TODOS los 11,303 registros (columna prov)
    todos_los_datos_prov = []
    bloque_size = 1000
    inicio = 0

    while True:
        respuesta_bloque = (
            supabase.table("cotizaciones_tbl")
            .select("prov")
            .not_.is_("prov", "null")
            .range(inicio, inicio + bloque_size - 1)
            .execute()
        )
        
        if not respuesta_bloque.data:
            break
            
        todos_los_datos_prov.extend(respuesta_bloque.data)
        inicio += bloque_size

    if todos_los_datos_prov:
        import pandas as pd

        # 2. Convertimos a DataFrame de Pandas
        df_prov = pd.DataFrame(todos_los_datos_prov)
        
        # Limpieza: quitamos espacios en blanco vacíos que puedan venir en el texto
        df_prov["prov"] = df_prov["prov"].astype(str).str.strip()
        
        # 3. Agrupamos y contamos cuántas cotizaciones tiene cada proveedor
        df_resumen_prov = df_prov.groupby("prov").size().reset_index(name="Total Cotizaciones")
        
        # Ordenamos de mayor a menor para que la barra más larga quede arriba del todo
        df_resumen_prov = df_resumen_prov.sort_values(by="Total Cotizaciones", ascending=False)
        
        # Configuramos 'prov' como el índice para que Streamlit arme las etiquetas del eje correctamente
        df_resumen_prov = df_resumen_prov.set_index("prov")

        # 4. Renderizamos el gráfico nativo de Streamlit
        # Al no especificar orientación, si el índice es texto, Streamlit lo adapta de forma óptima
        st.bar_chart(df_resumen_prov, y="Total Cotizaciones", use_container_width=True)
        
        # Desplegamos la tabla numérica abajo en un expansor por si querés auditar las cifras exactas
        with st.expander("📊 Ver tabla analítica de proveedores"):
            st.dataframe(df_resumen_prov, use_container_width=True)
            
    else:
        st.info("No se encontraron registros de proveedores en la base de datos.")

except Exception as e_prov:
    st.error(f"No se pudo generar el diagrama de proveedores: {e_prov}")
