import streamlit as st

def modulo_registros_fnc(df):
    """Muestra la tabla de registros en el módulo correspondiente."""
    st.subheader("📊 Listado de Registros (Cotizaciones)")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} registros.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros disponibles para mostrar o la tabla está vacía.")
