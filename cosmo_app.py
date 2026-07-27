import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuración estética de la aplicación global
st.set_page_config(page_title="Cosmo - Gestión Integral", layout="wide", page_icon="🚀")
st.title("🚀 Sistema de Gestión - CosmoBio")
st.write("Panel unificado para la administración, búsqueda e incorporación de clientes en tiempo real.")

# --- ESTILOS CSS AZUL CELESTE ---
st.markdown(
    """
    <style>
    span[data-baseweb="tag"] {
        background-color: #E0F7FA !important;
        color: #006064 !important;
        border: 1px solid #B2EBF2 !important;
        border-radius: 4px !important;
    }
    .stTextInput div[data-baseweb="input"] {
        border-color: #4DD0E1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 1. Función de conexión integrada
def iniciar_conexion_directa() -> Client:
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

# 2. Función de carga integrada (Limpia los "None" visuales)
def descargar_clientes_directo(conn: Client) -> pd.DataFrame:
    try:
        respuesta = conn.table("clientes_tbl").select("*").execute()
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
        df = df.rename(columns=mapeo_columnas)
        # Reemplaza los valores nulos o "None" por un espacio vacío para que la tabla sea más estética
        return df.fillna("")
    except Exception as e:
        st.error(f"Error al procesar la tabla: {e}")
        return pd.DataFrame()

# 3. Ejecución del programa principal
conn_directa = iniciar_conexion_directa()

if conn_directa is not None:
    # Creamos dos pestañas grandes para organizar el sistema de forma limpia
    pestana_visualizar, pestana_cargar = st.tabs(["📊 Visualización y Búsqueda", "➕ Incorporar Nuevo Cliente"])
    
    # --- PESTAÑA 1: VISUALIZACIÓN ---
    with pestana_visualizar:
        df_total = descargar_clientes_directo(conn_directa)
        
        if df_total is not None and not df_total.empty:
            st.markdown("### 🔍 Criterios de Búsqueda y Filtrado")
            columnas_disponibles = list(df_total.columns)
            columnas_seleccionadas = st.multiselect(
                "⚙️ Selecciona las columnas para aplicar la búsqueda:",
                options=columnas_disponibles,
                default=["Empresa / Institución", "Vendedor"]
            )
            
            texto_busqueda = st.text_input("✍️ Escribe el término a buscar:", key="buscar_input")
            
            df_filtrado = df_total.copy()
            if texto_busqueda and columnas_seleccionadas:
                mascara = pd.Series(False, index=df_total.index)
                for col in columnas_seleccionadas:
                    coincidencia = df_total[col].astype(str).str.contains(texto_busqueda, case=False, na=False)
                    mascara = mascara | coincidencia
                df_filtrado = df_total[mascara]
            
            st.subheader("👥 Listado General de Clientes (clientes_tbl)")
            st.write(f"Mostrando **{len(df_filtrado)}** de **{len(df_total)}** registros totales.")
            st.dataframe(df_filtrado, width="stretch", hide_index=True)
        else:
            st.warning("La tabla 'clientes_tbl' no devolvió registros.")
            
    # --- PESTAÑA 2: FORMULARIO DE CARGA ---
    with pestana_cargar:
        st.markdown("### 📝 Ficha de Registro de Cliente")
        st.write("Completa los datos en los casilleros. Los campos con (*) son obligatorios.")
        
        # Iniciamos el contenedor del formulario estructurado
        with st.form("formulario_alta_cliente", clear_on_submit=True):
            # Fila 1: Datos principales (Dividida en 3 columnas)
            c1, c2, c3 = st.columns(3)
            with c1:
                empresa = st.text_input("Empresa / Institución (*)")
                contacto = st.text_input("Nombre de Contacto")
                vendedor = st.text_input("Vendedor Asignado")
            with c2:
                rubro = st.text_input("Rubro Comercial")
                cargo = st.text_input("Cargo del Contacto")
                sector = st.text_input("Sector / Departamento")
            with c3:
                estado = st.selectbox("Estado del Cliente", ["Activo", "Inactivo", "Potencial", "En Seguimiento"])
                calificacion = st.text_input("Calificación (Ej: FNB, FNR)")
                zona_abrev = st.text_input("Zona Abrev. (Código)")
                
            st.divider()
            
            # Fila 2: Datos de localización y contacto
            c4, c5, c6 = st.columns(3)
            with c4:
                mail = st.text_input("Correo Electrónico (Email)")
                telefono = st.text_input("Teléfono Fijo")
                celular = st.text_input("Teléfono Celular")
            with c5:
                zona = st.text_input("Zona Geográfica")
                subzona = st.text_input("Localidad / Subzona")
                direccion = st.text_input("Dirección Física")
            with c6:
                web = st.text_input("Sitio Web (URL)")
                imaps = st.text_input("Enlace iMaps / Coordenadas")
                
            # Fila 3: Comentarios extensos ocupando todo el ancho
            observaciones = st.text_area("Observaciones o Comentarios adicionales")
            
            # Botón definitivo para procesar el envío
            boton_guardar = st.form_submit_button("💾 Guardar Cliente en Base de Datos", type="primary")
            
        # Lógica que se ejecuta al presionar el botón de Guardar
        if boton_guardar:
            if not empresa:
                st.error("❌ El campo 'Empresa / Institución' es obligatorio para registrar el cliente.")
            else:
                try:
                    # Armamos el diccionario vinculando tus palabras de los inputs con los nombres técnicos de Supabase
                    nuevo_registro = {
                        "empresa_institucion": empresa,
                        "contacto": contacto,
                        "vendedor": vendedor,
                        "rubro": rubro,
                        "cargo": cargo,
                        "sector": sector,
                        "estado_cliente": estado,
                        "calificacion": calificacion,
                        "zonaa": zona_abrev,
                        "mail": mail,
                        "telefono": telefono,
                        "celular": celular,
                        "zona": zona,
                        "subzona": subzona,
                        "direccion": direccion,
                        "web": web,
                        "imaps": imaps,
                        "observaciones": observaciones
                    }
                    
                    # Enviamos el comando INSERT a tu tabla real de Supabase
                    conn_directa.table("clientes_tbl").insert(nuevo_registro).execute()
                    
                    st.success(f"🎉 ¡El cliente '{empresa}' ha sido incorporado exitosamente a clientes_tbl!")
                    # Limpiamos la memoria caché para que la pestaña de visualización muestre al nuevo cliente de inmediato
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"❌ Error crítico al insertar el registro en Supabase: {e}")
else:
    st.error("Fallo de autenticación con el servidor.")
