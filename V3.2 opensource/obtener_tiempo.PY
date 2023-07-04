"""
Codigo para obtener referencias de los links generados

Instagram:  @Agus_teira 
Twitter:    @g_teira3
Github:     https://github.com/agusteira

04/07/2023
"""

import time
import os
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

cant_abrir_a_la_vez = 5 # Cantidad de pestañas que abrimos a la vez

pathCSVimportado = fr""             #Ruta del CSV donde generamos los links (a modificar)
pathCSVexportado = fr""             #ruta del CSV nuevo con las referencias (a modificar)
fila_sin_id = ""                    #Fila sin id (a modificar)

def obtener_links(lista_paginas:list, fila_sin_id:str, cant_abrir_a_la_vez:int)->list:
    """
    Esta funcion basicamente te abre las pestañas que generaste en el archivo anterior
    y les busca las referencias para poder saber a cuanto tiempo estas de entrar
    y despues te exporta el mismo csv que antes, pero con las referencias cargadas.
    Tambien imprime por consola la referencia, y el id del link

    Recibe: 
            -La lista de paginas del CSV con sus caracteristicas
            -La fila sin ID
            -Cantidad de veces que queres abrir x ventana
    Devuelve:
            -Un CSV igual que el importado, pero con las referencias de tiempo
            de cada link generado
    """
    numero_de_ventanita=0

    while len(lista_paginas) >= (numero_de_ventanita +cant_abrir_a_la_vez):
        lista_paginas_nuevas = []
        browser = webdriver.Chrome()

        for i in range((cant_abrir_a_la_vez-1)):
            browser.execute_script("window.open('about:blank','_blank');")
        handles = browser.window_handles

        for handle in handles: #Recorre las pestañas
            numero_de_ventanita += 1
            browser.switch_to.window(handle)
            try:
                browser.get(lista_paginas[numero_de_ventanita]['ID FILA']) 
            except:
                pass
            time.sleep(1)

        numero_de_ventanita=numero_de_ventanita - cant_abrir_a_la_vez
        
        for i, handle in enumerate(handles, start=1):
            pagina = {}
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            pagina ["hora"] = hora_actual
            pagina ["NUMERO DE VENTANA"] = numero_de_ventanita
            numero_de_ventanita += 1
            
            #------------------LO IMPORTANTE------------------------------------------------------------------------
            try:
                id_fila = browser.find_element(By.ID, 'hlLinkToQueueTicket2')       #Agarra el ID de fila
                pagina ["ID FILA"] = fila_sin_id + id_fila.text
                idddddd = fila_sin_id + id_fila.text                                #Esta variable la uso para despues mostrarla con el print
                pagina ["ID"] = id_fila.text

                try:
                    span = browser.find_element(By.ID, 'MainPart_lbWhichIsIn') #Esto te agarra los minutos, podes modificar a la referencia que deseas agarrar
                    width_value = span.text
                    pagina ["REFERENCIA"] = width_value

                except Exception as e:                  #Por si la REFERENCIA no carga
                    pagina ["REFERENCIA"] = None
                
            except:                                     #Por si la ID no carga
                pagina ["ID"] = None
                pagina ["ID FILA"] = None
            #----------DATOS-------------------
            try:
                lista_paginas_nuevas.append(pagina)
                browser.switch_to.window(handle)
                print(f"{numero_de_ventanita}    ID: {idddddd}       estado: {width_value}") #Para ir viendo por consola como va la cosa
            except:
                pass

        generar_csv(lista_paginas_nuevas, pathCSVexportado)

def generar_csv(lista:list, nombre_archivo:str):
    """
    A partir de una lista, y un nombre, crea un archivo 
    CSV con los datos de la lista con el nombre pasado
    Recibe: una lista con datos de personajes
    devuele: Crea un archivo CSV segun lo pasado
    """
    if len (lista)>0:
        modo_archivo = "a" if os.path.exists(nombre_archivo) else "w"

        with open(nombre_archivo , modo_archivo) as archivo:

            for e_caracteristica in lista:
                mensaje = "{0},{1},{2},{3},{4},{5}\n"
                try:
                    mensaje = mensaje.format(
                        e_caracteristica["NUMERO DE VENTANA"],
                        e_caracteristica["ID FILA"],
                        e_caracteristica["ID"],
                        e_caracteristica["hora"],
                        "",
                        e_caracteristica["REFERENCIA"]
                        )
                except:
                    pass
                try:
                    mensaje = mensaje.format(
                    e_caracteristica["NUMERO DE VENTANA"],
                    e_caracteristica["ID FILA"],
                    e_caracteristica["ID"],
                    e_caracteristica["hora"],
                    "",
                    "n/a"
                    )
                except:
                    pass
                try:
                    mensaje = mensaje.format(
                    e_caracteristica["NUMERO DE VENTANA"],
                    "n/a",
                    "",
                    e_caracteristica["hora"],
                    "",
                    "n/a"
                    )
                except:
                    pass
                
                archivo.write(mensaje)
    else:
        return -1

def leer_csv(nombre_archivo):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios con los datos.
    Recibe: nombre del archivo CSV.
    Devuelve: una lista de diccionarios con los datos del archivo.
    """
    lista = []
    with open(nombre_archivo, 'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            nuevo_diccionario = {}        
            for clave, valor in fila.items():
                nuevo_diccionario[clave] = valor
            lista.append(nuevo_diccionario)
    return lista

def ordenar_csv_por_REFERENCIA(nombre_archivo):
    # Leer el archivo CSV y cargar los datos en una lista de diccionarios
    with open(nombre_archivo, 'r', newline='') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        datos = list(lector)

    # Ordenar la lista de diccionarios por el valor de la clave "REFERENCIA"
    datos_ordenados = sorted(datos, key=lambda x: x['REFERENCIA'] if x['REFERENCIA'] is not None else 'ZZZZ', reverse=True) #Si no funciona, agregarle el int

    # Escribir los datos ordenados en un nuevo archivo CSV
    nombre_archivo_ordenado = nombre_archivo.split('.')[0] + '_ordenado.csv'
    with open(nombre_archivo_ordenado, 'w', newline='') as archivo_csv_ordenado:
        escritor = csv.DictWriter(archivo_csv_ordenado, fieldnames=lector.fieldnames)
        escritor.writeheader()
        escritor.writerows(datos_ordenados)

    print(f"El archivo CSV '{nombre_archivo}' ha sido ordenado por 'REFERENCIA' "
          f"y se ha guardado como '{nombre_archivo_ordenado}'.")

def generar_encabezado (nombre_archivo):
    modo_archivo = "a" if os.path.exists(nombre_archivo) else "w"
    with open(nombre_archivo , modo_archivo) as archivo:
        #Generamos las claves
        mensaje_principal = "{0},{1},{2},{3},{4},{5}\n"
        mensaje_principal = mensaje_principal.format(
                "NUMERO DE VENTANA",
                "ID FILA",
                "ID",
                "hora",
                "ESTADO",
                "REFERENCIA",
                )
        archivo.write(mensaje_principal)


lista = leer_csv(pathCSVimportado)

generar_encabezado(pathCSVexportado)
obtener_links(lista, fila_sin_id, cant_abrir_a_la_vez)


try:    
    ordenar_csv_por_REFERENCIA(pathCSVexportado)
except:
    print("No se pudo ordenar")
    pass



