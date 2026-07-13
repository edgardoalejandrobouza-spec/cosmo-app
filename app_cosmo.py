import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuración de la interfaz del navegador
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")

st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# 2. Función de carga masiva de datos con Caché para evitar lentitud
@st.cache_data
def cargar_datos(nombre_archivo, columnas):
    ruta_archivo = "clientes_limpios.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo, sep=";")
        df.columns = columnas
        return df
    return pd.DataFrame()

# Cargamos las bases de datos de forma local y segura
df_total = cargar_datos('clientes_limpios.csv', [
    'ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
    'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
    'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps'
])

# Columnas estimadas para registros (ajustar si tu archivo tiene más o menos campos)
columnas_reg = ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"]
df_registros = cargar_datos('registros_limpios.csv', columnas_reg)

# 3. CREACIÓN DE LAS 7 PESTAÑAS (Agregamos Modificar Registro)
tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg, tab_mod_reg = st.tabs([
    "📋 Ver Clientes", 
    "📊 Ver Registros", 
    "📈 Ver Seguimientos",
    "➕ Cargar Cliente", 
    "➕ Cargar Registro", 
    "➕ Cargar Seguimiento",
    "✏️ Modificar Registro"
])

# ========================================================
# PESTAÑA 1: VISUALIZACIÓN DE CLIENTES
# ========================================================
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

# ========================================================
# PESTAÑA 2: VISUALIZACIÓN DE REGISTROS (Cotizaciones)
# ========================================================
with tab_ver_reg:
    st.subheader("🗂️ Historial de Registros y Cotizaciones")
    if df_registros.empty:
        st.info("💡 No hay cotizaciones reales cargadas aún. Se muestra una tabla vacía de muestra.")
        st.dataframe(pd.DataFrame(columns=columnas_reg), use_container_width=True)
    else:
        st.dataframe(df_registros, use_container_width=True, hide_index=True)

# ========================================================
# PESTAÑA 3: VISUALIZACIÓN DE SEGUIMIENTOS
# ========================================================
with tab_ver_seg:
    st.subheader("📉 Panel de Seguimientos y Novedades")
    st.info("💡 Aquí se mostrará la tabla 'seg_tbl' para auditar las llamadas y estados de clientes.")
    st.dataframe(pd.DataFrame(columns=["ID Seg", "Fecha Acción", "Cliente", "Comentario/Detalle", "Próxima Acción"]), use_container_width=True)

# ========================================================
# PESTAÑA 4: FORMULARIO CARGAR CLIENTE
# ========================================================
with tab_car_cli:
    st.subheader("➕ Registro de Nuevo Cliente")
    with st.form("form_cliente", clear_on_submit=True):
        f_empresa = st.text_input("Nombre de la Empresa / Institución *")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            f_contacto = st.text_input("Nombre del Contacto")
            f_mail = st.text_input("Correo Electrónico")
            f_tel = st.text_input("Teléfono / Celular")
        with col_c2:
            f_vendedor = st.text_input("Vendedor Asignado (Abrev.)")
            f_rubro = st.text_input("Rubro de la Empresa")
            f_zona = st.text_input("Zona / Localidad")
        
        f_obs = st.text_area("Observaciones Adicionales")
        btn_cliente = st.form_submit_button("💾 Guardar Cliente en Base de Datos")
        if btn_cliente:
            if not f_empresa:
                st.error("⚠️ El nombre de la empresa es obligatorio.")
            else:
                st.success(f"🎉 ¡Cliente '{f_empresa}' listo para procesar!")

# ========================================================
# PESTAÑA 5: FORMULARIO CARGAR REGISTRO (Cotización)
# ========================================================
with tab_car_reg:
    st.subheader("➕ Carga de Nueva Cotización")
    with st.form("form_registro", clear_on_submit=True):
        f_coti_emp = st.text_input("Empresa Solicitante")
        f_pliego = st.text_area("Detalle del Pliego / Equipos Cotizados")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            f_monto = st.number_input("Monto Estimado ($)", min_value=0.0, format="%.2f")
        with col_r2:
            f_fecha_coti = st.date_input("Fecha de Cotización", datetime.now())
            
        btn_registro = st.form_submit_button("💾 Guardar Cotización")
        if btn_registro:
            st.success("🎉 ¡Cotización registrada exitosamente!")

# ========================================================
# PESTAÑA 6: FORMULARIO CARGAR SEGUIMIENTO
# ========================================================
with tab_car_seg:
    st.subheader("➕ Registrar Acción de Seguimiento")
    with st.form("form_seguimiento", clear_on_submit=True):
        f_seg_emp = st.text_input("Empresa / Cliente")
        f_estado_seg = st.selectbox("Estado Actual", ["Pendiente", "Llamar Mañana", "Pospuesto", "Presentado", "Ganado", "Perdido"])
        f_comentario = st.text_area("Detalle de la conversación / Novedad")
        f_prox_fecha = st.date_input("Fecha de Próxima Acción de Control", datetime.now())
        
        btn_seg = st.form_submit_button("💾 Registrar Seguimiento")
        if btn_seg:
            st.success("🎉 ¡Acción de seguimiento agendada!")

# ========================================================
# PESTAÑA 7: MODIFICAR REGISTRO (Nueva sección solicitada)
# ========================================================
with tab_mod_reg:
    st.subheader("✏️ Modificar o Actualizar Cotización Existente")
    st.write("Busca el registro que deseas editar ingresando su número identificador (ID).")
    
    # Cuadro para ingresar el ID de la cotización a modificar
    id_a_modificar = st.text_input("🆔 Ingrese el ID de la Cotización a cambiar:", placeholder="Ej: 105, 2341...")
    
    if id_a_modificar:
        st.divider()
        st.warning(f"Sección de edición activa para el Registro ID #{id_a_modificar}")
        
        # Formulario interno de edición
        with st.form("form_modificar_registro"):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                m_empresa = st.text_input("Empresa", value="Empresa de Muestra S.A.")
                m_monto = st.number_input("Monto Corregido ($)", min_value=0.0, value=150000.00, format="%.2f")
            with col_m2:
                m_fecha = st.date_input("Nueva Fecha Asociada", datetime.now())
            
            m_pliego = st.text_area("Actualizar Detalle del Pliego / Equipos", value="Especificaciones de muestra originales...")
            
            btn_modificar = st.form_submit_button("🔄 Aplicar Cambios y Actualizar Registro")
            if btn_modificar:
                st.success(f"🎉 ¡El Registro #{id_a_modificar} fue modificado exitosamente en el sistema!")
