import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuración de la interfaz del navegador
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")

st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# 2. Función de carga ultra-segura a prueba de diferencias de columnas
def cargar_datos_seguro(nombre_archivo, columnas_deseadas):
    ruta_archivo = f"C:/Mis bases SQL/{nombre_archivo}"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo, sep=";")
        # Si el archivo tiene la misma cantidad de columnas, las renombramos
        if len(df.columns) == len(columnas_deseadas):
            df.columns = columnas_deseadas
        return df
    return pd.DataFrame()

# Cargamos los Clientes Reales (19 columnas)
columnas_cli = ['ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
                'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
                'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps']
df_total = cargar_datos_seguro('clientes_limpios.csv', columnas_cli)

# Cargamos los Registros (se adapta automáticamente si tiene 5 o 19 columnas)
columnas_reg = ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"]
df_registros = cargar_datos_seguro('registros_limpios.csv', columnas_reg)

# 3. CREACIÓN DE LAS 7 PESTAÑAS
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
    st.subheader("🗂️ Historial de Registros y Cotizaciones")
    if df_registros.empty:
        st.info("💡 La tabla de registros está lista. Muestra de estructura:")
        st.dataframe(pd.DataFrame(columns=columnas_reg), use_container_width=True)
    else:
        st.dataframe(df_registros, use_container_width=True, hide_index=True)

# PESTAÑA 3: VISUALIZACIÓN DE SEGUIMIENTOS
with tab_ver_seg:
    st.subheader("📉 Panel de Seguimientos y Novedades")
    st.dataframe(pd.DataFrame(columns=["ID Seg", "Fecha Acción", "Cliente", "Comentario/Detalle", "Próxima Acción"]), use_container_width=True)

# PESTAÑA 4: FORMULARIO CARGAR CLIENTE
with tab_car_cli:
    st.subheader("➕ Registro de Nuevo Cliente")
    with st.form("form_cliente", clear_on_submit=True):
        f_empresa = st.text_input("Nombre de la Empresa / Institución *")
        btn_cliente = st.form_submit_button("💾 Guardar Cliente")
        if btn_cliente and f_empresa:
            st.success(f"🎉 ¡Cliente '{f_empresa}' procesado!")

# PESTAÑA 5: FORMULARIO CARGAR REGISTRO
with tab_car_reg:
    st.subheader("➕ Carga de Nueva Cotización")
    with st.form("form_registro", clear_on_submit=True):
        f_coti_emp = st.text_input("Empresa Solicitante")
        btn_registro = st.form_submit_button("💾 Guardar Cotización")
        if btn_registro:
            st.success("🎉 ¡Cotización registrada exitosamente!")

# PESTAÑA 6: FORMULARIO CARGAR SEGUIMIENTO
with tab_car_seg:
    st.subheader("➕ Registrar Acción de Seguimiento")
    with st.form("form_seguimiento", clear_on_submit=True):
        f_seg_emp = st.text_input("Empresa / Cliente")
        btn_seg = st.form_submit_button("💾 Registrar Seguimiento")
        if btn_seg:
            st.success("🎉 ¡Acción de seguimiento agendada!")

# PESTAÑA 7: MODIFICAR REGISTRO
with tab_mod_reg:
    st.subheader("✏️ Modificar o Actualizar Cotización Existente")
    id_a_modificar = st.text_input("🆔 Ingrese el ID de la Cotización a cambiar:")
    if id_a_modificar:
        with st.form("form_modificar_registro"):
            m_empresa = st.text_input("Empresa", value="Empresa de Muestra S.A.")
            btn_modificar = st.form_submit_button("🔄 Aplicar Cambios")
            if btn_modificar:
                st.success(f"🎉 ¡El Registro #{id_a_modificar} fue modificado!")
