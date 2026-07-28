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
st.subheader("📈 Volumen de Cotizaciones por Año")

try:
    # Consulta limpia usando la sintaxis correcta sin barras invertidas
    query_grafico = (
        supabase.table("cotizaciones_tbl")
        .select("fecha_de_inicio")
        .not_.is_("fecha_de_inicio", "null")
        .execute()
    )
    
    if query_grafico.data:
        import pandas as pd
        import altair as alt

        df_grafico = pd.DataFrame(query_grafico.data)
        df_grafico["fecha_de_inicio"] = pd.to_datetime(df_grafico["fecha_de_inicio"])
        df_grafico["Año"] = df_grafico["fecha_de_inicio"].dt.year
        
        df_resumen = df_grafico.groupby("Año").size().reset_index(name="Cantidad")
        df_resumen["Año"] = df_resumen["Año"].astype(str)

        grafico_barras = alt.Chart(df_resumen).mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            color="#1f77b4"
        ).encode(
            x=alt.X("Año:N", title="Año de Inicio", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Cantidad:Q", title="Total de Cotizaciones"),
            tooltip=["Año", "Cantidad"]
        ).properties(
            width=800,
            height=400
        ).interactive()

        st.altair_chart(grafico_barras, use_container_width=True)
        
        with st.expander("📊 Ver tabla de datos numéricos del gráfico"):
            st.dataframe(df_resumen.set_index("Año"), use_container_width=True)
            
    else:
        st.info("No hay datos de fechas disponibles para armar el gráfico.")

except Exception as e_grafico:
    st.error(f"No se pudo generar el gráfico de barras: {e_grafico}")
