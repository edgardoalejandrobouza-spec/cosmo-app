import streamlit as st

def ver_registros(df):
    """Muestra la tabla de registros en la pestaña correspondiente."""
    st.subheader("📊 Listado de Registros (Cotizaciones)")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} registros.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros disponibles para mostrar o la tabla está vacía.")
