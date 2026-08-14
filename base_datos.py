# Jorge Adalberto Ruiz Marquez - 376919

import json
import os

ARCHIVO_BAUL = "vault.json"


def _estructura_vacia() -> dict:
    return {"usuario": None, "servicios": []}


def _leer() -> dict:
    if not os.path.exists(ARCHIVO_BAUL):
        return _estructura_vacia()
    with open(ARCHIVO_BAUL, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def _guardar(datos: dict) -> None:
    with open(ARCHIVO_BAUL, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)


def inicializar() -> None:
    if not os.path.exists(ARCHIVO_BAUL):
        _guardar(_estructura_vacia())


def existe_usuario() -> bool:
    return _leer()["usuario"] is not None


def crear_usuario(nombre_usuario: str, contraseña: str) -> None:
    datos = _leer()
    datos["usuario"] = {"nombre_usuario": nombre_usuario, "contraseña": contraseña}
    _guardar(datos)


def obtener_usuario() -> dict | None:
    return _leer()["usuario"]


def insertar_servicio(fila: dict) -> None:
    datos = _leer()
    datos["servicios"].append(fila)
    _guardar(datos)


def actualizar_servicio(fila: dict) -> None:
    datos = _leer()
    for indice, servicio in enumerate(datos["servicios"]):
        if servicio["id"] == fila["id"]:
            datos["servicios"][indice] = fila
            break
    _guardar(datos)


def eliminar_servicio(id_: str) -> None:
    datos = _leer()
    datos["servicios"] = [s for s in datos["servicios"] if s["id"] != id_]
    _guardar(datos)


def obtener_servicios() -> list[dict]:
    servicios = _leer()["servicios"]
    return sorted(servicios, key=lambda s: s["nombre_servicio"].lower())
