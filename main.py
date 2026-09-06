"""Punto de arranque del Sistema de Restaurante (menu por consola)."""

from typing import Callable, Dict, Tuple

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante

# tupla con las opciones del menu, no cambia en tiempo de ejecucion
OPCIONES_MENU: Tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "----------------------------------------",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "----------------------------------------",
    "8. Mostrar categorías",
    "9. Vender producto",
    "10. Consultar ventas por usuario",
    "----------------------------------------",
    "11. Salir",
)

RUTA_PRODUCTOS: str = "datos/productos.json"
RUTA_USUARIOS: str = "datos/usuarios.json"
RUTA_VENTAS: str = "datos/ventas.json"


def sembrar_datos_iniciales(
    restaurante: Restaurante, archivo_servicio: ArchivoServicio
) -> None:
    """Precarga productos y usuarios de ejemplo la primera vez que se corre.

    Solo aplica si aun no existen datos guardados en JSON.
    """
    restaurante.registrar_producto(
        Producto(restaurante.generar_codigo_producto(), "Humitas", "Comida", 1.50, disponible=True, stock=15)
    )
    restaurante.registrar_producto(
        Producto(restaurante.generar_codigo_producto(), "Jugo de tomate", "Bebida", 1.50, disponible=True, stock=20)
    )
    restaurante.registrar_usuario(
        Usuario("1101234567", "Danny Betancourt", "danny@correo.com")
    )
    restaurante.registrar_usuario(
        Usuario("1107654321", "Carlos Pérez", "carlos@correo.com")
    )
    guardar_productos(restaurante, archivo_servicio)
    guardar_usuarios(restaurante, archivo_servicio)
    guardar_ventas(restaurante, archivo_servicio)


def mostrar_encabezado(restaurante: Restaurante) -> None:
    """Imprime el encabezado con el nombre del restaurante."""
    print("=" * 35)
    print(" SISTEMA DE GESTIÓN DE RESTAURANTE ")
    print("=" * 35)
    print(f"Nombre: {restaurante.nombre}")


