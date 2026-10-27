from conexion import *

conexion = obtener_conexion()
cursor = conexion.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS estudiantes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL
)""")

conexion.commit()
cursor.close()
conexion.close()

print("Base de datos creada correctamente")