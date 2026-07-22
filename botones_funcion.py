import streamlit as st

# Importaciones de tus módulos externos originales
import modulo_cliente
import modulo_registro
import modulo_seguimiento
import formulario_cliente
import formulario_registro
import formulario_seguimiento

def renderizar_interfaz(conn, df_total, df_registros, df_seguimientos):
    """Renderiza las pestañas de control y ejecuta los módulos correspondientes."""
    
    # Creamos las 6 pestañas funcionales
    tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg = st.tabs([
        "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
        "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento"
    ])

    # Enrutamiento de las funciones de visualización
    with tab_ver_cli:
        modulo_cliente.ver_clientes(df_total)

    with tab_ver_reg:
        modulo_registro.ver_registros(df_registros)

    with tab_ver_seg:
        modulo_seguimiento.ver_seguimientos(df_seguimientos)

    # Enrutamiento de las funciones de carga en base de datos
    with tab_car_cli:
        formulario_cliente.mostrar_formulario_cliente(conn, df_total)

    with tab_car_reg:
        formulario_registro.mostrar_formulario_registro(conn, df_registros)

    with tab_car_seg:
        formulario_seguimiento.mostrar_formulario_seguimiento(conn, df_seguimientos)
