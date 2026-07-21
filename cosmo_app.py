import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# Conexión nativa oficial con Supabase
conn_sb = st.connection("supabase", type=SupabaseConnection)

@st.cache_data(ttl="5m") # Cache de 5 minutos para optimizar el rendimiento de tu aplicación
def cargar_clientes_supabase():
    try:
        # Hacemos la consulta a tu nueva tabla clientes_tbl
        respuesta = conn_sb.table("clientes_tbl").select("*").execute()
        df = pd.DataFrame(respuesta.data)
        
        # Mapeamos los nombres de columnas idénticos a los de la base de datos
        columnas_ordenadas = [
            'id_cliente', 'zonaa', 'calificacion', 'estado_cliente', 'vendedor',
            'empresa_institucion', 'rubro', 'contacto', 'mail', 'telefono',
            'celular', 'cargo', 'sector', 'zona', 'subzona', 'direccion',
            'web', 'observaciones', 'imaps'
        ]
        
        if not df.empty:
            # Aseguramos que solo se seleccionen columnas existentes para evitar errores
            columnas_validas = [col for col in columnas_ordenadas if col in df.columns]
            return df[columnas_validas]
        else:
            return pd.DataFrame(columns=columnas_ordenadas)
            
    except Exception as e:
        st.error(f"Error al cargar datos desde Supabase: {e}")
        return pd.DataFrame()
