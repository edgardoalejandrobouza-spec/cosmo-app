import streamlit as st
import pandas as pd
from supabase import create_client, Client

def obtener_conexion():
    """Inicializa y retorna el cliente oficial y limpio de Supabase, saneando la URL."""
    try:
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Las claves SUPABASE_URL o SUPABASE_KEY no están definidas en los Secrets.")
            return None
            
        # 🚨 LIMPIEZA DE URL: Elimina espacios y barras diagonales finales que rompen PostgREST
        url_sb = url_sb.strip().rstrip('/')
        
        return create_client(url_sb, key_sb)
    except Exception as e:
        st.error(f"Error crítico al conectar con Supabase: {e}")
        return None

def cargar_clientes(conn):
    """Trae los clientes de clientes_tbl usando el mapeo seguro por diccionario."""
    try:
        # Hacemos la consulta limpia a la tabla exacta que vimos en tu panel de Supabase
        respuesta = conn.table("clientes_tbl").select("*").limit(1000).execute()
        
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame()
            
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        # Diccionario con los nombres exactos en minúsculas de tu base de datos
        mapeo_columnas = {
            'id_cliente': 'ID', 
            'zonaa': 'Zona Abrev.', 
            'calificacion': 'Calificación', 
            'estado_cliente': 'Estado', 
            'vendedor': 'Vendedor',
            'empresa_institucion': 'Empresa / Institución', 
            'rubro': 'Rubro', 
            'contacto': 'Contacto', 
            'mail': 'Email', 
            'telefono': 'Teléfono',
            'celular': 'Celular', 
            'cargo': 'Cargo', 
            'sector': 'Sector', 
            'zona': 'Zona', 
            'subzona': 'Localidad/Subzona', 
            'direccion': 'Dirección',
            'web': 'Web', 
            'observaciones': 'Observaciones', 
            'imaps': 'iMaps'
        }
        
        # Filtramos y renombramos de forma segura sin romper por cantidad de columnas
        columnas_existentes = [col for col in df.columns if col in mapeo_columnas]
        df = df[columnas_existentes]
        df = df.rename(columns=mapeo_columnas)
        
        return df
    except Exception as e:
        st.error(f"Error al procesar columnas de clientes: {e}")
        return pd.DataFrame()
