import streamlit as st
import pandas as pd
from datetime import datetime

# Función para VER Cotizaciones
def ver_registros(df_registros):
    st.subheader("🗂️ Historial de Cotizaciones en la Nube")
    st.dataframe(df_registros, use_container_width=True, hide_index=True)

# Función para CARGAR Cotizaciones (Guarda en Google Drive)
def cargar_registro(conn, df_registros):
    st.subheader("➕ Carga de Nueva Cotización Comercial")
    with st.form("form_registro_modulo", clear_on_submit=True):
        f_coti_emp = st.text_input("Empresa Solicitante *")
        f_pliego = st.text_area("Detalle del Pliego / Equipos Cotizados")
        f_monto = st.number_input("Monto Estimado ($)", min_value=0.0, format="%.2f")
        f_fecha_coti = st.date_input("Fecha de Cotización", datetime.now())
            
        btn_registro = st.form_submit_button("💾 Guardar Cotización")
        if btn_registro and f_coti_emp:
            nuevo_id = len(df_registros) + 1
            nueva_fila = pd.DataFrame([{"ID Coti": nuevo_id, "Fecha": f_fecha_coti.strftime("%Y-%m-%d"), "Empresa": f_coti_emp, "Detalle/Pliego": f_pliego, "Monto": f_monto}])
            df_actualizado = pd.concat([df_registros, nueva_fila], ignore_index=True)
            conn.update(worksheet="Cotizaciones", data=df_actualizado)
            st.cache_data.clear()
            st.success(f"🎉 ¡Cotización guardada exitosamente bajo el ID #{nuevo_id}!")
