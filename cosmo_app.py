import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuración estética de la aplicación global
st.set_page_config(page_title="Cosmo - Módulo Clientes Directo", layout="wide", page_icon="🚀")
st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Visualización directa de clientes_tbl desde Supabase con filtros avanzados.")

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
        st.error(f"Error al procesar la tabla: {e}")
        return pd.DataFrame()

# 3. Ejecución del programa principal
conn_directa = iniciar_conexion_directa()

if conn_directa is not None:
    st.success("✅ ¡Conectado a Supabase de forma directa!")
    df_total = descargar_clientes_directo(conn_directa)
    
    if df_total is not None and not df_total.empty:
        # --- NUEVA SECCIÓN DE CRITERIOS DE BÚSQUEDA ---
        st.markdown("### 🔍 Criterios de Búsqueda y Filtrado")
        
        # Desplegable para seleccionar qué columnas se quieren auditar
        columnas_disponibles = list(df_total.columns)
        columnas_seleccionadas = st.multiselect(
            "⚙️ Selecciona las columnas para aplicar la búsqueda (puedes tildar varias):",
            options=columnas_disponibles,
            default=["Empresa / Institución", "Vendedor"]  # Filtros por defecto iniciales
        )
        
        # Cuadro de entrada de texto para escribir la búsqueda
        texto_busqueda = st.text_input("✍️ Escribe el término a buscar:")
        
        # Lógica de filtrado en tiempo real sobre el DataFrame
        df_filtrado = df_total.copy()
        if texto_busqueda and columnas_seleccionadas:
            # Creamos una máscara booleana para filtrar filas
            mascara = pd.Series(False, index=df_total.index)
            for col in columnas_seleccionadas:
                # Busca coincidencias de texto ignorando mayúsculas/minúsculas y manejando nulos
                coincidencia = df_total[col].astype(str).str.contains(texto_busqueda, case=False, na=False)
                mascara = mascara | coincidencia
            df_filtrado = df_total[mascara]
        
        # --- RENDERIZADO DE TABLA ---
        st.subheader("👥 Listado General de Clientes (clientes_tbl)")
        st.write(f"Mostrando **{len(df_filtrado)}** de **{len(df_total)}** registros totales.")
        st.dataframe(df_filtrado, width="stretch", hide_index=True)

    else:
        st.warning("La tabla 'clientes_tbl' no devolvió registros.")
else:
    st.error("Fallo de autenticación con el servidor.")
