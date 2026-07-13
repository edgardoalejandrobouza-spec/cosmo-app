import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la interfaz del navegador
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")

st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# 2. Conexiones a las bases de datos (Archivo local + Google Sheets)
@st.cache_data
def cargar_clientes_locales():
    ruta_archivo = "clientes_limpios.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo, sep=";")
        df.columns = ['ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
                      'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
                      'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps']
        return df
    return pd.DataFrame()

df_total = cargar_clientes_locales()

# Conexión nativa y segura con la planilla en la nube
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_registros_drive():
    try:
        # Intenta leer los datos de la hoja; si está vacía, crea la estructura inicial
        df = conn.read(ttl="5s") # Se refresca cada 5 segundos
        if df.empty or "ID Coti" not in df.columns:
            return pd.DataFrame(columns=["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"])
        return df
    except Exception:
        return pd.DataFrame(columns=["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"])

df_registros = cargar_registros_drive()

# 3. CREACIÓN DE LAS 7 PESTAÑAS
tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg, tab_mod_reg = st.tabs([
    "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
    "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento", "✏️ Modificar Registro"
])

# PESTAÑA 1: VISUALIZACIÓN DE CLIENTES (Buscador Masivo de 8,200 filas)
with tab_ver_cli:
    st.subheader("🔍 Explorador Centralizado de Clientes")
    if df_total.empty:
        st.error("❌ No se encontró el archivo de clientes.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            texto_busqueda = st.text_input("🏢 Empresa o Institución:", placeholder="Ej: Abbott, Universidad...", key="search_emp")
        with col2:
            vendedor_filtro = st.text_input("👤 Vendedor:", placeholder="Ej: NC, ALE...", key="search_vend")

        df_filtrado = df_total.copy()
        if texto_busqueda:
            df_filtrado = df_filtrado[df_filtrado["Empresa / Institución"].astype(str).str.contains(texto_busqueda, case=False, na=False)]
        if vendedor_filtro:
            df_filtrado = df_filtrado[df_filtrado["Vendedor"].astype(str).str.contains(vendedor_filtro, case=False, na=False)]

        st.subheader(f"📊 Registros Encontrados ({len(df_filtrado)})")
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

# PESTAÑA 2: VISUALIZACIÓN DE REGISTROS (Leídos desde Google Drive en vivo)
with tab_ver_reg:
    st.subheader("🗂️ Historial de Cotizaciones en la Nube")
    if df_registros.empty:
        st.info("💡 Aún no se han guardado cotizaciones. ¡Usa la pestaña 'Cargar Registro' para ingresar la primera!")
    else:
        st.dataframe(df_registros, use_container_width=True, hide_index=True)

# PESTAÑA 3: VISUALIZACIÓN DE SEGUIMIENTOS
with tab_ver_seg:
    st.subheader("📉 Panel de Seguimientos")
    st.dataframe(pd.DataFrame(columns=["ID Seg", "Fecha Acción", "Cliente", "Comentario/Detalle", "Próxima Acción"]), use_container_width=True)

# PESTAÑA 4: FORMULARIO CARGAR CLIENTE
with tab_car_cli:
    st.subheader("➕ Registro de Nuevo Cliente")
    st.info("Simulación local activa para revisión estética.")

# PESTAÑA 5: FORMULARIO CARGAR REGISTRO REAL (Guarda en Google Drive al presionar el botón)
with tab_car_reg:
    st.subheader("➕ Carga de Nueva Cotización Comercial")
    with st.form("form_registro_real", clear_on_submit=True):
        f_coti_emp = st.text_input("Empresa Solicitante *")
        f_pliego = st.text_area("Detalle del Pliego / Equipos Cotizados")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            f_monto = st.number_input("Monto Estimado ($)", min_value=0.0, format="%.2f")
        with col_r2:
            f_fecha_coti = st.date_input("Fecha de Cotización", datetime.now())
            
        btn_registro = st.form_submit_button("💾 Guardar Cotización en Google Drive")
        if btn_registro:
            if not f_coti_emp:
                st.error("⚠️ El nombre de la empresa es obligatorio.")
            else:
                # Generamos un ID autoincremental simple basado en las filas existentes
                nuevo_id = len(df_registros) + 1
                nueva_fila = pd.DataFrame([{
                    "ID Coti": nuevo_id,
                    "Fecha": f_fecha_coti.strftime("%Y-%m-%d"),
                    "Empresa": f_coti_emp,
                    "Detalle/Pliego": f_pliego,
                    "Monto": f_monto
                }])
                # Concatenamos y actualizamos la hoja de Google Drive de forma automática
                df_actualizado = pd.concat([df_registros, nueva_fila], ignore_index=True)
                conn.update(data=df_actualizado)
                st.cache_data.clear() # Limpiamos caché para ver el cambio al instante
                st.success(f"🎉 ¡Cotización registrada con éxito en tu Google Sheets bajo el ID #{nuevo_id}!")

# PESTAÑA 6: FORMULARIO CARGAR SEGUIMIENTO
with tab_car_seg:
    st.subheader("➕ Registrar Acción de Seguimiento")

# PESTAÑA 7: MODIFICAR REGISTRO
with tab_mod_reg:
    st.subheader("✏️ Modificar Cotización Existente")
