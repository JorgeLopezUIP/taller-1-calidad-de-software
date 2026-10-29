from conexion import obtener_conexion


def crear_tabla_estudiantes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS estudiantes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                contrasena VARCHAR(255) NOT NULL
            )
            """
        )
        conexion.commit()
        print("Base de datos creada correctamente")
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    crear_tabla_estudiantes()