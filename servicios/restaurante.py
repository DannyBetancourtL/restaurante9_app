"""Servicio Restaurante: administra productos, usuarios y ventas."""

from typing import Dict, List, Optional, Set

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """Logica de negocio del sistema.

    Las listas (_productos, _usuarios, _ventas) siguen siendo la
    coleccion principal: sirven para listar, recorrer y guardar en
    JSON. Ademas se mantienen unos diccionarios como indices para no
    tener que recorrer esas listas cada vez que se busca algo por una
    clave conocida (codigo de producto, identificacion de usuario).
    """

    def __init__(self, nombre: str = "Restaurante Sabor Lojano") -> None:
        self.nombre: str = nombre

        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

        # indices auxiliares por clave
        self._indice_productos: Dict[str, Producto] = {}
        self._indice_usuarios: Dict[str, Usuario] = {}
        self._ventas_por_usuario: Dict[str, List[Venta]] = {}

        self._contador_producto: int = 0

    # ---------------------- productos ----------------------

    def cargar_productos_iniciales(self, productos: List[Producto]) -> None:
        """Carga los productos leidos desde productos.json al iniciar."""
        for producto in productos:
            self.registrar_producto(producto)
            try:
                numero = int(producto.codigo)
                if numero > self._contador_producto:
                    self._contador_producto = numero
            except ValueError:
                pass  # codigos no numericos no afectan el contador

    def obtener_productos(self) -> List[Producto]:
        return list(self._productos)

    def generar_codigo_producto(self) -> str:
        self._contador_producto += 1
        return str(self._contador_producto)

    def registrar_producto(self, producto: Producto) -> bool:
        """Registra un producto nuevo. False si el codigo ya existe."""
        if producto.codigo in self._indice_productos:
            return False
        self._productos.append(producto)
        self._indice_productos[producto.codigo] = producto
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Busca por codigo usando el indice (evita recorrer la lista)."""
        return self._indice_productos.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: Optional[str] = None,
        categoria: Optional[str] = None,
        precio: Optional[float] = None,
        disponible: Optional[bool] = None,
        stock: Optional[int] = None,
    ) -> bool:
        """Actualiza solo los campos que llegan distintos de None."""
        producto = self._indice_productos.get(codigo)
        if producto is None:
            return False

        nuevo_nombre = nombre if nombre is not None else producto.nombre
        nueva_categoria = categoria if categoria is not None else producto.categoria
        nuevo_precio = precio if precio is not None else producto.precio
        nuevo_stock = stock if stock is not None else producto.stock

        # reutilizo la validacion de Producto para no dejar datos invalidos
        Producto._validar_datos(producto.codigo, nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock)

        producto.nombre = nuevo_nombre
        producto.categoria = nueva_categoria
        producto.precio = nuevo_precio
        producto.stock = nuevo_stock
        if disponible is not None:
            producto.disponible = disponible
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina de la lista y del indice. False si no existe."""
        producto = self._indice_productos.pop(codigo, None)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> List[str]:
        return [producto.mostrar_informacion() for producto in self._productos]

    def obtener_categorias(self) -> Set[str]:
        """Categorias sin repetir, usando set."""
        return {producto.categoria for producto in self._productos}

    # ----------------------- usuarios -----------------------

    def cargar_usuarios_iniciales(self, usuarios: List[Usuario]) -> None:
        """Carga los usuarios leidos desde usuarios.json al iniciar."""
        for usuario in usuarios:
            self.registrar_usuario(usuario)

    def obtener_usuarios(self) -> List[Usuario]:
        return list(self._usuarios)

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un usuario nuevo. False si la identificacion ya existe."""
        if usuario.identificacion in self._indice_usuarios:
            return False
        self._usuarios.append(usuario)
        self._indice_usuarios[usuario.identificacion] = usuario
        return True

    def listar_usuarios(self) -> List[str]:
        return [usuario.mostrar_informacion() for usuario in self._usuarios]

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """Busca por identificacion usando el indice."""
        return self._indice_usuarios.get(identificacion)

    # ------------------------- ventas -------------------------

    def cargar_ventas_iniciales(self, ventas: List[Venta]) -> None:
        """Carga las ventas leidas desde ventas.json al iniciar.

        No se vuelve a descontar stock aqui, porque el stock guardado
        en productos.json ya quedo actualizado con estas ventas.
        """
        for venta in ventas:
            self._registrar_venta_en_colecciones(venta)

    def obtener_ventas(self) -> List[Venta]:
        return list(self._ventas)

    def _registrar_venta_en_colecciones(self, venta: Venta) -> None:
        """Agrega la venta a la lista y al indice por usuario a la vez."""
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """Registra una venta si el usuario, el producto y el stock son validos."""
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._registrar_venta_en_colecciones(venta)
        producto.vender(cantidad)
        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """Ventas de un usuario, usando el indice en vez de recorrer todo."""
        return list(self._ventas_por_usuario.get(identificacion_usuario, []))
