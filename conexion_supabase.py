import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

def obtener_conexion():
    """Inicializa y retorna la conexión limpia a Supabase."""
    try:
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Las claves SUPABASE_URL o SUPABASE_KEY no están definidas en los Secrets.")
            return None
            
        return st.connection("supabase", type=SupabaseConnection, url=url_sb, key=key_sb)
    except Exception as e:
        st.error(f"Error crítico en la configuración de credenciales: {e}")
        return None

def cargar_clientes(conn):
    """Trae los clientes ordenados y renombrados desde la base de datos."""
    try:
        respuesta = conn.table("clientes_tbl").select("*").execute()
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        columnas_db = [
            'id_cliente', 'zonaa', 'calificacion', 'estado_cliente', 'vendedor',
            'empresa_institucion', 'rubro', 'contacto', 'mail', 'telefono',
            'celular', 'cargo', 'sector', 'zona', 'subzona', 'direccion',
            'web', 'observaciones', 'imaps'
        ]
        columnas_validas = [col for col in columnas_db if col in df.columns]
        df = df[columnas_validas]
        
        df.columns = ['ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
                      'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
                      'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps'][:len(columnas_validas)]
        return df
    except Exception as e:
        st.error(f"Error al leer clientes: {e}")
        return pd.DataFrame()

def cargar_tabla_generica(conn, nombre_tabla, columnas_defecto):
    """Trae datos de cotizaciones o seguimientos de forma genérica."""
    try:
        respuesta = conn.table(nombre_tabla).select("*").execute()
        df = pd.DataFrame(respuesta.data)
        return df if not df.empty else pd.DataFrame(columns=columnas_defecto)
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)
