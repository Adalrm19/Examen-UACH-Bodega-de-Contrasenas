# Jorge Adalberto Ruiz Marquez - 376919

from tkinter import ttk

FONDO = "#1e1e2e"
FONDO_PANEL = "#282a3a"
TEXTO = "#e4e4e7"
TEXTO_ATENUADO = "#6b7280"
ACENTO = "#6366f1"
ACENTO_HOVER = "#818cf8"
ENTRADA_FONDO = "#2d2d44"
BORDE = "#3f3f5c"
CADUCADO_FONDO = "#5c1a1a"
CADUCADO_TEXTO = "#fca5a5"


def aplicar_tema_oscuro(raiz):
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")

    raiz.configure(bg=FONDO)

    estilo.configure("TFrame", background=FONDO)
    estilo.configure("TLabelframe", background=FONDO, bordercolor=BORDE)
    estilo.configure("TLabelframe.Label", background=FONDO, foreground=TEXTO)
    estilo.configure("TLabel", background=FONDO, foreground=TEXTO)

    estilo.configure("TButton", background=ENTRADA_FONDO, foreground=TEXTO, bordercolor=BORDE, padding=6)
    estilo.map(
        "TButton",
        background=[("active", ACENTO_HOVER), ("pressed", ACENTO)],
        foreground=[("disabled", TEXTO_ATENUADO)],
    )

    estilo.configure("TEntry", fieldbackground=ENTRADA_FONDO, foreground=TEXTO, insertcolor=TEXTO, bordercolor=BORDE)

    estilo.configure(
        "Treeview", background=FONDO_PANEL, fieldbackground=FONDO_PANEL, foreground=TEXTO,
        bordercolor=BORDE, rowheight=26,
    )
    estilo.map("Treeview", background=[("selected", ACENTO)], foreground=[("selected", TEXTO)])
    estilo.configure("Treeview.Heading", background=ENTRADA_FONDO, foreground=TEXTO, bordercolor=BORDE)
    estilo.map("Treeview.Heading", background=[("active", ACENTO_HOVER)])
