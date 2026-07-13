import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la interfaz del navegador
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")

st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# 2. Carga de Clientes Locales (Lectura fija de 8,200 filas desde GitHub)
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

# 3. Conexión y Auto-Creación de Columnas en Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_y_estructurar_drive(nombre_hoja, columnas_requeridas):
    try:
        # Intentamos leer la pestaña del Google Sheets
        df = conn.read(worksheet=nombre_hoja, ttl="2s")
        # Si la hoja está totalmente vacía o no tiene las columnas correctas, la automatizamos
        if df.empty or len(df.columns) < len(columnas_requeridas):
            df_inicial = pd.DataFrame(columns=columnas_requeridas)
            conn.update(worksheet=nombre_hoja, data=df_inicial)
            return df_inicial
        return df
    except Exception:
        # Si la pestaña ni siquiera existe, Python la crea con sus títulos correspondientes
        df_inicial = pd.DataFrame(columns=columnas_requeridas)
        try:
            conn.update(worksheet=nombre_hoja, data=df_inicial)
        except Exception:
            pass
        return df_inicial

# Automatizamos la creación de columnas para ambas hojas en paralelo
columnas_cotizaciones = ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"]
columnas_seguimientos = ["ID Seg", "Fecha Acción", "Cliente", "Estado Actual", "Comentario/Detalle"]

df_registros = cargar_y_estructurar_drive("Cotizaciones", columnas_cotizaciones)
df_seguimientos = cargar_y_estructurar_drive("Seguimientos", columnas_seguimientos)

# 4. CREACIÓN DE LAS PESTAÑAS VISUALES
tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg, tab_mod_reg = st.tabs([
    "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
    "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento", "✏️ Modificar Registro"
])

# PESTAÑA 1: VISUALIZACIÓN DE CLIENTES
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

# PESTAÑA 2: VISUALIZACIÓN DE REGISTROS (Cotizaciones)
with tab_ver_reg:
    st.subheader("🗂️ Historial de Cotizaciones en la Nube")
    st.dataframe(df_registros, use_container_width=True, hide_index=True)

# PESTAÑA 3: VISUALIZACIÓN DE SEGUIMIENTOS
with tab_ver_seg:
    st.subheader("📉 Panel de Seguimientos y Novedades")
    st.dataframe(df_seguimientos, use_container_width=True, hide_index=True)

# PESTAÑA 4: FORMULARIO CARGAR CLIENTE
with tab_car_cli:
    st.subheader("➕ Registro de Nuevo Cliente")
    st.info("Simulación local activa para revisión estética.")

# PESTAÑA 5: FORMULARIO CARGAR REGISTRO (Escribe en la pestaña Cotizaciones)
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
            
        btn_registro = st.form_submit_button("💾 Guardar Cotización")
        if btn_registro and f_coti_emp:
            nuevo_id = len(df_registros) + 1
            nueva_fila = pd.DataFrame([{"ID Coti": nuevo_id, "Fecha": f_fecha_coti.strftime("%Y-%m-%d"), "Empresa": f_coti_emp, "Detalle/Pliego": f_pliego, "Monto": f_monto}])
            df_actualizado = pd.concat([df_registros, nueva_fila], ignore_index=True)
            conn.update(worksheet="Cotizaciones", data=df_actualizado)
            st.cache_data.clear()
            st.success(f"🎉 ¡Cotización guardada en 'Cotizaciones' bajo el ID #{nuevo_id}!")

# PESTAÑA 6: FORMULARIO CARGAR SEGUIMIENTO (Escribe en la pestaña Seguimientos)
with tab_car_seg:
    st.subheader("➕ Registrar Acción de Seguimiento")
    with st.form("form_seguimiento_real", clear_on_submit=True):
        f_seg_emp = st.text_input("Empresa / Cliente *")
        f_estado_seg = st.selectbox("Estado Actual", ["Pendiente", "Llamar Mañana", "Pospuesto", "Presentado", "Ganado", "Perdido"])
        f_comentario = st.text_area("Detalle de la conversación / Novedad")
        f_fecha_seg = st.date_input("Fecha de Registro", datetime.now())
        
        btn_seg = st.form_submit_button("💾 Registrar Seguimiento")
        if btn_seg and f_seg_emp:
            nuevo_id_seg = len(df_seguimientos) + 1
            nueva_fila_seg = pd.DataFrame([{"ID Seg": nuevo_id_seg, "Fecha Acción": f_fecha_seg.strftime("%Y-%m-%d"), "Cliente": f_seg_emp, "Estado Actual": f_estado_seg, "Comentario/Detalle": f_comentario}])
            df_act_seg = pd.concat([df_seguimientos, nueva_fila_seg], ignore_index=True)
            conn.update(worksheet="Seguimientos", data=df_act_seg)
            st.cache_data.clear()
            st.success(f"🎉 ¡Seguimiento guardado exitosamente bajo el ID #{nuevo_id_seg}!")

# PESTAÑA 7: MODIFICAR REGISTRO
with tab_mod_reg:
    st.subheader("✏️ Modificar Cotización Existente")
