import streamlit as st
import conexion_supabase as cns
import botones_funcion as btn

# Configuración estética de la aplicación global
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")
st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# Llama al primer archivo externo (Conexión)
conn = cns.obtener_conexion()

if conn is not None:
    # Lógica de carga sin conflictos de parámetros de caché
    df_total = cns.cargar_clientes(conn)
    df_registros = cns.cargar_tabla_generica(conn, "cotizaciones_tbl", ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"])
    df_seguimientos = cns.cargar_tabla_generica(conn, "seguimientos_tbl", ["ID Seg", "Fecha Acción", "Cliente", "Estado Actual", "Comentario/Detalle"])

    # Llama al segundo archivo externo (Botones y Funciones de Interfaz)
    btn.renderizar_interfaz(conn, df_total, df_registros, df_seguimientos)
else:
    st.error("No se pudo iniciar la aplicación debido a un fallo en el módulo de conexión.")
