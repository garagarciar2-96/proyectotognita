# main.py
import customtkinter as ctk
from actividades.introduccion import ActividadIntroduccion
from actividades.monedas import ActividadMonedas
from actividades.pagar import ActividadPagar 

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AppProyectoTonita(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Toñita - Menú Principal")
        
        ancho = 900
        alto = 700
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = int((ancho_pantalla / 2) - (ancho / 2))
        y = int((alto_pantalla / 2) - (alto / 2))
        
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(True, True) 
        
        self.after(0, lambda: self.state('zoomed'))
        
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True)
        
        self.paginas = {}
        
        self.paginas["Menu"] = MenuInicio(parent=self.contenedor, controlador=self)
        self.paginas["Introduccion"] = ActividadIntroduccion(parent=self.contenedor, controlador=self)
        self.paginas["Monedas"] = ActividadMonedas(parent=self.contenedor, controlador=self)
        self.paginas["Pagar"] = ActividadPagar(parent=self.contenedor, controlador=self)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        self.mostrar_pagina("Menu")

    def mostrar_pagina(self, nombre_pagina):
        for pag in self.paginas.values():
            pag.grid_forget()
            
        pagina = self.paginas[nombre_pagina]
        pagina.grid(row=0, column=0, sticky="nsew")

class MenuInicio(ctk.CTkScrollableFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#F2F4F4")
        
        titulo = ctk.CTkLabel(self, text="¡Bienvenidos!", font=("Arial", 36, "bold"), text_color="#2C3E50")
        titulo.pack(pady=50)
        
        subtitulo = ctk.CTkLabel(self, text="¿Qué actividad vamos a jugar hoy?", font=("Arial", 20))
        subtitulo.pack(pady=10)
        
        btn_intro = ctk.CTkButton(
            self, text="1. Introducción: Contar Gallinas 🐔", font=("Arial", 18),
            width=400, height=55,
            command=lambda: controlador.mostrar_pagina("Introduccion")
        )
        btn_intro.pack(pady=20)
        
        btn_monedas = ctk.CTkButton(
            self, text="2. Monedas y Billetes 🪙💵", font=("Arial", 18),
            width=400, height=55, fg_color="#40C253", hover_color="#12CD60",
            command=lambda: controlador.mostrar_pagina("Monedas")
        )
        btn_monedas.pack(pady=20)
        
        btn_pagar = ctk.CTkButton(
            self, text="3. Tiendita 🛒", font=("Arial", 18),
            width=400, height=55, fg_color="#F39C12", hover_color="#D68910",
            command=lambda: controlador.mostrar_pagina("Pagar")
        )
        btn_pagar.pack(pady=20)

if __name__ == "__main__":
    app = AppProyectoTonita()
    app.mainloop()