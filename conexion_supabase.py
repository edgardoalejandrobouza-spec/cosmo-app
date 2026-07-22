def obtener_conexion():
    """Inicializa y retorna la conexión limpia a Supabase."""
    try:
        # Usamos .get para una lectura más segura en entornos modulares
        url_sb = st.secrets.get("SUPABASE_URL")
        key_sb = st.secrets.get("SUPABASE_KEY")
        
        if not url_sb or not key_sb:
            st.error("Las claves SUPABASE_URL o SUPABASE_KEY no están definidas en los Secrets de Streamlit.")
            return None
            
        return st.connection("supabase", type=SupabaseConnection, url=url_sb, key=key_sb)
    except Exception as e:
        st.error(f"Error crítico en la configuración de credenciales: {e}")
        return None
