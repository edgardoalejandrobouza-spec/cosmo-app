
import streamlit as st

def ver_registros(df):
    """Muestra la tabla de cotizaciones/registros en la pestaña correspondiente."""
    st.subheader("📊 Listado de Cotizaciones Registradas")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} registros de cotizaciones.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros de cotizaciones disponibles para mostrar o la tabla está vacía.")
