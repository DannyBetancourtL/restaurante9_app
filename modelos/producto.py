"""Clase Producto."""

from typing import Any, Dict


class Producto:
    """Producto del restaurante. El codigo lo asigna Restaurante."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        disponible: bool = True,
        stock: int = 0,
    ) -> None:
        self._validar_datos(codigo, nombre, categoria, precio, stock)
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.categoria: str = categoria
        self.precio: float = precio
        self.disponible: bool = disponible
        self.stock: int = stock

    @staticmethod
    def _validar_datos(
        codigo: str, nombre: str, categoria: str, precio: float, stock: int
    ) -> None:
        """Lanza ValueError si algun dato no es valido."""
        if not codigo or not str(codigo).strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio del producto debe ser un número mayor o igual a cero.")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock del producto debe ser un número entero mayor o igual a cero.")

    def vender(self, cantidad: int) -> None:
        """Descuenta stock. La validacion de cantidad/stock la hace Restaurante,
        pero aqui tambien se comprueba por seguridad."""
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self.stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self.stock -= cantidad

    def mostrar_informacion(self) -> str:
        return (
            f"Código: {self.codigo} | Producto: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: ${self.precio:.2f} | "
            f"Disponible: {self.disponible} | Stock: {self.stock}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a diccionario para guardarlo en JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible,
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Producto":
        """Reconstruye un Producto a partir de un registro leido de JSON."""
        try:
            return cls(
                codigo=str(datos["codigo"]),
                nombre=str(datos["nombre"]),
                categoria=str(datos["categoria"]),
                precio=float(datos["precio"]),
                disponible=bool(datos["disponible"]),
                stock=int(datos["stock"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de producto no contiene la clave requerida: {error}"
            ) from error
