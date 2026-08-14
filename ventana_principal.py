# Jorge Adalberto Ruiz Marquez - 376919

import tkinter as tk
from tkinter import messagebox, ttk

import tema
from gestor_baul import GestorBaul
from logo import colocar_logo, colocar_logo_en_barra
from modelos import Servicio
from ventanas import centrar_ventana

MASCARA = "*" * 10

COLUMNAS_TABLA = (
    ("servicio", "Servicio", 170, "w"),
    ("usuario", "Usuario / Correo", 230, "w"),
    ("fecha_creacion", "Fecha creacion", 120, "center"),
    ("estado", "Estado", 260, "w"),
)


class VentanaPrincipal(tk.Toplevel):
    def __init__(self, raiz: tk.Tk, gestor: GestorBaul, nombre_usuario: str, al_cerrar_sesion):
        super().__init__(raiz)
        self._raiz = raiz
        self._gestor = gestor
        self._al_cerrar_sesion = al_cerrar_sesion
        self._servicios: dict[str, Servicio] = {}

        self.title(f"Baul de Contraseñas - {nombre_usuario}")
        self.geometry("880x520")
        self.minsize(760, 460)
        self.configure(bg=tema.FONDO)
        self.protocol("WM_DELETE_WINDOW", self._raiz.destroy)

        self._construir_barra_botones()
        self._construir_barra_busqueda()
        self._construir_tabla()
        self._construir_panel_detalle()
        self._cargar_servicios()
        centrar_ventana(self)

    def _construir_barra_botones(self):
        barra = ttk.Frame(self, padding=(12, 12, 12, 0))
        barra.pack(fill="x")

        ttk.Button(barra, text="Agregar", command=self._abrir_formulario_agregar).pack(side="left")
        ttk.Button(barra, text="Editar", command=self._abrir_formulario_editar).pack(side="left", padx=6)
        ttk.Button(barra, text="Eliminar", command=self._eliminar_seleccionado).pack(side="left")
        self._logo = colocar_logo_en_barra(barra)
        ttk.Button(barra, text="Cerrar sesion", command=self._cerrar_sesion).pack(side="right")

    def _construir_barra_busqueda(self):
        barra = ttk.Frame(self, padding=(12, 12, 12, 0))
        barra.pack(fill="x")

        ttk.Label(barra, text="Buscar:").pack(side="left")
        self._texto_busqueda = tk.StringVar()
        self._texto_busqueda.trace_add("write", lambda *_: self._refrescar_tabla())
        ttk.Entry(barra, textvariable=self._texto_busqueda).pack(side="left", fill="x", expand=True, padx=(6, 0))

    def _construir_tabla(self):
        nombres_columnas = [columna[0] for columna in COLUMNAS_TABLA]
        self._tabla = ttk.Treeview(self, columns=nombres_columnas, show="headings", selectmode="browse")

        for id_columna, encabezado, ancho, alineacion in COLUMNAS_TABLA:
            self._tabla.heading(id_columna, text=encabezado)
            self._tabla.column(id_columna, width=ancho, anchor=alineacion)

        self._tabla.tag_configure("caducado", background=tema.CADUCADO_FONDO, foreground=tema.CADUCADO_TEXTO)
        self._tabla.pack(fill="both", expand=True, padx=12, pady=12)
        self._tabla.bind("<<TreeviewSelect>>", lambda evento: self._al_cambiar_seleccion())

    def _construir_panel_detalle(self):
        panel = ttk.LabelFrame(self, text="Detalle del servicio seleccionado", padding=12)
        panel.pack(fill="x", padx=12, pady=(0, 12))

        ttk.Label(panel, text="Usuario / Correo:").grid(row=0, column=0, sticky="w")
        self._etiqueta_usuario = ttk.Label(panel, text="-", font=("Consolas", 10))
        self._etiqueta_usuario.grid(row=0, column=1, sticky="w", padx=(6, 24))

        ttk.Label(panel, text="Contraseña:").grid(row=0, column=2, sticky="w")
        self._etiqueta_contraseña = ttk.Label(panel, text="-", font=("Consolas", 10))
        self._etiqueta_contraseña.grid(row=0, column=3, sticky="w", padx=6)

        self._boton_revelar = ttk.Button(panel, text="Revelar", command=self._alternar_revelado, state="disabled")
        self._boton_revelar.grid(row=0, column=4, padx=(24, 0))
        self._contraseña_revelada = False

    def _cargar_servicios(self):
        self._servicios = {servicio.id: servicio for servicio in self._gestor.listar_servicios()}
        self._refrescar_tabla()

    def _refrescar_tabla(self):
        seleccion_previa = self._id_seleccionado()
        self._tabla.delete(*self._tabla.get_children())

        filtro = self._texto_busqueda.get().strip().lower()
        for servicio in self._servicios.values():
            if filtro and filtro not in servicio.nombre_servicio.lower() and filtro not in servicio.usuario.lower():
                continue
            self._insertar_fila(servicio)

        if seleccion_previa and self._tabla.exists(seleccion_previa):
            self._tabla.selection_set(seleccion_previa)
        self._al_cambiar_seleccion()

    def _insertar_fila(self, servicio: Servicio):
        etiquetas = ("caducado",) if servicio.esta_caducado() else ()
        self._tabla.insert(
            "", "end", iid=servicio.id,
            values=(servicio.nombre_servicio, MASCARA, servicio.fecha_creacion, servicio.estado_legible()),
            tags=etiquetas,
        )

    def _id_seleccionado(self) -> str | None:
        seleccion = self._tabla.selection()
        return seleccion[0] if seleccion else None

    def _servicio_seleccionado(self) -> Servicio | None:
        id_ = self._id_seleccionado()
        return self._servicios.get(id_) if id_ else None

    def _al_cambiar_seleccion(self):
        self._contraseña_revelada = False
        self._boton_revelar.configure(text="Revelar")

        if self._servicio_seleccionado() is None:
            self._ocultar_detalle(texto_vacio="-")
            self._boton_revelar.configure(state="disabled")
        else:
            self._ocultar_detalle(texto_vacio=MASCARA)
            self._boton_revelar.configure(state="normal")

    def _alternar_revelado(self):
        servicio = self._servicio_seleccionado()
        if servicio is None:
            return

        self._contraseña_revelada = not self._contraseña_revelada
        if self._contraseña_revelada:
            self._mostrar_detalle(servicio)
            self._boton_revelar.configure(text="Ocultar")
        else:
            self._ocultar_detalle(texto_vacio=MASCARA)
            self._boton_revelar.configure(text="Revelar")

    def _mostrar_detalle(self, servicio: Servicio):
        self._etiqueta_usuario.configure(text=servicio.usuario)
        self._etiqueta_contraseña.configure(text=servicio.contraseña)

    def _ocultar_detalle(self, texto_vacio: str):
        self._etiqueta_usuario.configure(text=texto_vacio)
        self._etiqueta_contraseña.configure(text=texto_vacio)

    def _abrir_formulario_agregar(self):
        VentanaFormularioServicio(self, al_guardar=self._guardar_nuevo_servicio)

    def _abrir_formulario_editar(self):
        servicio = self._servicio_seleccionado()
        if servicio is None:
            messagebox.showwarning("Nada seleccionado", "Selecciona un servicio de la lista para editarlo.")
            return
        VentanaFormularioServicio(self, servicio=servicio, al_guardar=self._guardar_edicion)

    def _guardar_nuevo_servicio(self, servicio: Servicio):
        self._gestor.agregar_servicio(servicio)
        self._cargar_servicios()

    def _guardar_edicion(self, servicio: Servicio):
        self._gestor.editar_servicio(servicio)
        self._cargar_servicios()

    def _eliminar_seleccionado(self):
        servicio = self._servicio_seleccionado()
        if servicio is None:
            messagebox.showwarning("Nada seleccionado", "Selecciona un servicio de la lista para eliminarlo.")
            return
        confirmado = messagebox.askyesno(
            "Confirmar eliminacion",
            f"¿Eliminar el servicio '{servicio.nombre_servicio}'? Esta accion no se puede deshacer.",
        )
        if confirmado:
            self._gestor.eliminar_servicio(servicio.id)
            self._cargar_servicios()

    def _cerrar_sesion(self):
        self.destroy()
        self._al_cerrar_sesion()


