import streamlit as st

def modulo_seguimientos_fnc(df):
    """Muestra la tabla de seguimientos en el módulo correspondiente."""
    st.subheader("📈 Listado de Seguimientos")
    
    if df is not None and not df.empty:
        st.success(f"Se encontraron {len(df)} seguimientos.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay registros de seguimientos disponibles para mostrar.")
