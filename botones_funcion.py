import streamlit as st
import pandas as pd
from supabase import Client

def renderizar_interfaz(conn: Client, df_clientes: pd.DataFrame, df_cotizaciones: pd.DataFrame, df_seguimientos: pd.DataFrame):
    """Renderiza los componentes visuales, pestañas y botones del panel."""
    
    # Métricas clave en la parte superior
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Clientes", len(df_clientes) if not df_clientes.empty else 0)
    with col2:
        st.metric("Cotizaciones Activas", len(df_cotizaciones) if not df_cotizaciones.empty else 0)
    with col3:
        st.metric("Seguimientos Registrados", len(df_seguimientos) if not df_seguimientos.empty else 0)
        
    st.divider()

    # Creación de pestañas de navegación
    tab1, tab2, tab3 = st.tabs(["👥 Clientes", "📄 Cotizaciones", "📈 Seguimientos"])

    with tab1:
        st.subheader("Módulo de Clientes")
        if not df_clientes.empty:
            st.dataframe(df_clientes, use_container_width=True)
        else:
            st.info("No hay datos de clientes disponibles.")
            
        if st.button("🔄 Actualizar Clientes", key="btn_clientes"):
            st.cache_data.clear()
            st.rerun()

    with tab2:
        st.subheader("Historial de Cotizaciones")
        if not df_cotizaciones.empty:
            st.dataframe(df_cotizaciones, use_container_width=True)
        else:
            st.info("No hay registros en 'cotizaciones_tbl'.")
            
        if st.button("🔄 Actualizar Cotizaciones", key="btn_coti"):
            st.cache_data.clear()
            st.rerun()

    with tab3:
        st.subheader("Línea de Tiempo de Seguimientos")
        if not df_seguimientos.empty:
            st.dataframe(df_seguimientos, use_container_width=True)
        else:
            st.info("No hay registros en 'seguimientos_tbl'.")
            
        if st.button("🔄 Actualizar Seguimientos", key="btn_seg"):
            st.cache_data.clear()
            st.rerun()