def mostrar_menu() -> None:
    """Imprime el menu principal del sistema a partir de la tupla de opciones."""
    print("=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    for linea in OPCIONES_MENU:
        print(linea)


def solicitar_float(mensaje: str) -> float:
    """Solicita un numero decimal al usuario validando la entrada."""
    while True:
        valor = input(mensaje).strip()
        try:
            return float(valor)
        except ValueError:
            print("Valor invalido. Ingrese un numero (ej: 4.50).")


def solicitar_entero(mensaje: str) -> int:
    """Solicita un numero entero al usuario validando la entrada."""
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("Valor invalido. Ingrese un numero entero (ej: 10).")


def solicitar_bool(mensaje: str) -> bool:
    """Solicita una respuesta s/n al usuario y la convierte a booleano."""
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("s", "si", "sí"):
            return True
        if valor in ("n", "no"):
            return False
        print("Valor invalido. Responda 's' o 'n'.")


def solicitar_float_opcional(mensaje: str) -> "float | None":
    """Solicita un numero decimal, permitiendo dejarlo vacio (Enter)."""
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        try:
            return float(valor)
        except ValueError:
            print("Valor invalido. Ingrese un numero o deje vacio para no modificar.")


def solicitar_entero_opcional(mensaje: str) -> "int | None":
    """Solicita un numero entero, permitiendo dejarlo vacio (Enter)."""
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        try:
            return int(valor)
        except ValueError:
            print("Valor invalido. Ingrese un numero entero o deje vacio para no modificar.")


def solicitar_bool_opcional(mensaje: str) -> "bool | None":
    """Solicita s/n, permitiendo dejarlo vacio (Enter) para no modificar."""
    while True:
        valor = input(mensaje).strip().lower()
        if valor == "":
            return None
        if valor in ("s", "si", "sí"):
            return True
        if valor in ("n", "no"):
            return False
        print("Valor invalido. Responda 's', 'n' o deje vacio para no modificar.")


def guardar_productos(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Persiste en JSON el estado actual de los productos."""
    archivo_servicio.guardar_productos(restaurante.obtener_productos())


def guardar_usuarios(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Persiste en JSON el estado actual de los usuarios."""
    archivo_servicio.guardar_usuarios(restaurante.obtener_usuarios())


def guardar_ventas(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Persiste en JSON el estado actual de las ventas."""
    archivo_servicio.guardar_ventas(restaurante.obtener_ventas())


def registrar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Pide los datos de un producto y lo registra (el codigo es automatico)."""
    print("\n--- Registrar producto ---")
    nombre: str = input("Nombre: ").strip()
    categoria: str = input("Categoria: ").strip()
    precio: float = solicitar_float("Precio: ")
    disponible: bool = solicitar_bool("Disponible (s/n): ")
    stock: int = solicitar_entero("Stock: ")

    codigo: str = restaurante.generar_codigo_producto()
    try:
        producto = Producto(codigo, nombre, categoria, precio, disponible, stock)
    except ValueError as error:
        print(f"No se pudo registrar el producto: {error}\n")
        return

    restaurante.registrar_producto(producto)
    guardar_productos(restaurante, archivo_servicio)
    print(f"Producto registrado y guardado correctamente con el código '{codigo}'.\n")


def buscar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Solicita un codigo y muestra la informacion del producto encontrado."""
    print("\n--- Buscar producto ---")
    codigo: str = input("Código del producto: ").strip()
    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print(f"No existe un producto con el código '{codigo}'.\n")
        return
    print(producto.mostrar_informacion())
    print()


def actualizar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Solicita un codigo y los nuevos valores (opcionales) de un producto."""
    print("\n--- Actualizar producto ---")
    codigo: str = input("Código del producto a actualizar: ").strip()

    if restaurante.buscar_producto(codigo) is None:
        print(f"No existe un producto con el código '{codigo}'.\n")
        return

    print("Deje el campo vacío (Enter) para no modificarlo.")
    nombre: str = input("Nuevo nombre: ").strip()
    categoria: str = input("Nueva categoría: ").strip()
    precio = solicitar_float_opcional("Nuevo precio: ")
    disponible = solicitar_bool_opcional("Nueva disponibilidad (s/n): ")
    stock = solicitar_entero_opcional("Nuevo stock: ")

    try:
        restaurante.actualizar_producto(
            codigo,
            nombre=nombre or None,
            categoria=categoria or None,
            precio=precio,
            disponible=disponible,
            stock=stock,
        )
    except ValueError as error:
        print(f"No se pudo actualizar el producto: {error}\n")
        return

    guardar_productos(restaurante, archivo_servicio)
    print("Producto actualizado y guardado correctamente.\n")


def eliminar_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Solicita un codigo y elimina el producto correspondiente."""
    print("\n--- Eliminar producto ---")
    codigo: str = input("Código del producto a eliminar: ").strip()
    if restaurante.eliminar_producto(codigo):
        guardar_productos(restaurante, archivo_servicio)
        print("Producto eliminado y archivo actualizado correctamente.\n")
    else:
        print(f"No existe un producto con el código '{codigo}'.\n")


def listar_productos(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Muestra en consola todos los productos registrados."""
    print("\nPRODUCTOS REGISTRADOS")
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.\n")
        return
    for info in productos:
        print(info)
    print()


def registrar_usuario(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Solicita los datos de un usuario y lo registra en el servicio."""
    print("\n--- Registrar usuario ---")
    identificacion: str = input("Identificación: ").strip()
    nombre: str = input("Nombre: ").strip()
    correo: str = input("Correo: ").strip()

    try:
        usuario = Usuario(identificacion, nombre, correo)
    except ValueError as error:
        print(f"No se pudo registrar el usuario: {error}\n")
        return

    if restaurante.registrar_usuario(usuario):
        guardar_usuarios(restaurante, archivo_servicio)
        print("Usuario registrado y guardado correctamente.\n")
    else:
        print(f"Error: ya existe un usuario con la identificación '{identificacion}'.\n")


def listar_usuarios(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Muestra en consola todos los usuarios registrados."""
    print("\nUSUARIOS REGISTRADOS")
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.\n")
        return
    for info in usuarios:
        print(info)
    print()


def mostrar_categorias(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Muestra las categorias unicas de los productos registrados."""
    print("\nCATEGORÍAS REGISTRADAS")
    categorias = restaurante.obtener_categorias()
    if not categorias:
        print("No hay categorías registradas.\n")
        return
    for categoria in sorted(categorias):
        print(f"- {categoria}")
    print()


def vender_producto(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Registra una venta validando usuario, producto, cantidad y stock."""
    print("\n--- Vender producto ---")
    identificacion: str = input("Identificación del usuario: ").strip()
    codigo: str = input("Código del producto: ").strip()
    cantidad: int = solicitar_entero("Cantidad: ")

    if restaurante.buscar_usuario(identificacion) is None:
        print(f"No existe un usuario con la identificación '{identificacion}'.\n")
        return

    producto = restaurante.buscar_producto(codigo)
    if producto is None:
        print(f"No existe un producto con el código '{codigo}'.\n")
        return

    if cantidad <= 0:
        print("La cantidad debe ser mayor a cero.\n")
        return

    if producto.stock < cantidad:
        print(
            f"Stock insuficiente para '{producto.nombre}'. "
            f"Disponible: {producto.stock}, solicitado: {cantidad}.\n"
        )
        return

    if not restaurante.vender_producto(codigo, identificacion, cantidad):
        print("No se pudo registrar la venta. Verifique los datos ingresados.\n")
        return

    guardar_ventas(restaurante, archivo_servicio)
    guardar_productos(restaurante, archivo_servicio)
    print(
        f"Venta registrada correctamente: {cantidad} x '{producto.nombre}'. "
        f"Stock restante: {producto.stock}.\n"
    )


def consultar_ventas_usuario(restaurante: Restaurante, archivo_servicio: ArchivoServicio) -> None:
    """Muestra las ventas realizadas por un usuario en particular."""
    print("\n--- Consultar ventas por usuario ---")
    identificacion: str = input("Identificación del usuario: ").strip()

    if restaurante.buscar_usuario(identificacion) is None:
        print(f"No existe un usuario con la identificación '{identificacion}'.\n")
        return

    ventas = restaurante.consultar_ventas_usuario(identificacion)
    if not ventas:
        print("Este usuario no registra ventas.\n")
        return

    print(f"\nVENTAS DE {identificacion}")
    for venta in ventas:
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto is not None else ""
        print(venta.mostrar_informacion(nombre_producto))
    print()


def main() -> None:
    """Funcion principal que ejecuta el bucle del menu interactivo."""
    restaurante = Restaurante("Restaurante Sabor Lojano")
    archivo_servicio = ArchivoServicio(RUTA_PRODUCTOS, RUTA_USUARIOS, RUTA_VENTAS)

    # cargar lo que haya guardado en JSON (si no existe, arranca vacio)
    productos_guardados = archivo_servicio.cargar_productos()
    restaurante.cargar_productos_iniciales(productos_guardados)

    usuarios_guardados = archivo_servicio.cargar_usuarios()
    restaurante.cargar_usuarios_iniciales(usuarios_guardados)

    ventas_guardadas = archivo_servicio.cargar_ventas()
    restaurante.cargar_ventas_iniciales(ventas_guardadas)

    if not productos_guardados and not usuarios_guardados and not ventas_guardadas:
        sembrar_datos_iniciales(restaurante, archivo_servicio)
        print("Primer arranque detectado: se cargaron datos de ejemplo.\n")

    mostrar_encabezado(restaurante)
    print(
        f"Cargados: {len(restaurante.obtener_productos())} productos, "
        f"{len(restaurante.obtener_usuarios())} usuarios, "
        f"{len(restaurante.obtener_ventas())} ventas.\n"
    )

    # dict que asocia cada opcion del menu con su funcion
    opciones: Dict[str, Callable[[Restaurante, ArchivoServicio], None]] = {
        "1": registrar_producto,
        "2": buscar_producto,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": listar_productos,
        "6": registrar_usuario,
        "7": listar_usuarios,
        "8": mostrar_categorias,
        "9": vender_producto,
        "10": consultar_ventas_usuario,
    }

    while True:
        mostrar_menu()
        opcion: str = input("Seleccione una opcion: ").strip()

        if opcion == "11":
            print("\nGracias por usar el Sistema de Restaurante. ¡Hasta pronto!")
            break

        accion = opciones.get(opcion)
        if accion is None:
            print("\nOpción inválida. Intente nuevamente.\n")
            continue

        try:
            accion(restaurante, archivo_servicio)
        except Exception as error:  # noqa: BLE001 - evita que el programa se detenga
            print(f"\nOcurrió un error inesperado al procesar la opción: {error}\n")


if __name__ == "__main__":
    main()
