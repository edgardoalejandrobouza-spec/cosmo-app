import streamlit as st

# Módulos de Visualización (Vistas exactas de tu nomenclatura)
import modulo_clientes
import modulo_registros
import modulo_seguimientos

# Módulos de Inserción (Formularios exactos de tu nomenclatura)
import formulario_clientes
import formulario_registros
import formulario_seguimientos

def renderizar_interfaz(conn, df_total, df_registros, df_seguimientos):
    """Renderiza las pestañas de control y ejecuta los módulos correspondientes."""
    
    # Títulos de pestañas alineados al 100% con tu nomenclatura
    tab_mod_cli, tab_mod_reg, tab_mod_seg, tab_for_cli, tab_for_reg, tab_for_seg = st.tabs([
        "📋 Módulo Clientes", "📊 Módulo Registros", "📈 Módulo Seguimientos",
        "➕ Formulario Clientes", "➕ Formulario Registros", "➕ Formulario Seguimientos"
    ])

    # Llamadas a las funciones de visualización terminadas en _fnc
    with tab_mod_cli:
        modulo_clientes.modulo_clientes_fnc(df_total)

    with tab_mod_reg:
        modulo_registros.modulo_registros_fnc(df_registros)

    with tab_mod_seg:
        modulo_seguimientos.modulo_seguimientos_fnc(df_seguimientos)

    # Llamadas a las funciones de formularios terminadas en _fnc
    with tab_for_cli:
        formulario_clientes.formulario_clientes_fnc(conn, df_total)

    with tab_for_reg:
        formulario_registros.formulario_registros_fnc(conn, df_registros)

    with tab_for_seg:
        formulario_seguimientos.formulario_seguimientos_fnc(conn, df_seguimientos)
