import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuración estética de la aplicación global
st.set_page_config(page_title="Cosmo - Módulo Clientes Directo", layout="wide", page_icon="🚀")
st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Visualización directa de clientes_tbl desde Supabase (Sin archivos externos).")

# 1. Función de conexión integrada directamente aquí
def iniciar_conexion_directa() -> Client:
    """Inicializa el cliente oficial de Supabase leyendo los secrets."""
    try:
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Error: Las claves SUPABASE_URL o SUPABASE_KEY no están en los Secrets.")
            return None
            
        url_clean = url_sb.strip().rstrip('/')
        return create_client(url_clean, key_sb)
    except Exception as e:
        st.error(f"Error crítico de conexión: {e}")
        return None

# 2. Función de carga integrada directamente aquí
def descargar_clientes_directo(conn: Client) -> pd.DataFrame:
    """Trae los registros de clientes_tbl y mapea las columnas en español."""
    try:
        # Consulta directa a la tabla real de tu Supabase
        respuesta = conn.table("clientes_tbl").select("*").limit(1000).execute()
        
        if not respuesta or not hasattr(respuesta, 'data') or not respuesta.data:
            return pd.DataFrame()
            
        df = pd.DataFrame(respuesta.data)
        if df.empty:
            return pd.DataFrame()
            
        # Diccionario para pasar los nombres técnicos a nombres limpios en la pantalla
        mapeo_columnas = {
            'id_cliente': 'ID', 'zonaa': 'Zona Abrev.', 'calificacion': 'Calificación', 
            'estado_cliente': 'Estado', 'vendedor': 'Vendedor', 'empresa_institucion': 'Empresa / Institución', 
            'rubro': 'Rubro', 'contacto': 'Contacto', 'mail': 'Email', 'telefono': 'Teléfono',
            'celular': 'Celular', 'cargo': 'Cargo', 'sector': 'Sector', 'zona': 'Zona', 
            'subzona': 'Localidad/Subzona', 'direccion': 'Dirección', 'web': 'Web', 
            'observaciones': 'Observaciones', 'imaps': 'iMaps'
        }
        
        # Filtramos y renombramos solo las columnas que realmente existan en la BD
        columnas_existentes = [col for col in df.columns if col in mapeo_columnas]
        df = df[columnas_existentes]
        return df.rename(columns=mapeo_columnas)
    except Exception as e:
        st.error(f"Error al procesar la tabla: {e}")
        return pd.DataFrame()

# 3. Ejecución del programa principal
conn_directa = iniciar_conexion_directa()

if conn_directa is not None:
    st.success("✅ ¡Conectado a Supabase de forma directa desde cosmo_app.py!")
    
    # Ejecutamos la descarga de datos
    df_total = descargar_clientes_directo(conn_directa)
    
    if df_total is not None and not df_total.empty:
        st.write(f"Se encontraron **{len(df_total)}** registros en la tabla.")
        # Dibujamos la tabla interactiva de Streamlit ocupando todo el ancho
        st.dataframe(df_total, use_container_width=True, hide_index=True)
    else:
        st.warning("La tabla 'clientes_tbl' no devolvió registros o las columnas no coinciden.")
else:
    st.error("La aplicación no puede continuar porque falló la autenticación con el servidor.")
