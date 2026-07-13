import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def mostrar_formulario_cliente(conn_vieja, df_total):
    st.subheader("➕ Registro de Nuevo Cliente en la Red")
    
    with st.form("form_alta_cliente", clear_on_submit=True):
        f_empresa = st.text_input("Nombre de la Empresa / Institución *")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            f_contacto = st.text_input("Nombre del Contacto")
            f_mail = st.text_input("Correo Electrónico")
            f_tel = st.text_input("Teléfono Principal")
        with col_c2:
            f_vendedor = st.text_input("Vendedor Asignado (Abrev.)", placeholder="Ej: NC, ALE")
            f_rubro = st.text_input("Rubro de la Empresa", placeholder="Ej: Farmacéutica, Química")
            f_zona = st.text_input("Zona / Localidad", placeholder="Ej: CABA, NOA")
        
        f_obs = st.text_area("Observaciones Iniciales de la Cuenta")
        
        btn_cliente = st.form_submit_button("💾 Guardar Cliente de Forma Real")
        if btn_cliente:
            if not f_empresa:
                st.error("⚠️ El nombre de la empresa es obligatorio para darle el alta.")
            else:
                # CONFIGURACIÓN NATIVA DE CREDENCIALES EXCLUSIVA PARA EL FORMULARIO
                credenciales_formulario = {
                    "type": "service_account",
                    "project_id": "cosmo-sistema",
                    "private_key_id": "e9be1576cecae786c5acb1e6910fc082d5c86dcc",
                    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDJoT0Rv3bVGkSN\njW3k/3iSKSlCKLTzzfQ20TuFNS09st7A8fgHpZbzkqJp+WWQLXkhwHJv2UGwCscz\nxDIlnHrBoJiqf6Gdl8UUdMh7O7S6GVuavKWtC5Qc4gT1JF25chnQQYG7uL5OkCvQ\nBcWd849AHzTQBCDFTtp1qehZ/cCPMsVq92huFxpSNk5NaYRwhG7XNOhHyyi7988/\n1a/dZDWsLACAJsaE0576Z8HARwjk/7WfrtsQ/CltJkECBAfdgyR3tVaZ92zi2nl1\ntl4uoAStD9MBEuSirzH3uFAFkPyYTum34k7OuvOs4wQYoE6oDTkptw35o2doVFAz\njTntV3PVAgMBAAECggEACp80ZOV1wKc4Gk7rjadJtkV113bmhXuBlIu0O4HAJuJv\n6rE0lE6MY7uDU9rgF1bV7UnCnZLP65K9yMPasnGKY/3uXPkJThCLQNcgIqHUFQO1\n+DJc9f9Ip7bedP2b9GOG6Zox1+5VFDVzIWvUa8xDbSjXsuesxEgxqQYw5+C+zqxR\nmWWsc+Lt9+xWq2KMtyMdxtdhBI/EDLpBaMmWtA2e8BG6EtbfLm5wCkeElffFuh0x\nYTTXhIzrTOOUlXGMzfhoJFA2ocfCBUB7T9q+3LZg6CWrsDfFKA/+9Lt5/pGnYyHX\nWPuDqpx1K00HckxV/kxY8a+VcuuOrdsRpniU4wFG9wKBgQDomPSuedQBqS+3Poqd\nncybmgNdw5JoCW3NwYhSd5zPeN/xC9y/5NyGZX4yQ/j/2BsxS9T2EYr9L6fgSYul\n0tLultToLtOjU3u4N+K1cDo/LjxX6hIIIc8Xd/ElYqdDPncvr0h20rUrcrRyePrm\nuIXt5p3prbnJ25gLkzehQtKFkwKBgQDd6qUfyye1fyVRalrCqVr1rzkwWwLDjXqc\nF1ii3WUBAn6oFd0/XRLncRgP4Ds5XfGRT6Ux5gN67TxslSpSlIQVWQJSUQKoTax+\n2mN0lToWuVL0l27L+wZc9PnLKnvWlOKzx/P/fyVsTNpRKenS9cTR4KBExgkolfxV\nHxy8B2EB9wKBgC+nXsH8Xc41TnxZiOa/9LKQfE4SioVcIS39j6NttCfhmOf2yTRb\nfD7gvlkoCfTI3tFbuvbrIzG6OMe/6aeAqQyOxHIJXfzhVsCoWn9Xzecx3tUYNLeL\nzbT+Mt649pHVU2/mlo8ZnlqXdpbZaHYqqe3SyNmeaSkNH3qHn+cfHKiXAoGAeEuo\nMzHnVqWTzyx+AqPXYPMZZzMOrn7VBiRJsg+dnwyBKBCiHKURiFBwILsGn7RjLMgl\n3oS3Qj2z0ZCSnq1PZFsZvRGZBS8F4MX1v87c7FCNvXURZJWw/1b0ycM/2jRfJ+Gu\nTMPZv3lxpym3TNpVQQVHPLVKCEV5fa1lt/RIEUCgYB+6bWuzQKCkoAGeX+E3c/K\nN0QYXFda3H06+DEdJ+wnUnQ4DHZS/1auuCxFcPuHzRfCDT0UbsQpRgRm1uLckHdS\nERVKY8YpnyAbFnObOKpWGO97JEym3ksnOiUyZXbHHKRvSf6OwrBROKpl8xoqOUC6\nTW9WqzjagjXRzhj3VDoGiw==\n-----END PRIVATE KEY-----\n",
                    "client_email": "cosmo-conector@://gserviceaccount.com",
                    "client_id": "104098688315392941719"
                }
                
                # Creamos una conexión limpia exclusiva para el guardado seguro
                conn_real = st.connection("gsheets_form_cli", type=GSheetsConnection, credentials=credenciales_google)
                url_doc = "https://google.com"
                
                try:
                    df_existente = conn_real.read(spreadsheet=url_doc, worksheet="Clientes_Nuevos", ttl="0s")
                except Exception:
                    df_existente = pd.DataFrame(columns=["ID", "Empresa", "Contacto", "Email", "Teléfono", "Vendedor", "Rubro", "Zona", "Observaciones"])
                
                nuevo_id = len(df_existente) + 1
                nueva_fila = pd.DataFrame([{
                    "ID": nuevo_id,
                    "Empresa": f_empresa,
                    "Contacto": f_contacto,
                    "Email": f_mail,
                    "Teléfono": f_tel,
                    "Vendedor": f_vendedor,
                    "Rubro": f_rubro,
                    "Zona": f_zona,
                    "Observaciones": f_obs
                }])
                
                df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
                conn_real.update(spreadsheet=url_doc, worksheet="Clientes_Nuevos", data=df_actualizado)
                st.cache_data.clear()
                st.success(f"🎉 ¡El cliente '{f_empresa}' fue guardado con éxito total en tu Google Sheets bajo el ID #{nuevo_id}!")
