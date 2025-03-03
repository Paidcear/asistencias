import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Archivo JSON para almacenar los datos
data_file = "asistencias.json"

# Función para cargar los datos del archivo JSON
def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Función para guardar los datos en el archivo JSON
def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

# Función para reasignar IDs
def reassign_ids(data):
    for index, record in enumerate(data):
        record["id"] = index + 1
    return data

# Cargar datos iniciales
data = load_data()

# Panel lateral
st.sidebar.title("Gestión de Asistencias")
menu = st.sidebar.selectbox(
    "Opciones:",
    [
        "Registrar Asistencia",
        "Registrar Alumno",
        "Consultar Alumno",
        "Modificar Alumno",
        "Eliminar Alumno",
        "Mostrar Todos los Registros",
    ],
    index=0  # Establecer "Registrar Asistencia" como la opción predeterminada
)

# Restablecer Asistencias y Retardos
if st.sidebar.button("Restablecer Asistencias y Retardos", key="restablecer_button"):
    for record in data:
        record["Martes"]["asistencias"] = 0
        record["Martes"]["retardos"] = 0
        record["Miércoles"]["asistencias"] = 0
        record["Miércoles"]["retardos"] = 0
        record["Sábado"]["asistencias"] = 0
        record["Sábado"]["retardos"] = 0
    save_data(data)
    st.sidebar.success("Asistencias y retardos restablecidos a 0.")


# Registrar Asistencia (Opción predeterminada)
if menu == "Registrar Asistencia":
    st.title("Registrar Asistencias")
    asistencia_id = st.number_input("Ingresa el ID del Alumno:", min_value=1, step=1, format="%d")
    tipo = st.selectbox("Selecciona el tipo de registro:", ["Asistencia", "Retardo"], key="tipo_asistencia")
    dia = st.selectbox("Selecciona el día:", ["Martes", "Miércoles", "Sábado"], key="dia_asistencia")

    if st.button("Registrar", key="registrar_asistencia_action_button"):
        alumno = next((item for item in data if item["id"] == asistencia_id), None)
        if alumno:
            if dia not in alumno:
                alumno[dia] = {"asistencias": 0, "retardos": 0}  # Inicializa el día si no existe
            if tipo == "Asistencia":
                alumno[dia]["asistencias"] += 1
                st.success(f"Asistencia registrada para el alumno {alumno['nombre']} el {dia}.")
            elif tipo == "Retardo":
                alumno[dia]["retardos"] += 1
                st.success(f"Retardo registrado para el alumno {alumno['nombre']} el {dia}.")
            save_data(data)
        else:
            st.error("No se encontró ningún alumno con ese ID.")

# Registrar Alumno
elif menu == "Registrar Alumno":
    st.title("Registrar Nuevo Alumno")
    nombre = st.text_input("Nombre del Alumno:")
    nivel = st.selectbox("Nivel:", ["Licenciatura", "Bachillerato"])  # Opciones actualizadas

    if st.button("Registrar", key="registrar_alumno_button"):
        if nombre.strip() != "":
            new_id = len(data) + 1
            data.append({"id": new_id, "nombre": nombre, "nivel": nivel, "asistencias": 0, "retardos": 0, "Martes": {"asistencias": 0, "retardos": 0}, "Miércoles": {"asistencias": 0, "retardos": 0}, "Sábado": {"asistencias": 0, "retardos": 0}})
            save_data(data)
            st.success(f"Alumno '{nombre}' registrado con éxito.")
        else:
            st.error("Por favor, ingresa un nombre válido.")


# Consultar Alumno
elif menu == "Consultar Alumno":
    st.title("Consultar Alumno")
    consulta_id = st.number_input("Ingresa el ID del Alumno:", min_value=1, step=1, format="%d")

    if st.button("Buscar", key="consultar_alumno_button"):
        alumno = next((item for item in data if item["id"] == consulta_id), None)
        if alumno:
            st.write(f"**ID:** {alumno['id']}")
            st.write(f"**Nombre:** {alumno['nombre']}")
            st.write(f"**Nivel:** {alumno['nivel']}")
            st.write(f"**Martes Asistencias:** {alumno['Martes']['asistencias']}, Retardos: {alumno['Martes']['retardos']}")
            st.write(f"**Miércoles Asistencias:** {alumno['Miércoles']['asistencias']}, Retardos: {alumno['Miércoles']['retardos']}")
            st.write(f"**Sábado Asistencias:** {alumno['Sábado']['asistencias']}, Retardos: {alumno['Sábado']['retardos']}")
        else:
            st.error("No se encontró ningún alumno con ese ID.")


# Modificar Alumno
elif menu == "Modificar Alumno":
    st.title("Modificar Alumno")
    modificar_id = st.number_input("Ingresa el ID del Alumno a Modificar:", min_value=1, step=1, format="%d")

    alumno = next((item for item in data if item["id"] == modificar_id), None)
    if alumno:
        nuevo_nombre = st.text_input("Nombre del Alumno:", alumno["nombre"])
        nuevo_nivel = st.selectbox("Nivel:", ["Licenciatura", "Bachillerato"], index=["Licenciatura", "Bachillerato"].index(alumno["nivel"]))

        if st.button("Guardar Cambios", key="modificar_alumno_button"):
            alumno["nombre"] = nuevo_nombre
            alumno["nivel"] = nuevo_nivel
            save_data(data)
            st.success("Datos del alumno actualizados correctamente.")
    else:
        st.error("No se encontró ningún alumno con ese ID.")

# Eliminar Alumno
elif menu == "Eliminar Alumno":
    st.title("Eliminar Alumno")
    eliminar_id = st.number_input("Ingresa el ID del Alumno a Eliminar:", min_value=1, step=1, format="%d")

    if st.button("Eliminar", key="eliminar_alumno_button"):
        alumno = next((item for item in data if item["id"] == eliminar_id), None)
        if alumno:
            data.remove(alumno)
            data = reassign_ids(data)
            save_data(data)
            st.success(f"Alumno {alumno['nombre']} eliminado correctamente. ID reasignado.")
        else:
            st.error("No se encontró ningún alumno con ese ID.")

# Mostrar Todos los Registros con una tabla dinámica
elif menu == "Mostrar Todos los Registros":
    st.title("Registros")
    
    if data:
        # Crear una nueva lista con las columnas deseadas, incluyendo los días y sus asistencias/retardos
        formatted_data = [{
            "ID": record["id"], 
            "Nombre": record["nombre"], 
            "Nivel": record["nivel"], 
            "Martes Asistencias": record["Martes"]["asistencias"],
            "Martes Retardos": record["Martes"]["retardos"],
            "Miércoles Asistencias": record["Miércoles"]["asistencias"],
            "Miércoles Retardos": record["Miércoles"]["retardos"],
            "Sábado Asistencias": record["Sábado"]["asistencias"],
            "Sábado Retardos": record["Sábado"]["retardos"]
        } for record in data]

        # Convertir los datos a un DataFrame de Pandas para mejor presentación
        df = pd.DataFrame(formatted_data)

        # Establecer 'ID' como el índice de la tabla para que no se muestre la columna adicional de índice
        df.set_index('ID', inplace=True)

        # Mostrar la tabla en Streamlit como un dataframe interactivo con el ID como índice
        st.dataframe(df, use_container_width=True)  # Tabla sin columna extra de índice