class VentanaFormularioServicio(tk.Toplevel):
    def __init__(self, padre: tk.Tk, al_guardar, servicio: Servicio | None = None):
        super().__init__(padre)
        self._al_guardar = al_guardar
        self._servicio = servicio  # None => modo "agregar"; si no, modo "editar"

        self.title("Editar servicio" if servicio else "Agregar servicio")
        self.resizable(False, False)
        self.configure(bg=tema.FONDO)
        self.transient(padre)
        self.grab_set()

        self._construir_campos()
        self._precargar_valores()
        self._construir_boton_guardar()
        self._logo = colocar_logo(self)
        self._entrada_servicio.focus_set()
        centrar_ventana(self)

    def _construir_campos(self):
        contenedor = ttk.Frame(self, padding=20)
        contenedor.grid(row=0, column=0)
        self._contenedor = contenedor

        ttk.Label(contenedor, text="Nombre del servicio:").grid(row=0, column=0, sticky="w", pady=4)
        self._entrada_servicio = ttk.Entry(contenedor, width=32)
        self._entrada_servicio.grid(row=0, column=1, pady=4)

        ttk.Label(contenedor, text="Usuario / Correo:").grid(row=1, column=0, sticky="w", pady=4)
        self._entrada_usuario = ttk.Entry(contenedor, width=32)
        self._entrada_usuario.grid(row=1, column=1, pady=4)

        ttk.Label(contenedor, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=4)
        self._entrada_contraseña = ttk.Entry(contenedor, width=32, show="*")
        self._entrada_contraseña.grid(row=2, column=1, pady=4)

        ttk.Label(contenedor, text="Dias antes de caducar:").grid(row=3, column=0, sticky="w", pady=4)
        self._entrada_dias = ttk.Entry(contenedor, width=32)
        self._entrada_dias.grid(row=3, column=1, pady=4)
        ttk.Label(contenedor, text="(0 = nunca caduca)", font=("Segoe UI", 8)).grid(row=4, column=1, sticky="w")

    def _precargar_valores(self):
        if self._servicio:
            self._entrada_servicio.insert(0, self._servicio.nombre_servicio)
            self._entrada_usuario.insert(0, self._servicio.usuario)
            self._entrada_contraseña.insert(0, self._servicio.contraseña)
            self._entrada_dias.insert(0, str(self._servicio.dias_caducidad))
        else:
            self._entrada_dias.insert(0, "0")

    def _construir_boton_guardar(self):
        ttk.Button(self._contenedor, text="Guardar", command=self._guardar).grid(
            row=5, column=0, columnspan=2, pady=(16, 0), sticky="ew"
        )

    def _guardar(self):
        nombre_servicio = self._entrada_servicio.get().strip()
        usuario = self._entrada_usuario.get().strip()
        contraseña = self._entrada_contraseña.get()
        texto_dias = self._entrada_dias.get().strip()

        if not nombre_servicio or not usuario or not contraseña:
            messagebox.showerror("Datos incompletos", "Completa servicio, usuario y contraseña.", parent=self)
            return
        if not texto_dias.isdigit():
            messagebox.showerror("Dato invalido", "Los dias antes de caducar deben ser un numero entero (0 o mas).", parent=self)
            return

        dias_caducidad = int(texto_dias)
        if self._servicio:
            servicio = self._servicio
            servicio.nombre_servicio = nombre_servicio
            servicio.usuario = usuario
            servicio.contraseña = contraseña
            servicio.dias_caducidad = dias_caducidad
        else:
            servicio = Servicio.nuevo(nombre_servicio, usuario, contraseña, dias_caducidad)

        self._al_guardar(servicio)
        self.destroy()
