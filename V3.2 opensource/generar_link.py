"""
Codigo para generar filas

Instagram:  @Agus_teira 
Twitter:    @g_teira3
Github:     https://github.com/agusteira

04/07/2023
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import random
import datetime


fila_sin_id = fr""                                                              #Esta es la fila normal para entrar, NO TIENE QUE TENER ID, por ej: https://dfentertainment.queue-it.net/?c=dfentertainment&e=lolla24&cid=es-CL&q=
link = fr"{fila_sin_id}00000000-0000-0000-0000-000000000000"

hora_fila = "09:50:15"                                                          #Hora que queres que pare de generarse la fila
cant_paginas = 20                                                               #Cantidad de paginas a abrir por ventana
links = 0                                                                       #Cantidad de links generados en el csv/excel
nombreCSV= ""                                                                   #Nombre del archivo de excel para manejar las filas   (Hay que modificarla)            
pathCSV = fr".......{nombreCSV}.csv"                                            #Ruta del csv (Hay que modificarla)



def obtener_links_allacess(hora_fila: str, fila_sin_id: str, numero_de_ventana: int, cant_paginas: int) -> list:
    """
    Esta funcion basicamente te abre las pestañas que generaste en el archivo anterior
    y les busca las referencias para poder saber a cuanto tiempo estas de entrar
    y despues te exporta el mismo csv que antes, pero con las referencias cargadas.
    Tambien imprime por consola la referencia, y el id del link

    Recibe: 
            -La hora que queres que termine de generar filas
            -La fila sin ID
            -Cantidad de filas YA generadas (0 en caso de que se abra por primera vez)
            -Cantidad de paginas para abrir por ventana
    Devuelve:
            -Un CSV con:
                        Numeracion
                        Link
                        Id del link
                        Hora que se genero
            -Una flag de si se paso el tiempo establecido
    """

    browser = webdriver.Chrome() #Me abre el navegador
    lista_paginas = []

    for i in range(cant_paginas):
        browser.execute_script("window.open('about:blank','_blank');") #Abre nuevas pestañas en blanco

    handles = browser.window_handles #Le asigna un valor a cada pestaña

    for handle in handles: #Recorre las pestañas
        #idddd = fila_aleatoria()
        #linki = f"{fila_sin_id}{idddd}      
        browser.switch_to.window(handle)
        browser.get(link) #Le abre un link a cada pestaña       
        
        #----> Si queres usar la funcion FILA_ALEATORIA, descomenta los primeros 2 renglones
        #       y cambia en     browser.get(link)       link por linki


    for i, handle in enumerate(handles, start=1):
        """
        Esta vez recorremos las pestañas, 
        pero para agarrar la info que hay
        en ellas
        """
        pagina = {}

        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        pagina["hora"] = hora_actual

        numero_de_ventana_nuevo = numero_de_ventana + i #Enumera las paginas
        pagina["NUMERO DE VENTANA"] = numero_de_ventana_nuevo
        time.sleep(1)
        
        id_fila = browser.find_element(By.ID, 'hlLinkToQueueTicket2') 
        #Agarra el identificador de fila, esto hay que modificarlo segun la pagina y lo que muestra
        # ----- MainPart_lbUsersInLineAheadOfYou | hlLinkToQueueTicket2

        pagina["ID FILA"] = fila_sin_id + id_fila.text
        pagina["ID"] = id_fila.text
        pagina["REFERENCIA"] = ""  #Esto va vacio porque se completa en el obtenedor_tiempo

        lista_paginas.append(pagina) #Importamos todos los datos de la pagina a una diccionario que esta dentro de una lista
        browser.switch_to.window(handle) #Cambia de pagina

    generar_csv(lista_paginas, pathCSV)
    #Cuando termina con todas las pestañas de la ventana, se anexa la informacion al CSV

    if hora_actual < hora_fila:
        flag_tiempo = True
        return flag_tiempo
    else:
        #--------------Si la hora que elegiste ya paso, te muestra este menu--------------------------------
        print(f"\n\nLINKS GENERADOS: {cant_paginas}\n\n")
        salir = input("¿Desea salir? Presione 'S' para salir: ")
        if salir == "S":
            flag_tiempo = False
            return flag_tiempo
        else:
            hora_fila = input("Introduzca la nueva hora de salida: ")

def fila_aleatoria():
    """
    En esta funcion, generamos un ID aleatorio, NO SIRVE, solo es para
    hacer pruebas con diferentes IDs si no podemos generarlos
    """
    cadena_id = "00000000-0000-0000-0000-000000000000"
    nueva_cadena = ""

    for caracter in cadena_id:
        if caracter == "0":
            nueva_cadena += random.choice("0123456789abcdef")
        else:
            nueva_cadena += caracter
    return nueva_cadena

def generar_csv(lista:list, nombre_archivo:str):
    """
    A partir de una lista, y un nombre, crea un archivo 
    CSV con los datos de la lista con el nombre pasado
    Recibe: una lista con datos de personajes
    devuele: Crea un archivo CSV segun lo pasado
    """
    if len (lista)>0:
        with open(nombre_archivo , "a") as archivo:
            for e_caracteristica in lista:
                mensaje = "{0},{1},{2},{3},{4}\n"
                
                mensaje = mensaje.format(
                    e_caracteristica["NUMERO DE VENTANA"],
                    e_caracteristica["ID FILA"],
                    e_caracteristica["ID"],
                    e_caracteristica["hora"],
                    "",
                    e_caracteristica["REFERENCIA"]
                    )
                print(mensaje)
                archivo.write(mensaje)
            
    else:
        return -1

def generar_encabezado (nombre_archivo):
    modo_archivo = "a" if os.path.exists(nombre_archivo) else "w"
    with open(nombre_archivo , modo_archivo) as archivo:
        #Generamos las claves
        mensaje_clave = "{0},{1},{2},{3}\n"
        mensaje_clave = mensaje_clave.format ("NUMERO DE VENTANA", "ID FILA", "ID", "hora", "ESTADO", "REFERENCIA")
        print(mensaje_clave)
        archivo.write(mensaje_clave)



#-------------------------------------------------------------EJECUCION DEL PROGRAMA---------------------------------------------------------------------

generar_encabezado(pathCSV) #El encabezado solamente hay que ejecutarlo la primera vez, luego comentarlo

flag_tiempo = True
while flag_tiempo:  #Mientras la hora no sea la 
    flag_tiempo = obtener_links_allacess (hora_fila, fila_sin_id, links, cant_paginas)
    links += cant_paginas + 1 


"""
-La ID 00...00 te genera nuevos links en el mismo navegador
"""
