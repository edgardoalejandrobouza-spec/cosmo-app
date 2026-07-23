import streamlit as st
import pandas as pd
from supabase import create_client, Client

def obtener_conexion():
    """Inicializa y retorna el cliente oficial y limpio de Supabase."""
    try:
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Las claves SUPABASE_URL o SUPABASE_KEY no están definidas en los Secrets.")
            return None
            
        return create_client(url_sb, key_sb)
    except Exception as e:
        st.error(f"Error crítico al conectar con Supabase: {e}")
        return None

def cargar_clientes(conn):
    """Trae los clientes ordenados y renombrados usando el cliente oficial con límite."""
    try:
        # Consultamos las filas de la tabla clientes_tbl
        respuesta = conn.table("clientes_tbl").select("*").limit(1000).execute()
        
        # Validar si la respuesta contiene datos válidos
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame()
            
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        # Diccionario de mapeo explícito para evitar errores por desajuste de longitud (20 columnas en DB)
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
            # Si hay una vigésima columna en tu base de datos, agrégala aquí abajo automáticamente:
            # 'nombre_columna_20': 'Etiqueta Interfaz'
        }
        
        # Filtramos solo las columnas que realmente llegaron desde la base de datos
        columnas_existentes = [col for col in df.columns if col in mapeo_columnas]
        df = df[columnas_existentes]
        
        # Renombramos de forma segura usando el diccionario
        df = df.rename(columns=mapeo_columnas)
        
        return df
    except Exception as e:
        st.error(f"Error al procesar columnas de clientes: {e}")
        return pd.DataFrame()

def cargar_tabla_generica(conn, nombre_tabla, columnas_defecto):
    """Trae datos de cotizaciones o seguimientos de forma genérica usando el cliente oficial."""
    try:
        respuesta = conn.table(nombre_tabla).select("*").execute()
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame(columns=columnas_defecto)
        df = pd.DataFrame(respuesta.data)
        return df if not df.empty else pd.DataFrame(columns=columnas_defecto)
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)
