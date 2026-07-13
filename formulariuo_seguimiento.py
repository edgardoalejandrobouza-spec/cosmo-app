import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_formulario_seguimiento(conn, df_seguimientos):
    st.subheader("➕ Registrar Acción de Seguimiento")
    
    with st.form("form_seguimiento_real", clear_on_submit=True):
        f_seg_emp = st.text_input("Empresa / Cliente *")
        f_estado_seg = st.selectbox("Estado Actual", ["Pendiente", "Llamar Mañana", "Pospuesto", "Presentado", "Ganado", "Perdido"])
        f_comentario = st.text_area("Detalle de la conversación / Novedad")
        f_fecha_seg = st.date_input("Fecha de Registro", datetime.now())
        
        btn_seg = st.form_submit_button("💾 Registrar Seguimiento")
        if btn_seg and f_seg_emp:
            nuevo_id_seg = len(df_seguimientos) + 1
            nueva_fila_seg = pd.DataFrame([{
                "ID Seg": nuevo_id_seg, 
                "Fecha Acción": f_fecha_seg.strftime("%Y-%m-%d"), 
                "Cliente": f_seg_emp, 
                "Estado Actual": f_estado_seg, 
                "Comentario/Detalle": f_comentario
            }])
            df_act_seg = pd.concat([df_seguimientos, nueva_fila_seg], ignore_index=True)
            conn.update(worksheet="Seguimientos", data=df_act_seg)
            st.cache_data.clear()
            st.success(f"🎉 ¡Seguimiento guardado exitosamente bajo el ID #{nuevo_id_seg}!")
