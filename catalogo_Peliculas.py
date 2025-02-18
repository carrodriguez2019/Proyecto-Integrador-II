import csv
import os
import pandas as pd
from prettytable import PrettyTable
from art import *


directorio = 'C:/Users/fernando/Downloads/Python/Proyecto Integrador II'
nombre_archivo = 'Peliculas.csv'
archivo_categorias = 'categorias.csv'
tamanio_pagina = 3


def limpiar_pantalla():
    import os
    import platform
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def mostrar_titulo():
    return print(text2art("Catalogo de Peliculas", font="big"))

class Pelicula:
    def __init__(self,genero,titulo,año,duracion,calificacion,detalles):
        self.genero = genero
        self.titulo = titulo
        self.año = año
        self.duracion = duracion        
        self.calificacion = calificacion
        self.detalles = detalles
    
    def mostrar_informacion(self):
        return f"Título: {self.__titulo}, Año: {self.año}, Duracion: {self.duracion}, Calificacion: {self.calificacion}, Detalles: {self.detalles} "


class GestorCSV: #CatalogoPelicula
    def __init__(self, directorio, nombre_archivo, tamanio_pagina,acategoria):
        self.ruta_archivo = os.path.join(directorio, nombre_archivo)
        self.tamanio_pagina = tamanio_pagina
        self.datos = pd.DataFrame()
        self.datos_categoria = pd.DataFrame()
        self.datos_filtrados = pd.DataFrame(columns=["Genero", "Titulo", "Año", "Duración", "Clasificacion", "Detalles"])
        self.datos_filtrados_categorias = self.datos_categoria.copy()
        self.total_paginas = 0
        self.pagina_actual = 1
        self.ruta_archivo_categoria = os.path.join(directorio, acategoria)

    def cargar_datos(self):
        if os.path.exists(self.ruta_archivo):
            self.datos = pd.read_csv(self.ruta_archivo)
            self.datos_filtrados = self.datos.copy()
            self.total_paginas = (len(self.datos_filtrados) + self.tamanio_pagina - 1) // self.tamanio_pagina
        else:
            print(f"El archivo {self.ruta_archivo} no se encuentra en el directorio especificado.")
    
    def cargar_datos_categorias(self):
        if os.path.exists(self.ruta_archivo_categoria):
            self.datos_categoria = pd.read_csv(self.ruta_archivo_categoria)
            self.datos_filtrados_categorias = self.datos_categoria.copy()            
        else:
            print(f"El archivo {self.ruta_archivo_categoria} no se encuentra en el directorio especificado.") 

    def filtrar_por_genero(self, genero):
        self.datos_filtrados = self.datos[self.datos['Genero'].str.lower() == genero.lower()]
        self.total_paginas = (len(self.datos_filtrados) + self.tamanio_pagina - 1) // self.tamanio_pagina
        self.pagina_actual = 1  # Reiniciar a la primera página después de filtrar

    def mostrar_pagina(self):
        
        inicio = (self.pagina_actual - 1) * self.tamanio_pagina
        fin = inicio + self.tamanio_pagina
        tabla = PrettyTable(self.datos_filtrados.columns.tolist())
        
        for i in range(inicio, fin):
            if i < len(self.datos_filtrados):
                tabla.add_row(self.datos_filtrados.iloc[i].tolist())
            else:
                break
        
        print(tabla)

    def navegar_paginas(self,categoria):
        
        while True:
            limpiar_pantalla()
            mostrar_titulo()
            print(f"\nPágina {self.pagina_actual} de {self.total_paginas}")
            self.mostrar_pagina()
            
            accion = input("Escribe 'siguiente' para avanzar, 'anterior' para retroceder, o 'salir' para terminar: ").strip().lower()
            
            if accion == 'siguiente':
                if self.pagina_actual < self.total_paginas:
                    self.pagina_actual += 1
                else:
                    print("Ya estás en la última página.")
            elif accion == 'anterior':
                if self.pagina_actual > 1:
                    self.pagina_actual -= 1
                else:
                    print("Ya estás en la primera página.")
            elif accion == 'salir':
                limpiar_pantalla()
                mostrar_titulo()  
                print(f"Ha seleccionado la categoría: '{categoria}'") 
                print(f"A continuacion se mostraran las opciones disponibles para realizar en esta categoria") 
                menu_opciones(categoria)
                break
            else:
                print("Comando no reconocido. Por favor, intenta de nuevo.")
            
            
    
           
    def filtrar_por_categoria(self, categoria):       
        self.filtrar_por_genero(categoria)  # Filtrar por género usando el método de pandas
        
    def guardar_peliculas(self):
        self.datos.to_csv(self.ruta_archivo, index=False, encoding='utf-8-sig')
    
    def guardar_categorias(self):
        self.datos_categoria.to_csv(self.ruta_archivo_categoria, index=False, encoding='utf-8-sig')

    def agregar_pelicula(self,pelicula):
        self.cargar_datos()  # Asegurarse de cargar los datos existentes antes de agregar una nueva película
        print (f"{self.datos['Titulo'].str.lower()}")
        print (f"{pelicula.titulo.lower()}")
        if self.datos[self.datos['Titulo'].str.lower() == pelicula.titulo.lower()].empty:
            nueva_pelicula = pd.DataFrame([{
                "Genero": pelicula.genero,
                "Titulo": pelicula.titulo,
                "Año": pelicula.año,
                "Duración": pelicula.duracion,
                "Calificación": pelicula.calificacion,
                "Detalles": pelicula.detalles
            }])
            self.datos = pd.concat([self.datos, nueva_pelicula], ignore_index=True)
            self.guardar_peliculas()
            limpiar_pantalla()
            mostrar_titulo()
            print(f"Película '{pelicula.titulo}' agregada al catálogo.")
        else:
            limpiar_pantalla()
            mostrar_titulo()
            print(f"La película '{pelicula.titulo}' ya existe en el catálogo.")
            
    def eliminar_peliculas_por_categoria(self, categoria):
        self.cargar_datos()  # Asegurarse de cargar los datos existentes
        self.datos = self.datos[self.datos['Genero'].str.lower() != categoria.lower()]
        self.guardar_peliculas()        

    
    def eliminar_categoria(self,categoria):
        self.cargar_datos_categorias()
        self.datos_categoria = self.datos_categoria[self.datos_categoria['Categoria'].str.lower() != categoria.lower()]
        self.guardar_categorias()
        self.eliminar_peliculas_por_categoria(categoria)         
        print(f"La categoría '{categoria}' y las películas relacionadas han sido eliminadas del catálogo.")     
        


def menu_opciones(categoria):
    gestor = GestorCSV(directorio, nombre_archivo, tamanio_pagina,archivo_categorias)
    while True:
        print("\nOpciones:")
        print("1. Agregar Película")
        print("2. Listar Películas")
        print("3. Eliminar Catálogo")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()
            
        if opcion == '1':
            print(f"Acontinuacion los datos para agregar una película a la categoría '{categoria}'.")           
            titulo = input("Título: ")
            año = input("Año: ")
            duracion = input("Duracion: ")
            clasificacion = input("Clasificacion: ")
            detalles = input("Ingrese el enlace de imdb relacionado con la pelicula: ")
            nueva_pelicula = Pelicula(categoria.capitalize(), titulo, año, duracion, clasificacion, detalles)
            gestor.agregar_pelicula(nueva_pelicula)    
                    
        elif opcion == '2':           
            gestor.cargar_datos()
            gestor.filtrar_por_categoria(categoria)
            gestor.navegar_paginas(categoria)           
        elif opcion == '3':            
            gestor.eliminar_categoria(categoria)
            limpiar_pantalla()
            mostrar_titulo()  
            return
        elif opcion == '4':
            return
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 4.")


