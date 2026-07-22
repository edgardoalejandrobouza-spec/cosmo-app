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
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        # 🚨 CORREGIDO: Mapeo estricto con los nombres en minúsculas que se ven en tu captura
        columnas_db = [
            'id_cliente', 'zonaa', 'calificacion', 'estado_cliente', 'vendedor',
            'empresa_institucion', 'rubro', 'contacto', 'mail', 'telefono',
            'celular', 'cargo', 'sector', 'zona', 'subzona', 'direccion',
            'web', 'observaciones', 'imaps'
        ]
        columnas_validas = [col for col in columnas_db if col in df.columns]
        df = df[columnas_validas]
        
        # Renombramos para la visualización en la interfaz del usuario de Streamlit
        df.columns = ['ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
                      'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
                      'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps'][:len(columnas_validas)]
        return df
    except Exception as e:
        st.error(f"Error al procesar columnas de clientes: {e}")
        return pd.DataFrame()

def cargar_tabla_generica(conn, nombre_tabla, columnas_defecto):
    """Trae datos de cotizaciones o seguimientos de forma genérica usando el cliente oficial."""
    try:
        respuesta = conn.table(nombre_tabla).select("*").execute()
        df = pd.DataFrame(respuesta.data)
        return df if not df.empty else pd.DataFrame(columns=columnas_defecto)
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)
