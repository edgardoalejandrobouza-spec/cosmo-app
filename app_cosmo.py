import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. IMPORTACIÓN DE TUS 6 MÓDULOS DE FORMA MODULAR
import modulo_cliente
import modulo_registro
import modulo_seguimiento
import formulario_cliente
import formulario_registro
import formulario_seguimiento

# 2. Configuración de la interfaz del navegador
st.set_page_config(page_title="Cosmo - Panel de Control", layout="wide", page_icon="🚀")

st.title("🚀 Sistema de Gestión Integral - Cosmo")
st.write("Panel unificado para administración y visualización de datos en tiempo real.")

# 3. Carga de Clientes Locales (Lectura fija desde GitHub)
@st.cache_data
def cargar_clientes_locales():
    ruta_archivo = "clientes_limpios.csv"
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo, sep=";")
        df.columns = ['ID', 'Zona Abrev.', 'Calificación', 'Estado', 'Vendedor', 'Empresa / Institución', 
                      'Rubro', 'Contacto', 'Email', 'Teléfono', 'Celular', 'Cargo', 'Sector', 
                      'Zona', 'Localidad/Subzona', 'Dirección', 'Web', 'Observaciones', 'iMaps']
        return df
    return pd.DataFrame()

df_total = cargar_clientes_locales()

# 4. Conexión a las planillas de Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos_drive(nombre_hoja, columnas_defecto):
    try:
        df = conn.read(worksheet=nombre_hoja, ttl="2s")
        if df.empty or columnas_defecto[0] not in df.columns:
            return pd.DataFrame(columns=columnas_defecto)
        return df
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)

# Cargamos registros y seguimientos desde la nube en paralelo
df_registros = cargar_datos_drive("Cotizaciones", ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"])
df_seguimientos = cargar_datos_drive("Seguimientos", ["ID Seg", "Fecha Acción", "Cliente", "Estado Actual", "Comentario/Detalle"])

# 5. CREACIÓN DE LAS 6 PESTAÑAS SOLICITADAS
tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg = st.tabs([
    "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
    "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento"
])

# Conectamos cada pestaña a su correspondiente archivo independiente .py
with tab_ver_cli:
    modulo_cliente.ver_clientes(df_total)

with tab_ver_reg:
    modulo_registro.ver_registros(df_registros)

with tab_ver_seg:
    modulo_seguimiento.ver_seguimientos(df_seguimientos)

with tab_car_cli:
    formulario_cliente.mostrar_formulario_cliente()

with tab_car_reg:
    formulario_registro.mostrar_formulario_registro(conn, df_registros)
   
with tab_car_seg:
    formulario_seguimiento.mostrar_formulario_seguimiento(conn, df_seguimientos)
  
