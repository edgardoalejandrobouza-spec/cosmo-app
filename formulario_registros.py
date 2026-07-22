
import streamlit as st

def formulario_registros_fnc(conn, df):
    """Renderiza el formulario de carga de registros (cotizaciones) en Supabase."""
    st.subheader("➕ Cargar Nuevo Registro / Cotización")
    st.write("Complete los datos para registrar una nueva cotización en el sistema.")

    with st.form("nuevo_registro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha de Cotización")
            empresa = st.text_input("Empresa *")
            monto = st.number_input("Monto ($) *", min_value=0.0, step=100.0)
            
        with col2:
            detalle_pliego = st.text_area("Detalle / Pliego *", height=100)
            
        st.write("(*) Campos obligatorios")
        boton_guardar = st.form_submit_button("💾 Guardar Registro en Supabase")

    if boton_guardar:
        if not empresa or not detalle_pliego or monto <= 0:
            st.error("Por favor, complete los campos obligatorios y asegúrese de que el monto sea mayor a 0.")
        else:
            try:
                nuevo_registro = {
                    "fecha": str(fecha),
                    "empresa": empresa,
                    "detalle_pliego": detalle_pliego,
                    "monto": monto
                }
                
                # Inserción usando la sintaxis del cliente oficial de Supabase
                conn.table("registros_tbl").insert(nuevo_registro).execute()
                st.success(f"¡Excelente! La cotización para la empresa '{empresa}' fue registrada con éxito.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Hubo un error al guardar en la Base de Datos: {e}")
