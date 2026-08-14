# Jorge Adalberto Ruiz Marquez - 376919

import tkinter as tk

import base_datos
from tema import aplicar_tema_oscuro
from ventana_login import VentanaLogin
from ventana_principal import VentanaPrincipal


class Aplicacion:
    def __init__(self):
        self._raiz = tk.Tk()
        self._raiz.withdraw()
        aplicar_tema_oscuro(self._raiz)
        self._mostrar_login()

    def _mostrar_login(self):
        VentanaLogin(self._raiz, al_autenticar=self._abrir_baul)

    def _abrir_baul(self, gestor_baul, nombre_usuario):
        VentanaPrincipal(
            self._raiz, gestor_baul, nombre_usuario,
            al_cerrar_sesion=self._mostrar_login,
        )

    def ejecutar(self):
        self._raiz.mainloop()


def main():
    base_datos.inicializar()
    Aplicacion().ejecutar()


if __name__ == "__main__":
    main()
