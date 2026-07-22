import streamlit as st

def formulario_clientes_fnc(conn, df):
    """Renderiza el formulario de carga de clientes y guarda los datos en Supabase."""
    st.subheader("➕ Registro de Nuevo Cliente")
    st.write("Complete los datos requeridos para dar de alta un cliente en el sistema.")

    with st.form("nuevo_cliente_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            empresa_institucion = st.text_input("Empresa / Institución *")
            contacto = st.text_input("Nombre de Contacto *")
            mail = st.text_input("Correo Electrónico")
            telefono = st.text_input("Teléfono Fijo")
            celular = st.text_input("Celular")
            cargo = st.text_input("Cargo del Contacto")
            sector = st.text_input("Sector")
            
        with col2:
            zonaa = st.text_input("Zona Abrev. (Ej: CABA, GBA)")
            calificacion = st.selectbox("Calificación", ["A", "B", "C", "D"], index=0)
            estado_cliente = st.selectbox("Estado del Cliente", ["Activo", "Inactivo", "Potencial"], index=0)
            vendedor = st.text_input("Vendedor Asignado")
            zona = st.text_input("Zona Geográfica")
            subzona = st.text_input("Localidad / Subzona")
            direccion = st.text_input("Dirección Comercial")
            
        rubro = st.text_input("Rubro / Actividad")
        web = st.text_input("Sitio Web (URL)")
        imaps = st.text_input("Enlace iMaps / Google Maps")
        observaciones = st.text_area("Observaciones / Detalles adicionales")
        
        st.write("(*) Campos obligatorios")
        boton_guardar = st.form_submit_button("💾 Guardar Cliente en Supabase")

    if boton_guardar:
        if not empresa_institucion or not contacto:
            st.error("Por favor, complete los campos obligatorios (Empresa y Contacto).")
        else:
            try:
                nuevo_registro = {
                    "zonaa": zonaa,
                    "calificacion": calificacion,
                    "estado_cliente": estado_cliente,
                    "vendedor": vendedor,
                    "empresa_institucion": empresa_institucion,
                    "rubro": rubro,
                    "contacto": contacto,
                    "mail": mail,
                    "telefono": telefono,
                    "celular": celular,
                    "cargo": cargo,
                    "sector": sector,
                    "zona": zona,
                    "subzona": subzona,
                    "direccion": direccion,
                    "web": web,
                    "observaciones": observaciones,
                    "imaps": imaps
                }
                
                # Inserción usando el cliente oficial
                conn.table("clientes_tbl").insert(nuevo_registro).execute()
                st.success(f"¡Excelente! El cliente '{empresa_institucion}' fue registrado con éxito.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Hubo un error al guardar en la Base de Datos: {e}")
