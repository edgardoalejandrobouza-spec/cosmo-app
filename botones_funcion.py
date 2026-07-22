import streamlit as st

# Importamos tus archivos reales usando alias para no romper el código de abajo
import ver_clientes as modulo_cliente
import ver_regitros as modulo_registro  # Respetamos el nombre "ver_regitros" sin la 's'
import ver_seguimientos as modulo_seguimiento
import cargar_clientes as formulario_cliente
import cargar_seguimientos as formulario_seguimiento

def renderizar_interfaz(conn, df_total, df_registros, df_seguimientos):
    """Renderiza las pestañas de control y ejecuta los módulos correspondientes."""
    
    # Creamos las 6 pestañas funcionales (unificando ver y cargar)
    tab_ver_cli, tab_ver_reg, tab_ver_seg, tab_car_cli, tab_car_reg, tab_car_seg = st.tabs([
        "📋 Ver Clientes", "📊 Ver Registros", "📈 Ver Seguimientos",
        "➕ Cargar Cliente", "➕ Cargar Registro", "➕ Cargar Seguimiento"
    ])

    # Enrutamiento a tus archivos de visualización
    with tab_ver_cli:
        modulo_cliente.ver_clientes(df_total)

    with tab_ver_reg:
        modulo_registro.ver_registros(df_registros)

    with tab_ver_seg:
        modulo_seguimiento.ver_seguimientos(df_seguimientos)

    # Enrutamiento a tus archivos de carga de datos
    with tab_car_cli:
        formulario_cliente.mostrar_formulario_cliente(conn, df_total)

    with tab_car_reg:
        # Nota: Como en tu lista falta el botón específico de cargar registro, 
        # usamos temporalmente el de seguimientos o el que definas para no romper el flujo
        st.info("Formulario de carga de registros en desarrollo o vinculación.")

    with tab_car_seg:
        formulario_seguimiento.mostrar_formulario_seguimiento(conn, df_seguimientos)
