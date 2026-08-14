# Jorge Adalberto Ruiz Marquez - 376919

import base_datos
from modelos import Servicio


class GestorBaul:
    def listar_servicios(self) -> list[Servicio]:
        return [self._a_servicio(fila) for fila in base_datos.obtener_servicios()]

    def agregar_servicio(self, servicio: Servicio) -> None:
        base_datos.insertar_servicio(self._a_fila(servicio))

    def editar_servicio(self, servicio: Servicio) -> None:
        base_datos.actualizar_servicio(self._a_fila(servicio))

    def eliminar_servicio(self, id_servicio: str) -> None:
        base_datos.eliminar_servicio(id_servicio)

    def _a_fila(self, servicio: Servicio) -> dict:
        return {
            "id": servicio.id,
            "nombre_servicio": servicio.nombre_servicio,
            "usuario": servicio.usuario,
            "contraseña": servicio.contraseña,
            "fecha_creacion": servicio.fecha_creacion,
            "dias_caducidad": servicio.dias_caducidad,
        }

    def _a_servicio(self, fila: dict) -> Servicio:
        return Servicio(
            id=fila["id"],
            nombre_servicio=fila["nombre_servicio"],
            usuario=fila["usuario"],
            contraseña=fila["contraseña"],
            fecha_creacion=fila["fecha_creacion"],
            dias_caducidad=fila["dias_caducidad"],
        )
