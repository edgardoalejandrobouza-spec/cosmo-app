import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# 1. IMPORTACIÓN DE TUS MÓDULOS MODULARES
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

# 3. Carga de Clientes Locales (Lectura de 8,200 filas desde GitHub)
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

# 4. CONEXIÓN DIRECTA Y SEGURA CON LAS CREDENCIALES INTEGRADAS
# Definimos el diccionario de la cuenta de servicio de forma limpia
info_servicio = {
    "type": "service_account",
    "project_id": "cosmo-sistema",
    "private_key_id": "e9be1576cecae786c5acb1e6910fc082d5c86dcc",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDJoT0Rv3bVGkSN\njW3k/3iSKSlCKLTzzfQ20TuFNS09st7A8fgHpZbzkqJp+WWQLXkhwHJv2UGwCscz\nxDIlnHrBoJiqf6Gdl8UUdMh7O7S6GVuavKWtC5Qc4gT1JF25chnQQYG7uL5OkCvQ\nBcWd849AHzTQBCDFTtp1qehZ/cCPMsVq92huFxpSNk5NaYRwhG7XNOhHyyi7988/\n1a/dZDWsLACAJsaE0576Z8HARwjk/7WfrtsQ/CltJkECBAfdgyR3tVaZ92zi2nl1\ntl4uoAStD9MBEuSirzH3uFAFkPyYTum34k7OuvOs4wQYoE6oDTkptw35o2doVFAz\njTntV3PVAgMBAAECggEACp80ZOV1wKc4Gk7rjadJtkV113bmhXuBlIu0O4HAJuJv\n6rE0lE6MY7uDU9rgF1bV7UnCnZLP65K9yMPasnGKY/3uXPkJThCLQNcgIqHUFQO1\n+DJc9f9Ip7bedP2b9GOG6Zox1+5VFDVzIWvUa8xDbSjXsuesxEgxqQYw5+C+zqxR\nmWWsc+Lt9+xWq2KMtyMdxtdhBI/EDLpBaMmWtA2e8BG6EtbfLm5wCkeElffFuh0x\nYTTXhIzrTOOUlXGMzfhoJFA2ocfCBUB7T9q+3LZg6CWrsDfFKA/+9Lt5/pGnYyHX\nWPuDqpx1K00HckxV/kxY8a+VcuuOrdsRpniU4wFG9wKBgQDomPSuedQBqS+3Poqd\nncybmgNdw5JoCW3NwYhSd5zPeN/xC9y/5NyGZX4yQ/j/2BsxS9T2EYr9L6fgSYul\n0tLultToLtOjU3u4N+K1cDo/LjxX6hIIIc8Xd/ElYqdDPncvr0h20rUrcrRyePrm\nuIXt5p3prbnJ25gLkzehQtKFkwKBgQDd6qUfyye1fyVRalrCqVr1rzkwWwLDjXqc\nF1ii3WUBAn6oFd0/XRLncRgP4Ds5XfGRT6Ux5gN67TxslSpSlIQVWQJSUQKoTax+\n2mN0lToWuVL0l27L+wZc9PnLKnvWlOKzx/P/fyVsTNpRKenS9cTR4KBExgkolfxV\nHxy8B2EB9wKBgC+nXsH8Xc41TnxZiOa/9LKQfE4SioVcIS39j6NttCfhmOf2yTRb\nfD7gvlkoCfTI3tFbuvbrIzG6OMe/6aeAqQyOxHIJXfzhVsCoWn9Xzecx3tUYNLeL\nzbT+Mt649pHVU2/mlo8ZnlqXdpbZaHYqqe3SyNmeaSkNH3qHn+cfHKiXAoGAeEuo\nMzHnVqWTzyx+AqPXYPMZZzMOrn7VBiRJsg+dnwyBKBCiHKURiFBwILsGn7RjLMgl\n3oS3Qj2z0ZCSnq1PZFsZvRGZBS8F4MX1v87c7FCNvXURZJWw/1b0ycM/2jRfJ+Gu\nTMPZv3lxpym3TNpVQQVHPLVKCEV5fa1lt/RIEUCgYB+6bWuzQKCkoAGeX+E3c/K\nN0QYXFda3H06+DEdJ+wnUnQ4DHZS/1auuCxFcPuHzRfCDT0UbsQpRgRm1uLckHdS\nERVKY8YpnyAbFnObOKpWGO97JEym3ksnOiUyZXbHHKRvSf6OwrBROKpl8xoqOUC6\nTW9WqzjagjXRzhj3VDoGiw==\n-----END PRIVATE KEY-----\n",
    "client_email": "cosmo-conector@://gserviceaccount.com",
    "client_id": "104098688315392941719",
    "auth_uri": "https://google.com",
    "token_uri": "https://googleapis.com",
    "auth_provider_x509_cert_url": "https://googleapis.com",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cosmo-conector%40://gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Nos conectamos pasando las credenciales directamente de forma nativa
conn = st.connection("gsheets", type=GSheetsConnection, credentials=info_servicio)

def cargar_datos_drive(nombre_hoja, columnas_defecto):
    try:
        # Pasamos el link universal explícito del documento directamente en la lectura
        url_doc = "https://google.com"
        df = conn.read(spreadsheet=url_doc, worksheet=nombre_hoja, ttl="1s")
        if df.empty or columnas_defecto not in df.columns:
            return pd.DataFrame(columns=columnas_defecto)
        return df
    except Exception:
        return pd.DataFrame(columns=columnas_defecto)

# Cargamos registros y seguimientos desde Google Sheets en vivo
df_registros = cargar_datos_drive("Cotizaciones", ["ID Coti", "Fecha", "Empresa", "Detalle/Pliego", "Monto"])
df_seguimientos = cargar_datos_drive("Seguimientos", ["ID Seg", "Fecha Acción", "Cliente", "Estado Actual", "Comentario/Detalle"])

# 5. CREACIÓN DE LAS 6 PESTAÑAS MODULARES
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
    formulario_cliente.mostrar_formulario_cliente(conn, df_total)

with tab_car_reg:
    formulario_registro.mostrar_formulario_registro(conn, df_registros)

with tab_car_seg:
    modulo_seguimiento.cargar_seguimiento(conn, df_seguimientos)
