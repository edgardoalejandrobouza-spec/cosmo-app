import streamlit as st
import pandas as pd

def mostrar_formulario_cliente(conn, df_total):
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
        
        btn_cliente = st.form_submit_button("💾 Guardar Cliente de Forma Real")
        if btn_cliente:
            if not f_empresa:
                st.error("⚠️ El nombre de la empresa es obligatorio para darle el alta.")
            else:
                # Intentamos leer si ya existe la pestaña en Drive, sino creamos una estructura limpia
                try:
                    df_existente = conn.read(worksheet="Clientes_Nuevos", ttl="0s")
                except Exception:
                    df_existente = pd.DataFrame(columns=["ID", "Empresa", "Contacto", "Email", "Teléfono", "Vendedor", "Rubro", "Zona", "Observaciones"])
                
                nuevo_id = len(df_existente) + 1
                nueva_fila = pd.DataFrame([{
                    "ID": nuevo_id,
                    "Empresa": f_empresa,
                    "Contacto": f_contacto,
                    "Email": f_mail,
                    "Teléfono": f_tel,
                    "Vendedor": f_vendedor,
                    "Rubro": f_rubro,
                    "Zona": f_zona,
                    "Observaciones": f_obs
                }])
                
                df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
                # Guardamos físicamente en una pestaña nueva en tu mismo Google Drive
                conn.update(worksheet="Clientes_Nuevos", data=df_actualizado)
                st.cache_data.clear()
                st.success(f"🎉 ¡El cliente '{f_empresa}' fue guardado de VERDAD en tu Google Sheets bajo el ID #{nuevo_id}!")
