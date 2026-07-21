import streamlit as st

# Conexión nativa oficial con Supabase
conn_sb = st.connection("supabase", type=st.connections.SupabaseConnection)

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
        return df[columnas_ordenadas] if not df.empty else pd.DataFrame(columns=columnas_ordenadas)
    except Exception as e:
        st.error(f"Error al conectar o leer desde Supabase: {e}")
        return pd.DataFrame()

# Reemplaza tu vieja línea de df_total por esta:
df_total = cargar_clientes_supabase()
