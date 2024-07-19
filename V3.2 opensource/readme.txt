"""
BOT PARA SALTEARSE LA FILA VIRTUAL

Instagram:  @Agus_teira 
Twitter:    @g_teira3
Github:     https://github.com/agusteira

04/07/2023
"""

Hay 2 archivos "generar_link.py" y "obtener_tiempo.py"

La mayoria de cosas ya estan explicadas dentro de cada codigo, primero perdon por la desprolijidad
recien arranco a aprender a codear, y este fue uno de mis primeros proyectos solo

Segundo, el codigo "generar_link.py", lo que hace, bueno, es eso, generar un link, se tiene que ejecutar antes
de que arranque la cola, y las cosas especificas a modificar estan detalladas dentro del codigo

Tercero, el codigo "obtener_tiempo.py" se tiene que ejecutar cuando ya arranco la fila y te dice
en que posicion esta, esto podes modificar que referencia usar, algunas paginas de queue it utilizan 
el metodo de "faltan tantos minutos", otras te dicen "Estas en la posicion X", y asi. Asi que 
eso lo pueden modificar ustedes

Y por ultimo, y por lo que comparto el codigo, es el captcha, no encontre forma de saltearmelo facil, y todavia no estoy muy familiarizado
con JS ni con cosas backend que puedan servir para saltearme el codigo.

Cosas que se podrian agregrar/selenium
    -Manejo de proxies
    -En vez de utilizar selenium utilizar otra libreria que no tengas que abrir la paginas
     como REQUESTS, pero que tampoco te bloquee la ip
    -Algo para saltearse el captcha

Librerias utilizadas:
    -Selenium
