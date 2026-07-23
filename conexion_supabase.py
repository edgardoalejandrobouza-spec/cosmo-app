import streamlit as st
import pandas as pd
from supabase import create_client, Client

def obtener_conexion():
    """Inicializa y retorna el cliente oficial de Supabase limpiando la URL."""
    try:
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Las claves SUPABASE_URL o SUPABASE_KEY no están definidas en los Secrets.")
            return None
            
        # Forzamos la limpieza de la URL por si quedó alguna barra en los Secrets
        url_clean = url_sb.strip().rstrip('/')
        return create_client(url_clean, key_sb)
    except Exception as e:
        st.error(f"Error crítico al conectar con Supabase: {e}")
        return None

def cargar_clientes(conn):
    """Trae los clientes de clientes_tbl usando mapeo seguro."""
    try:
        respuesta = conn.table("clientes_tbl").select("*").limit(1000).execute()
        
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame()
            
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        mapeo_columnas = {
            'id_cliente': 'ID', 'zonaa': 'Zona Abrev.', 'calificacion': 'Calificación', 
            'estado_cliente': 'Estado', 'vendedor': 'Vendedor', 'empresa_institucion': 'Empresa / Institución', 
            'rubro': 'Rubro', 'contacto': 'Contacto', 'mail': 'Email', 'telefono': 'Teléfono',
            'celular': 'Celular', 'cargo': 'Cargo', 'sector': 'Sector', 'zona': 'Zona', 
            'subzona': 'Localidad/Subzona', 'direccion': 'Dirección', 'web': 'Web', 
            'observaciones': 'Observaciones', 'imaps': 'iMaps'
        }
        
        columnas_existentes = [col for col in df.columns if col in mapeo_columnas]
        df = df[columnas_existentes]
        return df.rename(columns=mapeo_columnas)
    except Exception as e:
        st.error(f"Error al procesar columnas de clientes: {e}")
        return pd.DataFrame()

def cargar_tabla_generica(conn, nombre_tabla, columnas_defecto):
    """Trae datos de cualquier tabla secundaria de forma segura."""
    try:
        respuesta = conn.table(nombre_tabla).select("*").execute()
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame(columns=columnas_defecto)
        df = pd.DataFrame(respuesta.data)
        return df if not df.empty else pd.DataFrame(columns=columnas_defecto)
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)
