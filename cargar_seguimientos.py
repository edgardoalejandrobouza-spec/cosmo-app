import streamlit as st
import pandas as pd
from datetime import datetime

# Función para VER Seguimientos
def ver_seguimientos(df_seguimientos):
    st.subheader("📉 Panel de Seguimientos y Novedades")
    st.dataframe(df_seguimientos, use_container_width=True, hide_index=True)

# Función para CARGAR un Seguimiento (Guarda en Google Drive)
def cargar_seguimientos(conn, df_seguimientos):
    st.subheader("➕ Registrar Acción de Seguimiento")
    with st.form("form_seguimiento_modulo", clear_on_submit=True):
        f_seg_emp = st.text_input("Empresa / Cliente *")
        f_estado_seg = st.selectbox("Estado Actual", ["Pendiente", "Llamar Mañana", "Pospuesto", "Presentado", "Ganado", "Perdido"])
        f_comentario = st.text_area("Detalle de la conversación")
        f_fecha_seg = st.date_input("Fecha de Registro", datetime.now())
        
        btn_seg = st.form_submit_button("💾 Registrar Seguimiento")
        if btn_seg and f_seg_emp:
            nuevo_id_seg = len(df_seguimientos) + 1
            nueva_fila_seg = pd.DataFrame([{"ID Seg": nuevo_id_seg, "Fecha Acción": f_fecha_seg.strftime("%Y-%m-%d"), "Cliente": f_seg_emp, "Estado Actual": f_estado_seg, "Comentario/Detalle": f_comentario}])
            df_act_seg = pd.concat([df_seguimientos, nueva_fila_seg], ignore_index=True)
            conn.update(worksheet="Seguimientos", data=df_act_seg)
            st.cache_data.clear()
            st.success(f"🎉 ¡Seguimiento guardado exitosamente bajo el ID #{nuevo_id_seg}!")
