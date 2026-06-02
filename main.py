# main.py
import customtkinter as ctk
# Importamos la actividad desde nuestra carpeta de actividades
from actividades.introduccion import ActividadIntroduccion
from actividades.monedas import ActividadMonedas

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AppProyectoTonita(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Toñita - Menú Principal")
        
        # Mejoramos el entorno: ventana más amplia y centrada
        ancho = 900
        alto = 700
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho / 2))
        y = int((alto_pantalla / 2) - (alto / 2))
        
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(True, True) # ¡Quitamos el candado para que se estire!
        
        # Hacemos que arranque maximizada (pantalla completa) de forma segura
        self.after(0, lambda: self.state('zoomed'))
        
        # Contenedor base donde se montan y desmontan las páginas
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True)
        
        # Diccionario para almacenar las "páginas" del proyecto
        self.paginas = {}
        
        # Inicializamos las páginas
        self.paginas["Menu"] = MenuInicio(parent=self.contenedor, controlador=self)
        self.paginas["Introduccion"] = ActividadIntroduccion(parent=self.contenedor, controlador=self)
        self.paginas["Monedas"] = ActividadMonedas(parent=self.contenedor, controlador=self)
        
        # Colocamos las páginas en el mismo espacio (grid)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        self.mostrar_pagina("Menu")

    def mostrar_pagina(self, nombre_pagina):
        # TRUCO DE LA ABUELA: Primero escondemos todas las páginas (limpiamos la mesa)
        for pag in self.paginas.values():
            pag.grid_forget()
            
        # Y solo ponemos en la pantalla la página que nos interesa
        pagina = self.paginas[nombre_pagina]
        pagina.grid(row=0, column=0, sticky="nsew")

class MenuInicio(ctk.CTkScrollableFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#F2F4F4")
        
        titulo = ctk.CTkLabel(self, text="¡Bienvenidos!", font=("Arial", 36, "bold"), text_color="#2C3E50")
        titulo.pack(pady=50)
        
        subtitulo = ctk.CTkLabel(self, text="¿Qué actividad vamos a jugar hoy?", font=("Arial", 20))
        subtitulo.pack(pady=10)
        
        # Botón 1: Introducción (Las gallinas)
        btn_intro = ctk.CTkButton(
            self, text="1. Introducción: Contar Gallinas 🐔", font=("Arial", 18),
            width=400, height=55,
            command=lambda: controlador.mostrar_pagina("Introduccion")
        )
        btn_intro.pack(pady=20)
        
        # Botón 2: Monedas y Billetes (Próximamente)
        btn_monedas = ctk.CTkButton(
            self, text="2. Monedas y Billetes de México 🪙💵", font=("Arial", 18),
            width=400, height=55, fg_color="#40C253", hover_color="#27AE60",
            command=lambda: controlador.mostrar_pagina("Monedas")
        )
        btn_monedas.pack(pady=20)

if __name__ == "__main__":
    app = AppProyectoTonita()
    app.mainloop()