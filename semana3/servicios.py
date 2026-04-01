# Modulo servicios.py
# Contiene todas las funciones de gestion del inventario en memoria.

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
        nombre (str): nombre del producto.
        precio (float): precio unitario del producto.
        cantidad (int): cantidad disponible del producto.
    Retorna:
        str: mensaje indicando si se agrego o ya existia.
    """
    # Verificar si el producto ya existe antes de agregar
    existente = buscar_producto(inventario, nombre)
    if existente is not None:
        return "El producto ya existe. Use la opcion Actualizar para modificarlo."

    producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
    inventario.append(producto)
    return "Producto agregado correctamente."


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario en consola.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
    Retorna:
        None
    """
    if len(inventario) == 0:
        print("El inventario esta vacio.")
        return

    print("")
    print("--- Inventario ---")
    for producto in inventario:
        print("Producto:", producto["nombre"],
              "| Precio:", producto["precio"],
              "| Cantidad:", producto["cantidad"])
    print("------------------")


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre en el inventario.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
        nombre (str): nombre del producto a buscar.
    Retorna:
        dict: el producto encontrado, o None si no existe.
    """
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio o la cantidad de un producto existente.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
        nombre (str): nombre del producto a actualizar.
        nuevo_precio (float, opcional): nuevo precio a asignar.
        nueva_cantidad (int, opcional): nueva cantidad a asignar.
    Retorna:
        str: mensaje indicando el resultado de la operacion.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        return "Producto no encontrado."

    # Actualizar solo los campos que se proporcionaron
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio
    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad

    return "Producto actualizado correctamente."


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
        nombre (str): nombre del producto a eliminar.
    Retorna:
        str: mensaje indicando el resultado de la operacion.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        return "Producto no encontrado."

    inventario.remove(producto)
    return "Producto eliminado correctamente."


def calcular_estadisticas(inventario):
    """
    Calcula estadisticas generales del inventario.
    Parametros:
        inventario (list): lista de diccionarios con los productos.
    Retorna:
        dict: diccionario con unidades_totales, valor_total,
              producto_mas_caro y producto_mayor_stock.
              Retorna None si el inventario esta vacio.
    """
    if len(inventario) == 0:
        return None

    # Funcion lambda para calcular el subtotal de un producto
    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = 0
    valor_total = 0.0

    for producto in inventario:
        unidades_totales = unidades_totales + producto["cantidad"]
        valor_total = valor_total + subtotal(producto)

    # Encontrar el producto mas caro y el de mayor stock
    producto_mas_caro = inventario[0]
    producto_mayor_stock = inventario[0]

    for producto in inventario:
        if producto["precio"] > producto_mas_caro["precio"]:
            producto_mas_caro = producto
        if producto["cantidad"] > producto_mayor_stock["cantidad"]:
            producto_mayor_stock = producto

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }
