import streamlit as st
import pandas as pd

# Función para VER Clientes
def ver_clientes(df_total):
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

# Función para CARGAR un Cliente Nuevo (Simulación activa)
def cargar_cliente():
    st.subheader("➕ Registro de Nuevo Cliente")
    with st.form("form_cliente_modulo", clear_on_submit=True):
        f_empresa = st.text_input("Nombre de la Empresa / Institución *")
        f_contacto = st.text_input("Nombre del Contacto")
        f_mail = st.text_input("Correo Electrónico")
        f_vendedor = st.text_input("Vendedor Asignado (Abrev.)")
        
        btn_cliente = st.form_submit_button("💾 Guardar Cliente")
        if btn_cliente and f_empresa:
            st.success(f"🎉 ¡Cliente '{f_empresa}' procesado estéticamente de forma modular!")
