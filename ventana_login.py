# Jorge Adalberto Ruiz Marquez - 376919

import tkinter as tk
from tkinter import messagebox, ttk

import base_datos
import tema
from gestor_baul import GestorBaul
from logo import colocar_logo
from ventanas import centrar_ventana

LONGITUD_MINIMA_CONTRASEÑA = 4


class VentanaLogin(tk.Toplevel):
    def __init__(self, raiz: tk.Tk, al_autenticar):
        super().__init__(raiz)
        self._raiz = raiz
        self._al_autenticar = al_autenticar
        self._modo_registro = not base_datos.existe_usuario()

        self.title("Baul de Contraseñas - Iniciar sesion")
        self.resizable(False, False)
        self.configure(bg=tema.FONDO)
        self.protocol("WM_DELETE_WINDOW", self._raiz.destroy)

        self._construir_encabezado()
        self._construir_campos()
        self._construir_boton_ingresar()
        self._logo = colocar_logo(self)
        self.bind("<Return>", lambda evento: self._intentar_autenticar())
        self._entrada_usuario.focus_set()
        centrar_ventana(self)

    def _construir_encabezado(self):
        self._contenedor = ttk.Frame(self, padding=24)
        self._contenedor.grid(row=0, column=0)

        titulo = "Crear contraseña maestra" if self._modo_registro else "Iniciar sesion"
        ttk.Label(self._contenedor, text="Baul de Contraseñas", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 4)
        )
        ttk.Label(self._contenedor, text=titulo, font=("Segoe UI", 10)).grid(
            row=1, column=0, columnspan=2, pady=(0, 16)
        )

    def _construir_campos(self):
        ttk.Label(self._contenedor, text="Nombre de usuario:").grid(row=2, column=0, sticky="w", pady=4)
        self._entrada_usuario = ttk.Entry(self._contenedor, width=28)
        self._entrada_usuario.grid(row=2, column=1, pady=4)

        ttk.Label(self._contenedor, text="Contraseña maestra:").grid(row=3, column=0, sticky="w", pady=4)
        self._entrada_contraseña = ttk.Entry(self._contenedor, width=28, show="*")
        self._entrada_contraseña.grid(row=3, column=1, pady=4)

        self._entrada_confirmar = None
        if self._modo_registro:
            ttk.Label(self._contenedor, text="Confirmar contraseña:").grid(row=4, column=0, sticky="w", pady=4)
            self._entrada_confirmar = ttk.Entry(self._contenedor, width=28, show="*")
            self._entrada_confirmar.grid(row=4, column=1, pady=4)

    def _construir_boton_ingresar(self):
        fila_boton = 5 if self._modo_registro else 4
        texto_boton = "Crear baul" if self._modo_registro else "Ingresar"
        ttk.Button(self._contenedor, text=texto_boton, command=self._intentar_autenticar).grid(
            row=fila_boton, column=0, columnspan=2, pady=(16, 0), sticky="ew"
        )

    def _intentar_autenticar(self):
        nombre_usuario = self._entrada_usuario.get().strip()
        contraseña = self._entrada_contraseña.get()

        if not nombre_usuario or not contraseña:
            messagebox.showerror("Datos incompletos", "Completa el usuario y la contraseña maestra.", parent=self)
            return

        if self._modo_registro:
            self._registrar(nombre_usuario, contraseña)
        else:
            self._iniciar_sesion(nombre_usuario, contraseña)

    def _registrar(self, nombre_usuario: str, contraseña: str):
        confirmacion = self._entrada_confirmar.get()
        if contraseña != confirmacion:
            messagebox.showerror("Las contraseñas no coinciden", "Vuelve a escribir la contraseña maestra.", parent=self)
            return
        if len(contraseña) < LONGITUD_MINIMA_CONTRASEÑA:
            messagebox.showerror(
                "Contraseña muy corta",
                f"Usa al menos {LONGITUD_MINIMA_CONTRASEÑA} caracteres para la contraseña maestra.",
                parent=self,
            )
            return

        base_datos.crear_usuario(nombre_usuario, contraseña)

        messagebox.showinfo("Baul creado", "Tu baul de contraseñas fue creado correctamente.", parent=self)
        self._completar_autenticacion(nombre_usuario)

    def _iniciar_sesion(self, nombre_usuario: str, contraseña: str):
        usuario_guardado = base_datos.obtener_usuario()

        credenciales_validas = (
            usuario_guardado is not None
            and nombre_usuario == usuario_guardado["nombre_usuario"]
            and contraseña == usuario_guardado["contraseña"]
        )

        if not credenciales_validas:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña maestra incorrectos.", parent=self)
            self._entrada_contraseña.delete(0, tk.END)
            return

        self._completar_autenticacion(nombre_usuario)

    def _completar_autenticacion(self, nombre_usuario: str):
        gestor = GestorBaul()
        self.destroy()
        self._al_autenticar(gestor, nombre_usuario)
