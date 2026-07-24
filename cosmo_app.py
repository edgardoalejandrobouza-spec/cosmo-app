import streamlit as st
import conexion_supabase as cns

# Configuración estética de la aplicación global
st.set_page_config(page_title="Cosmo - Módulo Clientes", layout="wide", page_icon="🚀")
st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Visualización centralizada de la base de datos de clientes en tiempo real.")

# Llama al primer archivo externo (Conexión)
conn = cns.obtener_conexion()

if conn is not None:
    st.success("✅ Conexión con Supabase establecida con éxito.")
    
    # Intentamos cargar la tabla apuntando a tu función limpia
    st.subheader("👥 Listado General de Clientes (clientes_tbl)")
    df_total = cns.cargar_clientes_tbl(conn)
    
    # Validamos que el DataFrame contenga tus 8,218 registros antes de dibujarlo
    if df_total is not None and not df_total.empty:
        st.write(f"Se encontraron **{len(df_total)}** registros cargados en el sistema.")
        # Muestra la tabla interactiva ocupando todo el ancho de la pantalla
        st.dataframe(df_total, use_container_width=True)
    else:
        st.warning("⚠️ El DataFrame de clientes está vacío. Revisa que el nombre de la tabla en 'conexion_supabase.py' sea exactamente 'clientes_tbl'.")
        
    st.divider()
    st.info("💡 Nota: Las secciones de cotizaciones y seguimientos se pausaron temporalmente para limpiar la pantalla.")
else:
    st.error("No se pudo iniciar la aplicación debido a un fallo en el módulo de conexión.")
