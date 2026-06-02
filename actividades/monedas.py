# actividades/monedas.py
import os
import random
import customtkinter as ctk
from PIL import Image

class ActividadMonedas(ctk.CTkScrollableFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#D5F5E3") 
        self.controlador = controlador
        
        # --- ESTADO DEL JUEGO ---
        self.nivel_actual = 1 # Empezamos en el nivel más facilito
        self.cantidades = {1000: 0, 100: 0, 10: 0, 1: 0} # Aquí guardamos cuánto sale de cada uno
        
        # --- CARGAR IMÁGENES ---
        ruta_raiz = os.path.dirname(os.path.dirname(__file__))
        ruta_assets = os.path.join(ruta_raiz, "assets")
        
        try:
            self.img_moneda1 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda1.png")), size=(1.2*60, 1.2*60))
            self.img_moneda10 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "moneda10.png")), size=(1.2*65, 1.2*65))
            self.img_billete100 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete100.jpg")), size=(1.2*140, 1.2*65))
            self.img_billete1000 = ctk.CTkImage(light_image=Image.open(os.path.join(ruta_assets, "billete1000.png")), size=(1.2*140, 1.2*65))
        except Exception as e:
            print(f"Error al cargar las imágenes de dinero: {e}")
            self.img_moneda1, self.img_moneda10, self.img_billete100, self.img_billete1000 = None, None, None, None

        # --- INTERFAZ GRÁFICA ---
        # Botón Volver
        self.btn_volver = ctk.CTkButton(
            self, text="⬅ Volver al Menú", font=("Arial", 14, "bold"),
            fg_color="#E74C3C", hover_color="#C0392B",
            command=lambda: self.controlador.mostrar_pagina("Menu")
        )
        self.btn_volver.pack(anchor="nw", padx=20, pady=10)
        
        # Título e Instrucciones
        self.lbl_titulo = ctk.CTkLabel(self, text="¿Cuánto dinero hay? 🪙💵", font=("Arial", 36, "bold"), text_color="#2E4053")
        self.lbl_titulo.pack(pady=5)
        
        # --- SELECTOR DE DIFICULTAD ---
        self.selector_dificultad = ctk.CTkSegmentedButton(
            self, 
            values=["Nivel 1 ", "Nivel 2 ", "Nivel 3 ", "Nivel 4 "],
            command=self.cambiar_nivel,
            font=("Arial", 16, "bold"),
            selected_color="#27AE60",
            selected_hover_color="#1E8449"
        )
        self.selector_dificultad.pack(pady=10)
        self.selector_dificultad.set("Nivel 1 ($1)") # Que empiece seleccionado el nivel 1
        
        # Área adaptable donde aparecerán las monedas y billetes
        self.area_dinero = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.area_dinero.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Área de las cajitas (Inputs)
        self.area_cajas = ctk.CTkFrame(self, fg_color="transparent")
        self.area_cajas.pack(pady=10)
        
        # --- CAJITAS DE RESPUESTA (Se ocultan/muestran mágicamente) ---
        self.cajas = {} 
        
        titulos_cajas = {
            1000: "Billetes de $1000\n(Millares)",
            100: "Billetes de $100\n(Centenas)",
            10: "Monedas de $10\n(Decenas)",
            1: "Monedas de $1\n(Unidades)"
        }
        
        for valor, texto in titulos_cajas.items():
            frame = ctk.CTkFrame(self.area_cajas, fg_color="transparent")
            lbl = ctk.CTkLabel(frame, text=texto, font=("Arial", 14, "bold"))
            lbl.pack()
            entrada = ctk.CTkEntry(frame, font=("Arial", 40, "bold"), width=80, justify="center")
            entrada.pack(pady=5)
            self.cajas[valor] = {"frame": frame, "entrada": entrada}

        # --- NUEVOS BOTONES DE ACCIÓN (Revisar y Saltar) ---
        self.contenedor_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_botones.pack(pady=10)

        self.btn_revisar = ctk.CTkButton(self.contenedor_botones, text="¡Revisar! ✅", font=("Arial", 20, "bold"), fg_color="#27AE60", hover_color="#1E8449", command=self.revisar_respuesta)
        self.btn_revisar.grid(row=0, column=0, padx=15)
        
        # Este es el botón nuevo que pediste para evitar frustraciones
        self.btn_saltar = ctk.CTkButton(self.contenedor_botones, text="Cambiar Reto 🔄", font=("Arial", 20, "bold"), fg_color="#F39C12", hover_color="#D68910", command=self.generar_nuevo_reto)
        self.btn_saltar.grid(row=0, column=1, padx=15)
        
        self.lbl_resultado = ctk.CTkLabel(self, text="", font=("Arial", 24, "bold"))
        self.lbl_resultado.pack(pady=5)
        
        # Arrancamos con el primer reto
        self.actualizar_cajas_visibles()
        self.generar_nuevo_reto()

    def cambiar_nivel(self, valor_seleccionado):
        if "Nivel 1" in valor_seleccionado: self.nivel_actual = 1
        elif "Nivel 2" in valor_seleccionado: self.nivel_actual = 2
        elif "Nivel 3" in valor_seleccionado: self.nivel_actual = 3
        elif "Nivel 4" in valor_seleccionado: self.nivel_actual = 4
        
        # Si estamos en nivel 3 o 4, forzamos la pantalla completa para que todo quepa
        if self.nivel_actual >= 3:
            self.controlador.state('zoomed')
            
        self.actualizar_cajas_visibles()
        self.generar_nuevo_reto()

    def actualizar_cajas_visibles(self):
        # Primero ocultamos todas las cajitas
        for datos in self.cajas.values():
            datos["frame"].grid_forget()
            
        # Luego mostramos solo las que tocan en este nivel, de izquierda a derecha
        columna = 0
        valores_ordenados = [1000, 100, 10, 1]
        
        for valor in valores_ordenados:
            # Mostramos $1000 solo en nivel 4; $100 en 3 y 4; $10 en 2, 3 y 4...
            if (valor == 1000 and self.nivel_actual < 4) or \
               (valor == 100 and self.nivel_actual < 3) or \
               (valor == 10 and self.nivel_actual < 2):
                continue
                
            self.cajas[valor]["frame"].grid(row=0, column=columna, padx=15)
            columna += 1

    def limpiar_dinero(self):
        # Limpiamos los contenedores hijos del área de dinero
        for widget in self.area_dinero.winfo_children():
            widget.destroy()

    def generar_nuevo_reto(self):
        self.limpiar_dinero()
        self.lbl_resultado.configure(text="")
        self.btn_revisar.configure(state="normal")
        
        # Limpiamos los textos escritos por el niño
        for datos in self.cajas.values():
            datos["entrada"].delete(0, 'end')
        
        # Generamos cantidades aleatorias según el nivel
        self.cantidades[1] = random.randint(1, 9)
        self.cantidades[10] = random.randint(1, 9) if self.nivel_actual >= 2 else 0
        self.cantidades[100] = random.randint(1, 9) if self.nivel_actual >= 3 else 0
        self.cantidades[1000] = random.randint(1, 9) if self.nivel_actual >= 4 else 0
        
        # Diccionario para relacionar valores con sus imágenes
        imagenes = {
            1000: self.img_billete1000,
            100: self.img_billete100,
            10: self.img_moneda10,
            1: self.img_moneda1
        }

        # Dibujamos todo el dinero de forma adaptativa
        # TRUCO DE ORDEN POSICIONAL: Como la lista va de mayor a menor, al empaquetarlos 
        # a la izquierda (side="left"), quedarán en orden: Millares | Centenas | Decenas | Unidades
        valores_ordenados = [1000, 100, 10, 1]
        for valor in valores_ordenados:
            cantidad = self.cantidades[valor]
            if cantidad > 0:
                frame_valor = ctk.CTkFrame(self.area_dinero, fg_color="transparent")
                # El side="left" hace que se acomoden en horizontal y no empujen los botones abajo
                frame_valor.pack(side="left", expand=True, fill="both", padx=5) 
                
                # Reducimos las columnas para que se apilen más hacia abajo dentro de su propio espacio
                columnas_maximas = 2 if valor >= 100 else 3
                
                for i in range(cantidad):
                    lbl = ctk.CTkLabel(frame_valor, image=imagenes[valor], text="")
                    lbl.grid(row=i // columnas_maximas, column=i % columnas_maximas, padx=5, pady=5)

    def revisar_respuesta(self):
        todo_correcto = True
        
        # Revisamos cada cajita que deba estar visible según el nivel
        valores_ordenados = [1000, 100, 10, 1]
        for valor in valores_ordenados:
            if (valor == 1000 and self.nivel_actual < 4) or \
               (valor == 100 and self.nivel_actual < 3) or \
               (valor == 10 and self.nivel_actual < 2):
                continue
                
            intento_texto = self.cajas[valor]["entrada"].get().strip()
            intento_num = int(intento_texto) if intento_texto.isdigit() else 0
            
            if intento_num != self.cantidades[valor]:
                todo_correcto = False
                break
                
        if todo_correcto:
            self.lbl_resultado.configure(text="¡Excelente, mijo! 🌟", text_color="#27AE60")
            self.btn_revisar.configure(state="disabled")
            self.after(2000, self.generar_nuevo_reto)
        else:
            self.lbl_resultado.configure(text="Uy, vuélvelos a contar despacito 🤔", text_color="#E74C3C")