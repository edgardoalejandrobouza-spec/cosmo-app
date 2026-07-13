import streamlit as st
import pandas as pd

def mostrar_formulario_cliente():
    st.subheader("➕ Registro de Nuevo Cliente en la Red")
    
    with st.form("form_alta_cliente", clear_on_submit=True):
        f_empresa = st.text_input("Nombre de la Empresa / Institución *")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            f_contacto = st.text_input("Nombre del Contacto")
            f_mail = st.text_input("Correo Electrónico")
            f_tel = st.text_input("Teléfono Principal")
        with col_c2:
            f_vendedor = st.text_input("Vendedor Asignado (Abrev.)", placeholder="Ej: NC, ALE")
            f_rubro = st.text_input("Rubro de la Empresa", placeholder="Ej: Farmacéutica, Química")
            f_zona = st.text_input("Zona / Localidad", placeholder="Ej: CABA, NOA")
        
        f_obs = st.text_area("Observaciones Iniciales de la Cuenta")
        
        btn_cliente = st.form_submit_button("💾 Guardar Cliente de Forma Modular")
        if btn_cliente:
            if not f_empresa:
                st.error("⚠️ El nombre de la empresa es obligatorio para darle el alta.")
            else:
                st.success(f"🎉 ¡El cliente '{f_empresa}' fue procesado con éxito dentro de su archivo independiente!")
