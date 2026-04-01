# Modulo archivos.py
# Contiene las funciones para guardar y cargar el inventario en formato CSV.

import csv
import os

def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
        ruta (str): ruta del archivo donde se guardara el CSV.
        incluir_header (bool): indica si se escribe el encabezado. Por defecto True.
    Retorna:
        None
    """
    # Validar que el inventario no este vacio antes de guardar
    if len(inventario) == 0:
        print("El inventario esta vacio. No hay datos para guardar.")
        return

    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)

            # Escribir encabezado si corresponde
            if incluir_header:
                escritor.writerow(["nombre", "precio", "cantidad"])

            # Escribir cada producto como una fila
            for producto in inventario:
                escritor.writerow([producto["nombre"], producto["precio"], producto["cantidad"]])

        print("Inventario guardado en:", ruta)

    except Exception as error:
        print("No se pudo guardar el archivo. Error:", error)


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV y los retorna como lista de diccionarios.
    Parametros:
        ruta (str): ruta del archivo CSV a cargar.
    Retorna:
        list: lista de productos validos cargados desde el archivo.
              Retorna lista vacia si ocurre un error grave.
    """
    productos_cargados = []
    filas_invalidas = 0

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            encabezado = next(lector, None)

            # Validar que el encabezado sea el correcto
            if encabezado is None or encabezado != ["nombre", "precio", "cantidad"]:
                print("El archivo no tiene un encabezado valido. Se esperaba: nombre,precio,cantidad")
                return []

            # Procesar cada fila del archivo
            for fila in lector:
                # Validar que la fila tenga exactamente 3 columnas
                if len(fila) != 3:
                    filas_invalidas = filas_invalidas + 1
                    continue

                try:
                    nombre = fila[0].strip()
                    precio = float(fila[1].strip())
                    cantidad = int(fila[2].strip())

                    # Validar que precio y cantidad no sean negativos
                    if precio < 0 or cantidad < 0:
                        filas_invalidas = filas_invalidas + 1
                        continue

                    productos_cargados.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})

                except ValueError:
                    filas_invalidas = filas_invalidas + 1
                    continue

    except FileNotFoundError:
        print("Archivo no encontrado:", ruta)
        return []
    except UnicodeDecodeError:
        print("Error al leer el archivo. Verifique que el archivo este en formato UTF-8.")
        return []
    except Exception as error:
        print("Error inesperado al leer el archivo:", error)
        return []

    # Informar sobre filas invalidas encontradas
    if filas_invalidas > 0:
        print(str(filas_invalidas) + " filas invalidas omitidas.")

    return productos_cargados
