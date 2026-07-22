import streamlit as st

def ver_clientes(df):
    """Recibe el DataFrame con los datos y dibuja la tabla en la pestaña correspondiente."""
    st.subheader("📋 Listado de Clientes Registrados")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} clientes en la base de datos.")
        # Muestra la tabla interactiva con buscador y filtros nativos
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros de clientes disponibles para mostrar o la tabla está vacía.")
