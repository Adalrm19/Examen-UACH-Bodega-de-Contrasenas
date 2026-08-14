# Jorge Adalberto Ruiz Marquez - 376919

import os
import tkinter as tk
from tkinter import ttk

RUTA_LOGO = "logo.png"
TAMAÑO_MAXIMO_LOGO = 32


def cargar_logo():
    if not os.path.exists(RUTA_LOGO):
        return None
    try:
        imagen = tk.PhotoImage(file=RUTA_LOGO)
    except tk.TclError:
        return None
    factor = max(1, max(imagen.width(), imagen.height()) // TAMAÑO_MAXIMO_LOGO)
    return imagen.subsample(factor, factor) if factor > 1 else imagen


def colocar_logo(ventana):
    logo = cargar_logo()
    if logo:
        ttk.Label(ventana, image=logo).place(relx=1.0, x=-8, y=8, anchor="ne")
    return logo


def colocar_logo_en_barra(barra):
    logo = cargar_logo()
    if logo:
        ttk.Label(barra, image=logo).pack(side="right", padx=(0, 8))
    return logo
