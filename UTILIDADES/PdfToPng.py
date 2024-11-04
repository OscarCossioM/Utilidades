# Importamos las bibliotecas necesarias
# Primero necesitarás instalar estas bibliotecas usando pip:
# pip install pdf2image tkinter pillow
# También necesitarás instalar poppler-utils:
# En Windows: https://github.com/oschwartz10612/poppler-windows/releases/
# En Linux: sudo apt-get install poppler-utils
# En Mac: brew install poppler

import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import os
from PIL import Image

class ConvertidorPDFaPNG:
    def __init__(self):
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Convertidor PDF a PNG")
        self.ventana.geometry("600x400")
        
        # Variables para almacenar las rutas
        self.carpeta_entrada = tk.StringVar()
        self.carpeta_salida = tk.StringVar()
        self.calidad = tk.IntVar(value=100)  # Valor predeterminado de calidad
        
        # Crear la interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica"""
        # Marco principal con padding
        marco = tk.Frame(self.ventana, padx=20, pady=20)
        marco.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(marco, text="Convertidor de PDF a PNG", font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Sección carpeta de entrada
        frame_entrada = tk.Frame(marco)
        frame_entrada.pack(fill='x', pady=5)
        
        tk.Label(frame_entrada, text="Carpeta de entrada:").pack(side='left')
        tk.Entry(frame_entrada, textvariable=self.carpeta_entrada, width=50).pack(side='left', padx=5)
        tk.Button(frame_entrada, text="Buscar", command=self.seleccionar_entrada).pack(side='left')
        
        # Sección carpeta de salida
        frame_salida = tk.Frame(marco)
        frame_salida.pack(fill='x', pady=5)
        
        tk.Label(frame_salida, text="Carpeta de salida:").pack(side='left')
        tk.Entry(frame_salida, textvariable=self.carpeta_salida, width=50).pack(side='left', padx=5)
        tk.Button(frame_salida, text="Buscar", command=self.seleccionar_salida).pack(side='left')
        
        # Control de calidad
        frame_calidad = tk.Frame(marco)
        frame_calidad.pack(fill='x', pady=10)
        
        tk.Label(frame_calidad, text="Calidad de imagen (1-100):").pack(side='left')
        tk.Scale(frame_calidad, from_=1, to=100, orient='horizontal', 
                variable=self.calidad, length=200).pack(side='left', padx=5)
        
        # Botón de conversión
        tk.Button(marco, text="Convertir PDFs", command=self.convertir_pdfs,
                 bg='#4CAF50', fg='white', pady=10, padx=20).pack(pady=20)
        
        # Instrucciones
        instrucciones = """
        Instrucciones:
        1. Seleccione la carpeta que contiene los archivos PDF
        2. Seleccione la carpeta donde desea guardar las imágenes PNG
        3. Ajuste la calidad de la imagen (mayor número = mejor calidad)
        4. Haga clic en 'Convertir PDFs'
        """
        tk.Label(marco, text=instrucciones, justify='left').pack(pady=10)

    def seleccionar_entrada(self):
        """Abre un diálogo para seleccionar la carpeta de entrada"""
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta con los PDFs")
        if carpeta:
            self.carpeta_entrada.set(carpeta)

    def seleccionar_salida(self):
        """Abre un diálogo para seleccionar la carpeta de salida"""
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta para guardar los PNGs")
        if carpeta:
            self.carpeta_salida.set(carpeta)

    def convertir_pdfs(self):
        """Realiza la conversión de PDF a PNG"""
        # Verificar que se hayan seleccionado las carpetas
        if not self.carpeta_entrada.get() or not self.carpeta_salida.get():
            messagebox.showerror("Error", "Por favor seleccione las carpetas de entrada y salida")
            return

        try:
            # Obtener lista de archivos PDF en la carpeta de entrada
            pdfs = [f for f in os.listdir(self.carpeta_entrada.get()) if f.lower().endswith('.pdf')]
            
            if not pdfs:
                messagebox.showinfo("Información", "No se encontraron archivos PDF en la carpeta seleccionada")
                return

            for pdf in pdfs:
                # Ruta completa del archivo PDF
                pdf_path = os.path.join(self.carpeta_entrada.get(), pdf)
                
                # Convertir PDF a imágenes
                imagenes = convert_from_path(pdf_path)
                
                # Nombre base para los archivos PNG
                nombre_base = os.path.splitext(pdf)[0]
                
                # Guardar cada página como PNG
                for i, imagen in enumerate(imagenes):
                    # Crear nombre del archivo de salida
                    png_path = os.path.join(
                        self.carpeta_salida.get(), 
                        f"{nombre_base}_pagina_{i+1}.png"
                    )
                    
                    # Guardar la imagen con la calidad especificada
                    imagen.save(png_path, "PNG", quality=self.calidad.get())
            
            messagebox.showinfo("Éxito", "¡Conversión completada!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la conversión: {str(e)}")

    def iniciar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    app = ConvertidorPDFaPNG()
    app.iniciar()