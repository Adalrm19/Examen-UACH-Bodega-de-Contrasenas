# Jorge Adalberto Ruiz Marquez - 376919

import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass
class Servicio:
    id: str
    nombre_servicio: str
    usuario: str
    contraseña: str
    fecha_creacion: str
    dias_caducidad: int = 0  # 0 = nunca caduca

    @staticmethod
    def nuevo(nombre_servicio: str, usuario: str, contraseña: str, dias_caducidad: int = 0) -> "Servicio":
        return Servicio(
            id=str(uuid.uuid4()),
            nombre_servicio=nombre_servicio,
            usuario=usuario,
            contraseña=contraseña,
            fecha_creacion=date.today().isoformat(),
            dias_caducidad=dias_caducidad,
        )

    def fecha_de_caducidad(self) -> date | None:
        if self.dias_caducidad <= 0:
            return None
        fecha_creacion = datetime.strptime(self.fecha_creacion, "%Y-%m-%d").date()
        return fecha_creacion + timedelta(days=self.dias_caducidad)

    def esta_caducado(self) -> bool:
        fecha_limite = self.fecha_de_caducidad()
        if fecha_limite is None:
            return False
        return date.today() > fecha_limite

    def estado_legible(self) -> str:
        if self.dias_caducidad <= 0:
            return "Nunca caduca"
        if self.esta_caducado():
            return "Contraseña caducada"
        dias_restantes = (self.fecha_de_caducidad() - date.today()).days
        return f"Vigente ({dias_restantes} dias restantes)"
