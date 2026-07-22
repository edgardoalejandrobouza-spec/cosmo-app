import streamlit as st

# Módulos de Visualización (Vistas exactas de tu Word)
import modulo_clientes
import modulo_registros
import modulo_seguimientos

# Módulos de Inserción (Formularios exactos de tu Word)
import formulario_clientes
import formulario_registros
import formulario_seguimientos

def renderizar_interfaz(conn, df_total, df_registros, df_seguimientos):
    """Renderiza las pestañas de control y ejecuta los módulos correspondientes."""
    
    # Creamos las 6 pestañas funcionales para la navegación de la app
    tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg = st.tabs([
        "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
        "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento"
    ])

    # Llamadas directas y simétricas a tus módulos de visualización
    with tab_ver_cli:
        modulo_clientes.ver_clientes(df_total)

    with tab_ver_reg:
        modulo_registros.ver_registros(df_registros)

    with tab_ver_seg:
        modulo_seguimientos.ver_seguimientos(df_seguimientos)

    # Llamadas directas y simétricas a tus formularios de inserción
    with tab_car_cli:
        formulario_clientes.mostrar_formulario_cliente(conn, df_total)

    with tab_car_reg:
        formulario_registros.mostrar_formulario_registro(conn, df_registros)

    with tab_car_seg:
        formulario_seguimientos.mostrar_formulario_seguimiento(conn, df_seguimientos)
