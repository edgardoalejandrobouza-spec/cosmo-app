import streamlit as st

def modulo_clientes_fnc(df):
    """Muestra la tabla de clientes en el módulo correspondiente."""
    st.subheader("📋 Listado de Clientes Registrados")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} clientes en la base de datos.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros de clientes disponibles para mostrar.")
