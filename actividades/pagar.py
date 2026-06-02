# actividades/pagar.py
import os
import random
import customtkinter as ctk
from PIL import Image

class ActividadPagar(ctk.CTkScrollableFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#FAD7A1") 
        self.controlador = controlador
        
        self.nivel_actual = 1
        self.objetivo = 0
        self.dinero_en_bandeja = {1000: 0, 100: 0, 10: 0, 1: 0} # Lo que el niño va poniendo
        
        ruta_raiz = os.path.dirname(os.path.dirname(__file__))
        ruta_assets = os.path.join(ruta_raiz, "assets")
        
        try:
            self.img_m1 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda1.png")), size=(70, 70))
            self.img_m10 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda10.png")), size=(75, 75))
            self.img_b100 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete100.jpg")), size=(150, 70))
            self.img_b1000 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete1000.png")), size=(150, 70))
            
            self.img_m1_p = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda1.png")), size=(45, 45))
            self.img_m10_p = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda10.png")), size=(50, 50))
            self.img_b100_p = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete100.jpg")), size=(100, 45))
            self.img_b1000_p = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete1000.png")), size=(100, 45))
        except Exception as e:
            print(f"Error al cargar las imágenes de dinero: {e}")
            self.img_m1, self.img_m10, self.img_b100, self.img_b1000 = None, None, None, None
            self.img_m1_p, self.img_m10_p, self.img_b100_p, self.img_b1000_p = None, None, None, None

        self.btn_volver = ctk.CTkButton(
            self, text="⬅ Volver", font=("Arial", 14, "bold"),
            fg_color="#E74C3C", hover_color="#C0392B",
            command=lambda: self.controlador.mostrar_pagina("Menu")
        )
        self.btn_volver.pack(anchor="nw", padx=20, pady=10)
        
        self.lbl_titulo = ctk.CTkLabel(self, text=" La Tiendita 🛒", font=("Arial", 36, "bold"), text_color="#2E4053")
        self.lbl_titulo.pack(pady=5)
        
        self.selector_dificultad = ctk.CTkSegmentedButton(
            self, 
            values=["Nivel 1 ", "Nivel 2 ", "Nivel 3 ", "Nivel 4 "],
            command=self.cambiar_nivel,
            font=("Arial", 16, "bold"),
            selected_color="#D35400",
            selected_hover_color="#A04000"
        )
        self.selector_dificultad.pack(pady=10)
        self.selector_dificultad.set("Nivel 1 ")
        
        self.contenedor_letreros = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_letreros.pack(pady=10)
        
        self.lbl_objetivo = ctk.CTkLabel(self.contenedor_letreros, text="Total: $0", font=("Arial", 32, "bold"), text_color="#C0392B")
        self.lbl_objetivo.grid(row=0, column=0, padx=20)
        
        self.lbl_actual = ctk.CTkLabel(self.contenedor_letreros, text="Llevas: $0", font=("Arial", 32, "bold"), text_color="#27AE60")
        self.lbl_actual.grid(row=0, column=1, padx=20)

        self.lbl_instrucciones = ctk.CTkLabel(self, text="", font=("Arial", 18), text_color="#566573")
        self.lbl_instrucciones.pack(pady=(10,0))
        
        self.cartera = ctk.CTkFrame(self, fg_color="transparent")
        self.cartera.pack(pady=10)
        
        self.botones_cartera = {}
        valores = [1000, 100, 10, 1]
        imagenes_cartera = {1000: self.img_b1000, 100: self.img_b100, 10: self.img_m10, 1: self.img_m1}
        
        for valor in valores:
            btn = ctk.CTkButton(
                self.cartera, text="", image=imagenes_cartera[valor], 
                fg_color="transparent", hover_color="#E5E8E8", width=0,
                command=lambda v=valor: self.agregar_dinero(v)
            )
            self.botones_cartera[valor] = btn

        self.area_bandeja = ctk.CTkFrame(self, fg_color="white", corner_radius=15, height=200)
        self.area_bandeja.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.contenedor_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_botones.pack(pady=10)

        self.btn_pagar = ctk.CTkButton(self.contenedor_botones, text="¡Pagar! ✅", font=("Arial", 20, "bold"), fg_color="#27AE60", hover_color="#1E8449", command=self.revisar_pago)
        self.btn_pagar.grid(row=0, column=0, padx=10)
        
        self.btn_limpiar = ctk.CTkButton(self.contenedor_botones, text="Limpiar Bandeja 🗑️", font=("Arial", 20, "bold"), fg_color="#E74C3C", hover_color="#C0392B", command=self.limpiar_bandeja)
        self.btn_limpiar.grid(row=0, column=1, padx=10)
        
        self.btn_saltar = ctk.CTkButton(self.contenedor_botones, text="Cambiar Reto 🔄", font=("Arial", 20, "bold"), fg_color="#F39C12", hover_color="#D68910", command=self.generar_nuevo_reto)
        self.btn_saltar.grid(row=0, column=2, padx=10)
        
        self.lbl_resultado = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"))
        self.lbl_resultado.pack(pady=5)
        
        self.actualizar_cartera_visible()
        self.generar_nuevo_reto()

    def cambiar_nivel(self, valor_seleccionado):
        if "Nivel 1" in valor_seleccionado: self.nivel_actual = 1
        elif "Nivel 2" in valor_seleccionado: self.nivel_actual = 2
        elif "Nivel 3" in valor_seleccionado: self.nivel_actual = 3
        elif "Nivel 4" in valor_seleccionado: self.nivel_actual = 4
        
        if self.nivel_actual >= 3:
            self.controlador.state('zoomed')
            
        self.actualizar_cartera_visible()
        self.generar_nuevo_reto()

    def actualizar_cartera_visible(self):
        for btn in self.botones_cartera.values():
            btn.grid_forget()
            
        columna = 0
        for valor in [1000, 100, 10, 1]:
            if (valor == 1000 and self.nivel_actual < 4) or \
               (valor == 100 and self.nivel_actual < 3) or \
               (valor == 10 and self.nivel_actual < 2):
                continue
            self.botones_cartera[valor].grid(row=0, column=columna, padx=15)
            columna += 1

    def generar_nuevo_reto(self):
        self.limpiar_bandeja()
        self.lbl_resultado.configure(text="")
        self.btn_pagar.configure(state="normal")
        
        if self.nivel_actual == 1:
            self.objetivo = random.randint(1, 9)
        elif self.nivel_actual == 2:
            self.objetivo = random.randint(10, 99)
        elif self.nivel_actual == 3:
            self.objetivo = random.randint(100, 999)
        elif self.nivel_actual == 4:
            self.objetivo = random.randint(1000, 9999)
            
        self.lbl_objetivo.configure(text=f"Total: ${self.objetivo}")

    def agregar_dinero(self, valor):
        if self.dinero_en_bandeja[valor] < 20:
            self.dinero_en_bandeja[valor] += 1
                        
            denominacion_actual = valor
            
            while denominacion_actual < 1000 and self.dinero_en_bandeja[denominacion_actual] == 10:
                self.dinero_en_bandeja[denominacion_actual] = 0  
                denominacion_actual = denominacion_actual * 10    
                self.dinero_en_bandeja[denominacion_actual] += 1  
                
            self.actualizar_dibujo_bandeja()

    def quitar_dinero(self, valor):
        if self.dinero_en_bandeja[valor] > 0:
            self.dinero_en_bandeja[valor] -= 1
            self.actualizar_dibujo_bandeja()

    def limpiar_bandeja(self):
        self.dinero_en_bandeja = {1000: 0, 100: 0, 10: 0, 1: 0}
        self.actualizar_dibujo_bandeja()

    def actualizar_dibujo_bandeja(self):
        for widget in self.area_bandeja.winfo_children():
            widget.destroy()
            
        total = 0
        imagenes_peques = {
            1000: self.img_b1000_p,
            100: self.img_b100_p,
            10: self.img_m10_p,
            1: self.img_m1_p
        }
        
        valores_ordenados = [1000, 100, 10, 1]
        for valor in valores_ordenados:
            cantidad = self.dinero_en_bandeja[valor]
            total += cantidad * valor
            if cantidad > 0:
                frame_valor = ctk.CTkFrame(self.area_bandeja, fg_color="transparent")
                frame_valor.pack(side="left", expand=True, fill="both", padx=5) 
                
                columnas_maximas = 3 if valor >= 100 else 5
                
                for i in range(cantidad):
                    btn = ctk.CTkButton(
                        frame_valor, image=imagenes_peques[valor], text="",
                        fg_color="transparent", hover_color="#FAD7A1", width=0,
                        command=lambda v=valor: self.quitar_dinero(v)
                    )
                    btn.grid(row=i // columnas_maximas, column=i % columnas_maximas, padx=5, pady=5)
                    
        self.lbl_actual.configure(text=f"Llevas: ${total}")

    def revisar_pago(self):
        total_pagado = sum(valor * cantidad for valor, cantidad in self.dinero_en_bandeja.items())
        
        if total_pagado == self.objetivo:
            self.lbl_resultado.configure(text="¡Pago exacto, mijo! ¡Qué bárbaro! 🌟", text_color="#27AE60")
            self.btn_pagar.configure(state="disabled")
            self.after(2500, self.generar_nuevo_reto)
        elif total_pagado < self.objetivo:
            self.lbl_resultado.configure(text="Uy, te falta dinerito. ¡Síguele echando! 🧐", text_color="#E74C3C")
        else:
            self.lbl_resultado.configure(text="¡Te pasaste de la cuenta! Dale a limpiar y vuelve a intentar. 😅", text_color="#E74C3C")