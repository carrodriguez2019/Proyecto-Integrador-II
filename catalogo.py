from catalogo_Peliculas import menu_opciones
from art import *
import csv
import os
from prettytable import PrettyTable
import platform
import sys




# Establece directamente la ruta del directorio
directorio = 'C:/Users/fernando/Downloads/Python/Proyecto Integrador II'
# Archivo CSV de categorías
archivo_categorias = 'categorias.csv'
ruta_archivo = os.path.join(directorio, archivo_categorias)

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrarCategoria(self, index):
        return f"{index}. Categoria: {self.nombre}"

class GestorCategorias:
    def __init__(self,ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.categorias =  self.leer_categorias()

    # Leer categorías desde el archivo CSV
    def leer_categorias(self):
        categorias = []
        try:
            with open(self.ruta_archivo, mode='r', newline='', encoding='utf-8-sig') as archivo:
                lector_csv = csv.DictReader(archivo)
                for fila in lector_csv:
                    categorias.append(Categoria(fila['Categoria']))
            return categorias
        except FileNotFoundError:
            print("Error: El archivo CSV no se encontró.")
        except PermissionError:
            print("Error: No tiene permisos para acceder al archivo CSV.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        return []
    
    def agregar_categorias(self,nombre):
        # Verificar si la nueva categoría ya existe
        categoria_existe = any(categoria.nombre.lower() == nombre.lower() for categoria in self.categorias)
        if categoria_existe:         
            limpiar_pantalla()
            mostrar_titulo()                         
            print(f"La categoría ingresada: '{nombre}' ya existe.")
            self.categoria_nueva()        
            
        else:
            try:
                with open(ruta_archivo, mode='a', newline='', encoding='utf-8-sig') as archivo:
                    escritor_csv = csv.writer(archivo, lineterminator='\n')
                    escritor_csv.writerow([nombre])
                self.categorias.append(Categoria(nombre))
                limpiar_pantalla()
                mostrar_titulo()                      
                print(f"La categoría '{nombre}' ha sido añadida al archivo CSV.")
                self.categoria_nueva()    
                    
            except FileNotFoundError:
                print("Error: El archivo CSV no se encontró.")
            except PermissionError:
                print("Error: No tiene permisos para acceder al archivo CSV.")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
        
        
    
    def imprimir_categorias(self):
        # Crear la tabla usando prettytable
        tabla = PrettyTable()
        tabla.field_names = ["Nro", "Categoria"]

        # Llenar la tabla con las categorías enumeradas
        for i, categoria in enumerate(self.categorias, start=1):
            tabla.add_row([i, categoria.nombre])

        # Mostrar la tabla
        print(tabla)
    
        return self.categorias     
    
    def seleccionar_categoria(self):        
        while True:
            numero = input('Por favor seleccione el número de categoría: ').strip()
            if numero.isdigit() and 1 <= int(numero) <= len(self.categorias):
                categoria_seleccionada = self.categorias[int(numero) - 1].nombre                               
                return categoria_seleccionada
            else:
                print('El valor ingresado no es válido. Por favor ingrese un número de categoría válido.') 
                continue
    
    def categoria_nueva(self):        
        gestor = GestorCategorias(ruta_archivo)
        
        while True: 
            gestor.imprimir_categorias()           
            opciones()           
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                nuevo_nombre = input("Ingrese el nombre de la nueva categoría: ")
                self.agregar_categorias(nuevo_nombre)
            elif opcion == '2':
                categoria = self.seleccionar_categoria() 
                limpiar_pantalla()
                mostrar_titulo()     
                print(f"Ha seleccionado la categoría: '{categoria}'") 
                print(f"A continuacion se mostraran las opciones disponibles para realizar en esta categoria")                                      
                menu_opciones(categoria.strip())                                
            elif opcion == '3':
                print("Saliendo del programa. ¡Hasta luego!")
                sys.exit()
            else:
                mostrar_menu()
                print("Opción no válida. Intente de nuevo.")  
                         
 

def limpiar_pantalla():
    
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")


    
def mostrar_titulo():   
    return print(text2art("Catalogo de Peliculas", font="big"))

def opciones():
 
    print("1. Agregar otra categoría")
    print("2. Seleccionar categoría")
    print("3. Salir")       
        

def mostrar_menu():
    limpiar_pantalla()
    mostrar_titulo()
    gestor = GestorCategorias(ruta_archivo)
    gestor.categoria_nueva()
        
def main():
    mostrar_menu()
       
if __name__ == "__main__":
    main()
                                       
                
   

