"""Clase Usuario."""

from typing import Any, Dict


class Usuario:
    """Persona registrada en el sistema (identificacion, nombre, correo)."""

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self._validar_datos(identificacion, nombre, correo)
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.correo: str = correo

    @staticmethod
    def _validar_datos(identificacion: str, nombre: str, correo: str) -> None:
        if not identificacion or not str(identificacion).strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or "@" not in correo:
            raise ValueError("El correo del usuario no es válido.")

    def mostrar_informacion(self) -> str:
        return (
            f"Identificación: {self.identificacion} | Nombre: {self.nombre} | "
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Usuario":
        try:
            return cls(
                identificacion=str(datos["identificacion"]),
                nombre=str(datos["nombre"]),
                correo=str(datos["correo"]),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de usuario no contiene la clave requerida: {error}"
            ) from error
