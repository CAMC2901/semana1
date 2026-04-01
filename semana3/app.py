# Archivo principal app.py
# Punto de entrada del sistema de inventario.
# Integra el menu principal con todas las operaciones disponibles.

from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    calcular_estadisticas
)
from archivos import guardar_csv, cargar_csv

# -----------------------------------------------
# Lista principal del inventario en memoria
# -----------------------------------------------
inventario = []

# -----------------------------------------------
# Funciones auxiliares para solicitar y validar datos
# -----------------------------------------------

def pedir_precio():
    """Solicita un precio valido al usuario. Retorna float."""
    precio_valido = False
    precio = 0.0
    while not precio_valido:
        texto = input("Precio: ")
        try:
            precio = float(texto)
            if precio < 0:
                print("El precio no puede ser negativo.")
            else:
                precio_valido = True
        except ValueError:
            print("Ingrese un numero valido para el precio.")
    return precio

def pedir_cantidad():
    """Solicita una cantidad valida al usuario. Retorna int."""
    cantidad_valida = False
    cantidad = 0
    while not cantidad_valida:
        texto = input("Cantidad: ")
        try:
            cantidad = int(texto)
            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
            else:
                cantidad_valida = True
        except ValueError:
            print("Ingrese un numero entero valido para la cantidad.")
    return cantidad

# -----------------------------------------------
# Funciones de cada opcion del menu
# -----------------------------------------------

def opcion_agregar():
    """Solicita datos al usuario y agrega un producto al inventario."""
    nombre = input("Nombre del producto: ")
    precio = pedir_precio()
    cantidad = pedir_cantidad()
    mensaje = agregar_producto(inventario, nombre, precio, cantidad)
    print(mensaje)

def opcion_mostrar():
    """Muestra todos los productos del inventario."""
    mostrar_inventario(inventario)

def opcion_buscar():
    """Busca un producto por nombre y muestra su informacion."""
    nombre = input("Nombre del producto a buscar: ")
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        print("Producto no encontrado.")
    else:
        print("Producto:", producto["nombre"],
              "| Precio:", producto["precio"],
              "| Cantidad:", producto["cantidad"])

def opcion_actualizar():
    """Actualiza el precio o cantidad de un producto existente."""
    nombre = input("Nombre del producto a actualizar: ")
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        print("Producto no encontrado.")
        return

    print("Deje en blanco si no desea cambiar el campo.")

    # Pedir nuevo precio (opcional)
    texto_precio = input("Nuevo precio (actual " + str(producto["precio"]) + "): ")
    nuevo_precio = None
    if texto_precio.strip() != "":
        try:
            nuevo_precio = float(texto_precio)
            if nuevo_precio < 0:
                print("El precio no puede ser negativo. No se actualizo el precio.")
                nuevo_precio = None
        except ValueError:
            print("Precio invalido. No se actualizo el precio.")

    # Pedir nueva cantidad (opcional)
    texto_cantidad = input("Nueva cantidad (actual " + str(producto["cantidad"]) + "): ")
    nueva_cantidad = None
    if texto_cantidad.strip() != "":
        try:
            nueva_cantidad = int(texto_cantidad)
            if nueva_cantidad < 0:
                print("La cantidad no puede ser negativa. No se actualizo la cantidad.")
                nueva_cantidad = None
        except ValueError:
            print("Cantidad invalida. No se actualizo la cantidad.")

    mensaje = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
    print(mensaje)

def opcion_eliminar():
    """Elimina un producto del inventario por nombre."""
    nombre = input("Nombre del producto a eliminar: ")
    mensaje = eliminar_producto(inventario, nombre)
    print(mensaje)

