import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client

@st.cache_resource
def obtener_conexion() -> Client:
    """Establece y cachea la conexión con Supabase usando secretos de Streamlit."""
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        # Se corrigió la asignación inválida dentro de st.error
        st.error(f"Error de configuración en las credenciales: {e}")
        return None

@st.cache_data
def cargar_clientes(_conn: Client) -> pd.DataFrame:
    """Carga la tabla de clientes completa."""
    if not _conn:
        return pd.DataFrame()
    try:
        response = _conn.table("clientes").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.warning(f"No se pudo cargar la tabla clientes: {e}")
        return pd.DataFrame()

@st.cache_data
def cargar_tabla_generica(_conn: Client, tabla_nombre: str, columnas: list = None) -> pd.DataFrame:
    """Carga cualquier tabla específica solicitando solo las columnas deseadas a Supabase."""
    if not _conn:
        return pd.DataFrame()
    try:
        # Optimización: Se solicitan solo las columnas necesarias desde la base de datos
        query_cols = ",".join(columnas) if columnas else "*"
        response = _conn.table(tabla_nombre).select(query_cols).execute()
        
        df = pd.DataFrame(response.data)
        if df.empty and columnas:
            return pd.DataFrame(columns=columnas)
            
        return df.fillna("")
    except Exception as e:
        st.warning(f"No se pudo cargar la tabla {tabla_nombre}: {e}")
        return pd.DataFrame()
