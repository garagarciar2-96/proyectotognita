# actividades/introduccion.py
import os
import customtkinter as ctk
from PIL import Image

# Nota que ahora heredamos de ctk.CTkFrame, no de ctk.CTk
class ActividadIntroduccion(ctk.CTkScrollableFrame):
    def __init__(self, parent, controlador):
        # Inicializamos el Frame pegándolo al contenedor principal
        super().__init__(parent, fg_color="#EDBB99")
        self.controlador = controlador
        
        # --- CONTROL DE ESTADO ---
        self.contador = 0
        self.max_gallinas = 20
        self.en_animacion = False
        
        # --- CARGAR IMÁGENES ---
        # Buscamos la carpeta assets subiendo un nivel desde la carpeta 'actividades'
        ruta_raiz = os.path.dirname(os.path.dirname(__file__))
        ruta_assets = os.path.join(ruta_raiz, "assets")
        ruta_gallina = os.path.join(ruta_assets, "gallina.png")
        
        try:
            self.img_gallina_normal = ctk.CTkImage(light_image=Image.open(ruta_gallina), size=(90, 90))
            self.img_gallina_peque = ctk.CTkImage(light_image=Image.open(ruta_gallina), size=(40, 40))
        except Exception as e:
            print(f"Error al cargar las imágenes en la actividad: {e}")
            self.img_gallina_normal = None
            self.img_gallina_peque = None

        # --- INTERFAZ GRÁFICA (UI) ---
        
        # Botón Volver al Menú (Arriba a la izquierda)
        self.btn_volver = ctk.CTkButton(
            self, text="⬅ Volver al Menú", font=("Arial", 14, "bold"),
            fg_color="#E74C3C", hover_color="#C0392B",
            command=lambda: self.controlador.mostrar_pagina("Menu")
        )
        self.btn_volver.pack(anchor="nw", padx=20, pady=20)
        
        # Contenedor para el Número Grande
        self.contenedor_numero = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_numero.pack(pady=10)
        
        self.lbl_digito_izq = ctk.CTkLabel(self.contenedor_numero, text="", font=("Arial", 120, "bold"))
        self.lbl_digito_izq.grid(row=0, column=0)
        
        self.lbl_digito_der = ctk.CTkLabel(self.contenedor_numero, text="0", font=("Arial", 120, "bold"), text_color="#E74C3C")
        self.lbl_digito_der.grid(row=0, column=1)
        
        # Área de la Granja Principal
        self.granja = ctk.CTkFrame(self, width=700, height=320, fg_color="#EDBB99", corner_radius=15)
        self.granja.pack(pady=10)
        self.granja.grid_propagate(False)
        
        # Sub-contenedores (Mitad Izquierda y Derecha)
        self.lado_izquierdo = ctk.CTkFrame(self.granja, width=330, height=300, fg_color="transparent")
        self.lado_izquierdo.place(x=10, y=10)
        self.lado_izquierdo.grid_propagate(False)
        
        self.lado_derecho = ctk.CTkFrame(self.granja, width=330, height=300, fg_color="transparent")
        self.lado_derecho.place(x=360, y=10)
        self.lado_derecho.grid_propagate(False)
        
        # Las Cercas
        self.cerca_izq = self.crear_cerca(self.lado_izquierdo)
        self.cerca_der = self.crear_cerca(self.lado_derecho)
        
        self.interior_cerca_izq = ctk.CTkFrame(self.cerca_izq, width=240, height=240, fg_color="#EDBB99")
        self.interior_cerca_izq.pack(padx=4, pady=4)
        self.interior_cerca_izq.grid_propagate(False)
        
        self.interior_cerca_der = ctk.CTkFrame(self.cerca_der, width=240, height=240, fg_color="#EDBB99")
        self.interior_cerca_der.pack(padx=4, pady=4)
        self.interior_cerca_der.grid_propagate(False)

        self.gallinas_en_pantalla = []
        
        # Panel de Navegación
        self.panel_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.panel_botones.pack(side="bottom", pady=20)
        
        self.btn_izq = ctk.CTkButton(self.panel_botones, text="⬅ Anterior", font=("Arial", 18, "bold"), command=self.decrementar)
        self.btn_izq.grid(row=0, column=0, padx=20)
        
        self.btn_der = ctk.CTkButton(self.panel_botones, text="Siguiente ➡", font=("Arial", 18, "bold"), command=self.incrementar)
        self.btn_der.grid(row=0, column=1, padx=20)
        
        self.actualizar_interfaz()

    def crear_cerca(self, parent):
        return ctk.CTkFrame(parent, width=260, height=260, fg_color="#D35400", border_color="#5C3A21", border_width=6, corner_radius=10)

    def incrementar(self):
        if self.contador < self.max_gallinas and not self.en_animacion:
            self.contador += 1
            if self.contador == 10:
                self.disparar_animacion_diez()
            elif self.contador == 20:
                self.disparar_animacion_veinte()
            else:
                self.actualizar_interfaz()
            
    def decrementar(self):
        if self.contador > 0 and not self.en_animacion:
            self.contador -= 1
            self.actualizar_interfaz()
            
    def limpiar_pantalla(self):
        for gallina in self.gallinas_en_pantalla:
            gallina.destroy()
        self.gallinas_en_pantalla.clear()
        self.cerca_izq.place_forget()
        self.cerca_der.place_forget()
        
    def actualizar_interfaz(self):
        self.limpiar_pantalla()
        
        if self.contador < 10:
            self.lbl_digito_izq.configure(text="")
            self.lbl_digito_der.configure(text=str(self.contador), text_color="#E74C3C")
            
            for i in range(self.contador):
                fila, columna = i // 5, i % 5
                lbl = ctk.CTkLabel(self.granja, image=self.img_gallina_normal, text="" if self.img_gallina_normal else "🐔")
                if not self.img_gallina_normal: lbl.configure(font=("Arial", 30))
                lbl.grid(row=fila, column=columna, padx=20, pady=25)
                self.gallinas_en_pantalla.append(lbl)
                
        elif 10 <= self.contador < 20:
            unidades = self.contador - 10
            self.lbl_digito_izq.configure(text="1", text_color="#1F6AA5")
            self.lbl_digito_der.configure(text=str(unidades), text_color="#E74C3C")
            
            self.cerca_izq.place(x=35, y=10)
            for i in range(10):
                fila, columna = i // 4, i % 4
                lbl = ctk.CTkLabel(self.interior_cerca_izq, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
                lbl.grid(row=fila, column=columna, padx=8, pady=12)
                self.gallinas_en_pantalla.append(lbl)
                
            for i in range(unidades):
                fila, columna = i // 4, i % 4
                lbl = ctk.CTkLabel(self.lado_derecho, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
                lbl.grid(row=fila, column=columna, padx=12, pady=15)
                self.gallinas_en_pantalla.append(lbl)

        self.ajustar_botones()

    
    def disparar_animacion_diez(self):
        self.en_animacion = True
        self.ajustar_botones()
        self.lbl_digito_izq.configure(text="1", text_color="#E74C3C")
        self.lbl_digito_der.configure(text="0", text_color="#E74C3C")
        
        # Paso 1: Aparece la gallina 10 en tamaño normal para completar el grupo
        self.limpiar_pantalla()
        for i in range(10):
            fila, columna = i // 5, i % 5
            lbl = ctk.CTkLabel(self.granja, image=self.img_gallina_normal, text="" if self.img_gallina_normal else "🐔")
            if not self.img_gallina_normal: lbl.configure(font=("Arial", 30))
            lbl.grid(row=fila, column=columna, padx=20, pady=25)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_diez_paso_1_5)

    def animacion_diez_paso_1_5(self):
        # Paso 2: Se encogen en su mismo lugar
        self.limpiar_pantalla()
        for i in range(10):
            fila, columna = i // 5, i % 5
            lbl = ctk.CTkLabel(self.granja, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=20, pady=25)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_diez_paso_2)

    def animacion_diez_paso_2(self):
        # Paso 3: Se acomodan en grupo del lado izquierdo (AÚN SIN CERCA)
        self.limpiar_pantalla()
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.lado_izquierdo, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=12, pady=15)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_diez_paso_2_5)

    def animacion_diez_paso_2_5(self):
        # Paso 4: ¡Magia! Aparece la cerca alrededor de ellas
        self.limpiar_pantalla()
        self.cerca_izq.place(x=35, y=10)
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.interior_cerca_izq, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=8, pady=12)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_diez_paso_3)

    def animacion_diez_paso_3(self):
        # Paso 5: Los números cambian de color indicando que ya está lista la decena
        self.lbl_digito_izq.configure(text="1", text_color="#1F6AA5")
        self.lbl_digito_der.configure(text="0", text_color="#2ECC71")
        self.en_animacion = False
        self.ajustar_botones()

    def disparar_animacion_veinte(self):
        self.en_animacion = True
        self.ajustar_botones()
        self.lbl_digito_izq.configure(text="2", text_color="#E74C3C")
        self.lbl_digito_der.configure(text="0", text_color="#E74C3C")
        
        # Paso 1: Aparece la gallina 20 (la décima del lado derecho) formando el grupo, SIN cerca derecha.
        self.limpiar_pantalla()
        self.cerca_izq.place(x=35, y=10) # La cerca izquierda ya existe y se queda ahí
        
        # Redibujamos las 10 gallinas de la cerca izquierda
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.interior_cerca_izq, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=8, pady=12)
            self.gallinas_en_pantalla.append(lbl)
            
        # Dibujamos las 10 gallinas chiquitas sueltas en el lado derecho
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.lado_derecho, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=12, pady=15)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_veinte_paso_2)

    def animacion_veinte_paso_2(self):
        # Paso 2: ¡Magia! Les cae la cerca del lado derecho a las nuevas gallinas
        self.limpiar_pantalla()
        self.cerca_izq.place(x=35, y=10)
        self.cerca_der.place(x=35, y=10) # ¡Ahora sí aparece la cerca derecha!
        
        # Las 10 de la izquierda en su cerca
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.interior_cerca_izq, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=8, pady=12)
            self.gallinas_en_pantalla.append(lbl)
            
        # Las 10 de la derecha ya adentro de su cerca
        for i in range(10):
            fila, columna = i // 4, i % 4
            lbl = ctk.CTkLabel(self.interior_cerca_der, image=self.img_gallina_peque, text="" if self.img_gallina_peque else "🐔")
            if not self.img_gallina_peque: lbl.configure(font=("Arial", 15))
            lbl.grid(row=fila, column=columna, padx=8, pady=12)
            self.gallinas_en_pantalla.append(lbl)
            
        self.after(300, self.animacion_veinte_paso_3)

    def animacion_veinte_paso_3(self):
        # Paso 3: Cambio de color en los números indicando que terminamos la segunda decena
        self.lbl_digito_izq.configure(text="2", text_color="#1F6AA5")
        self.lbl_digito_der.configure(text="0", text_color="#2ECC71")
        self.en_animacion = False
        self.ajustar_botones()

    def ajustar_botones(self):
        if self.en_animacion:
            self.btn_izq.configure(state="disabled", fg_color="#BDC3C7")
            self.btn_der.configure(state="disabled", fg_color="#BDC3C7")
            return
        self.btn_izq.configure(state="disabled" if self.contador == 0 else "normal", fg_color="#BDC3C7" if self.contador == 0 else ["#3B8ED0", "#1F6AA5"])
        self.btn_der.configure(state="disabled" if self.contador == self.max_gallinas else "normal", fg_color="#BDC3C7" if self.contador == self.max_gallinas else ["#3B8ED0", "#1F6AA5"])