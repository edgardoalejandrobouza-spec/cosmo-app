@st.cache_data(ttl="5m")
def cargar_clientes(_conn): # 👈 AGREGÁ EL GUION BAJO AQUÍ
    """Trae los clientes ordenados y renombrados desde la base de datos."""
    try:
        respuesta = _conn.table("clientes_tbl").select("*").execute() # 👈 CAMBIÁ A _conn AQUÍ
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
