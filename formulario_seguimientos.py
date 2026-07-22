import streamlit as st

def formulario_seguimientos_fnc(conn, df):
    """Renderiza el formulario de carga de seguimientos comerciales en Supabase."""
    st.subheader("➕ Cargar Nuevo Seguimiento")
    st.write("Complete los datos para registrar una nueva acción de seguimiento sobre un cliente.")

    with st.form("nuevo_seguimiento_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha_accion = st.date_input("Fecha de la Acción")
            cliente = st.text_input("Cliente / Empresa *")
            estado_actual = st.selectbox("Estado Actual *", ["En Proceso", "Ganado", "Perdido", "Pendiente"], index=0)
            
        with col2:
            comentario_detalle = st.text_area("Comentario / Detalle de la Acción *", height=100)
            
        st.write("(*) Campos obligatorios")
        boton_guardar = st.form_submit_button("💾 Guardar Seguimiento en Supabase")

    if boton_guardar:
        if not cliente or not comentario_detalle:
            st.error("Por favor, complete los campos obligatorios (Cliente y Comentario).")
        else:
            try:
                nuevo_seguimiento = {
                    "fecha_accion": str(fecha_accion),
                    "cliente": cliente,
                    "estado_actual": estado_actual,
                    "comentario_detalle": comentario_detalle
                }
                
                # Inserción usando el cliente oficial de Supabase
                conn.table("seguimientos_tbl").insert(nuevo_seguimiento).execute()
                st.success(f"¡Excelente! El seguimiento para '{cliente}' fue registrado con éxito.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Hubo un error al guardar en la Base de Datos: {e}")

