import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_formulario_registro(conn, df_registros):
    st.subheader("➕ Carga de Nueva Cotización Comercial")
    
    with st.form("form_registro_real", clear_on_submit=True):
        f_coti_emp = st.text_input("Empresa Solicitante *")
        f_pliego = st.text_area("Detalle del Pliego / Equipos Cotizados")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            f_monto = st.number_input("Monto Estimado ($)", min_value=0.0, format="%.2f")
        with col_r2:
            f_fecha_coti = st.date_input("Fecha de Cotización", datetime.now())
            
        btn_registro = st.form_submit_button("💾 Guardar Cotización")
        if btn_registro and f_coti_emp:
            # Enlace universal del documento explícito para el guardado
            url_doc = "https://google.com"
            
            nuevo_id = len(df_registros) + 1
            nueva_fila = pd.DataFrame([{
                "ID Coti": nuevo_id, 
                "Fecha": f_fecha_coti.strftime("%Y-%m-%d"), 
                "Empresa": f_coti_emp, 
                "Detalle/Pliego": f_pliego, 
                "Monto": f_monto
            }])
            df_actualizado = pd.concat([df_registros, nueva_fila], ignore_index=True)
            
            # Forzamos la actualización pasándole la dirección completa
            conn.update(spreadsheet=url_doc, worksheet="Cotizaciones", data=df_actualizado)
            st.cache_data.clear()
            st.success(f"🎉 ¡Cotización guardada exitosamente en Drive bajo el ID #{nuevo_id}!")