def opcion_estadisticas():
    """Calcula y muestra las estadisticas del inventario."""
    stats = calcular_estadisticas(inventario)
    if stats is None:
        print("El inventario esta vacio. No hay estadisticas que mostrar.")
        return

    print("")
    print("--- Estadisticas del Inventario ---")
    print("Unidades totales:", stats["unidades_totales"])
    print("Valor total del inventario:", stats["valor_total"])
    print("Producto mas caro:", stats["producto_mas_caro"]["nombre"],
          "| Precio:", stats["producto_mas_caro"]["precio"])
    print("Producto con mayor stock:", stats["producto_mayor_stock"]["nombre"],
          "| Cantidad:", stats["producto_mayor_stock"]["cantidad"])
    print("-----------------------------------")

def opcion_guardar_csv():
    """Solicita una ruta al usuario y guarda el inventario en un archivo CSV."""
    ruta = input("Ingrese la ruta del archivo (ej: inventario.csv): ")
    guardar_csv(inventario, ruta)

def opcion_cargar_csv():
    """Carga productos desde un CSV y permite sobrescribir o fusionar el inventario."""
    ruta = input("Ingrese la ruta del archivo a cargar (ej: inventario.csv): ")
    productos_cargados = cargar_csv(ruta)

    if len(productos_cargados) == 0:
        print("No se cargaron productos.")
        return

    print("Se encontraron " + str(len(productos_cargados)) + " productos en el archivo.")
    decision = input("Sobrescribir inventario actual? (S/N): ")

    if decision.strip().upper() == "S":
        # Reemplazar todo el inventario con los productos cargados
        inventario.clear()
        for p in productos_cargados:
            inventario.append(p)
        print("Accion: reemplazo. Inventario actualizado con " + str(len(productos_cargados)) + " productos.")

    else:
        # Fusion: actualizar existentes o agregar nuevos
        # Politica: si el nombre ya existe, se suma la cantidad y se actualiza el precio al nuevo valor.
        print("Politica de fusion: si el producto ya existe, se suma la cantidad y se actualiza el precio.")
        productos_nuevos = 0
        productos_fusionados = 0

        for p in productos_cargados:
            existente = buscar_producto(inventario, p["nombre"])
            if existente is not None:
                existente["cantidad"] = existente["cantidad"] + p["cantidad"]
                existente["precio"] = p["precio"]
                productos_fusionados = productos_fusionados + 1
            else:
                inventario.append(p)
                productos_nuevos = productos_nuevos + 1

        print("Accion: fusion. Productos nuevos agregados:", productos_nuevos,
              "| Productos actualizados:", productos_fusionados)

# -----------------------------------------------
# Mostrar el menu principal
# -----------------------------------------------
def mostrar_menu():
    print("")
    print("--- Menu de Inventario ---")
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Estadisticas")
    print("7. Guardar CSV")
    print("8. Cargar CSV")
    print("9. Salir")

# -----------------------------------------------
# Bucle principal del programa
# Se ejecuta hasta que el usuario elija la opcion 9
# -----------------------------------------------
mostrar_menu()
opcion = input("Seleccione una opcion (1-9): ")

while opcion != "9":
    try:
        if opcion == "1":
            opcion_agregar()
        elif opcion == "2":
            opcion_mostrar()
        elif opcion == "3":
            opcion_buscar()
        elif opcion == "4":
            opcion_actualizar()
        elif opcion == "5":
            opcion_eliminar()
        elif opcion == "6":
            opcion_estadisticas()
        elif opcion == "7":
            opcion_guardar_csv()
        elif opcion == "8":
            opcion_cargar_csv()
        else:
            print("Opcion invalida. Por favor ingrese un numero entre 1 y 9.")
    except Exception as error:
        print("Ocurrio un error inesperado:", error)

    mostrar_menu()
    opcion = input("Seleccione una opcion (1-9): ")

print("Saliendo del programa. Hasta luego.")

# -----------------------------------------------
# Este programa implementa un sistema completo de gestion de inventario.
# Permite agregar, mostrar, buscar, actualizar y eliminar productos,
# calcular estadisticas del inventario, y guardar o cargar datos en formato CSV.
# El inventario se mantiene en memoria como lista de diccionarios.
# El codigo esta modularizado en tres archivos: app.py, servicios.py y archivos.py.
# -----------------------------------------------
