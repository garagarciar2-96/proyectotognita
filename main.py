# main.py
import customtkinter as ctk
# Importamos la actividad desde nuestra carpeta de actividades
from actividades.introduccion import ActividadIntroduccion

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AppProyectoTonita(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Toñita - Menú Principal")
        self.geometry("800x650")
        self.resizable(False, False)
        
        # Contenedor base donde se montan y desmontan las páginas
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True)
        
        # Diccionario para almacenar las "páginas" del proyecto
        self.paginas = {}
        
        # Inicializamos las páginas
        self.paginas["Menu"] = MenuInicio(parent=self.contenedor, controlador=self)
        self.paginas["Introduccion"] = ActividadIntroduccion(parent=self.contenedor, controlador=self)
        
        # Colocamos ambas páginas en el mismo espacio (grid)
        for pag in self.paginas.values():
            pag.grid(row=0, column=0, sticky="nsew")
            
        # Mostramos la página de inicio al arrancar
        self.mostrar_pagina("Menu")

    def mostrar_pagina(self, nombre_pagina):
        # Trae al frente la página solicitada (como cambiar de pestaña)
        pagina = self.paginas[nombre_pagina]
        pagina.tkraise()

class MenuInicio(ctk.CTkFrame):
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
            width=400, height=55, state="disabled", fg_color="#40C253"
        )
        btn_monedas.pack(pady=20)

if __name__ == "__main__":
    app = AppProyectoTonita()
    app.mainloop()