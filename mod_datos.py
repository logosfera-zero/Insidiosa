#!/usr/bin/env python
""" Este modulo carga los datos de duración de los videos administrados

Rellena los json de la carpeta Datos con el fin de crear una pequeña base
de datos con las duraciones de los programas afectados, tandas y promos.

"""

import requests
import json
from aux_config import * 
from aux_tiempos import * 
import os
import sys
import subprocess
from os import listdir
from os.path import isfile, join

__author__ = "Ignacio Tula"
__copyright__ = "Ignacio Tula, Logos Consultora, Logosfera, Zero, 2018"
__credits__ = ["Ignacio Tula", "Tamara Polo"]
__license__ = "AGPL"
__version__ = "0.0.1"
__maintainer__ = "Ignacio Tula"
__email__ = "itula@logos.net.ar"
__status__ = "Desarrollo"



config_rutas = leerConfiguracion("Rutas")

matrizDatos = []





def obtenerDuracionProgramas(transmision,temporada):

    config_programas = leerConfiguracion("Torta")
    
    # Por cada Programa
    for i in config_programas['programas']:
        print ("BUCLE DE " + str(i))

        # Si está organizado por carpetas
        if config_programas['OrganizadoEnCarpetas']:

            # Según este en mayus o minus las carpetas
            if config_programas['CarpetasenMayusculas']:
                i_string = str(i['programa']).upper()
            else:
                i_string = str(i['programa']).lower()

            # Forma la ruta probable
            ruta = str(config_rutas["rutaProgramas"] + i_string)
        
            # Confirma la existencia de ruta probable + carpeta de programa
            if os.path.isdir(ruta):
                imprimir= "\n LEYENDO CARPETA: " + ruta
                print(imprimir)
                
                bloqueActual = 1
                buscando = True

                MatrizDelPrograma = {}
                MatrizDelPrograma['Programa'] = i_string.upper()
                MatrizDelPrograma['Duracion'] = "DESCONOCIDA"
                MatrizDelPrograma['Obligatorio'] = i['obligatorio']
                MatrizDelPrograma['Bloques'] = []

                while buscando:
                    

                    stringComposicion = "PGM - " + i_string.upper()  
                    stringComposicion = stringComposicion + " - T" + str(temporada) + "_P" + str(transmision)
                    stringComposicion = stringComposicion + " - BLQ" + str(bloqueActual)
                    stringComposicion = stringComposicion + config_programas['ExtensionDeVideoBuscada']
                    rutayString = ruta + "\\" +  stringComposicion
                    print("\nPROBANDO SI EXISTE: " + rutayString)
                
                    if isfile(rutayString):

                        
                        
                        print("Existe :" + stringComposicion)
                        matrizMenorDatos = []
                        matrizMenorDatos.append(stringComposicion)
                        batcmd = '"' + config_rutas["rutaExif"] + '" -api largefilesupport=1 -MediaDuration "'  + rutayString + '"' 

                        try:
                            duracion = str(subprocess.check_output(batcmd, shell=True))
                        except subprocess.CalledProcessError as e:
                            continue

                        duracion = str(duracion).replace("b'Media Duration                  : ","")
                        duracion = duracion[0:-5]
                        print("Duración del bloque " + str(bloqueActual) + ":" , str(duracion))
                        matrizMenorDatos.append(duracion)
                        MatrizDelPrograma['Bloques'].append(matrizMenorDatos)
                        bloqueActual+=1
                    
                    else:
                        buscando = False

                    
                if len(MatrizDelPrograma) != 0:

                    dur = 0
                    for blq in MatrizDelPrograma['Bloques']:
                        dur = dur + DuracionHaciaSegundos(blq[1]) 
                    
                    MatrizDelPrograma['Duracion'] = SegundosHaciaDuracion(dur)
                    matrizDatos.append(MatrizDelPrograma)

    
    data = corregirDobleComilla(str(matrizDatos))
    archi =  open ("Datos/Programas.json","w")
    archi.write(data)
    archi.close()




def obtenerDuracionTanda():

    config_tandas = leerConfiguracion("Torta")
    
    # Por cada Tipo de Tanda
    for i in config_tandas['tandas']:
        print ("BUCLE DE " + str(i))

       
        

        # Según este en mayus o minus las carpetas
        if config_tandas['CarpetasenMayusculas']:
            i_string = str(i['tipo']).upper()
        else:
            i_string = str(i['tipo']).lower()

        # Forma la ruta probable
        ruta = str(config_rutas["rutaTandas"] + i_string)
    
        # Confirma la existencia de ruta probable + carpeta de programa
        if os.path.isdir(ruta):
            imprimir= "\n LEYENDO CARPETA: " + ruta
            print(imprimir)
            
            
            

            
            
            todasLasTandas = listdir(ruta)

            for tanda in todasLasTandas:
                
                MatrizDeLaTanda = []

                tanda = str(tanda)    

                print(tanda[len(tanda) - 4:len(tanda)])
            
                if tanda[len(tanda) - 4:len(tanda)] == ".mp4":
                    MatrizDeLaTanda.append(ruta + "\\" + tanda)
                    MatrizDeLaTanda.append(tanda)
                    
                    
                    print("Existe :" + MatrizDeLaTanda[0])
                    
                    batcmd = '"' + config_rutas["rutaExif"] + '" -api largefilesupport=1 -MediaDuration "'  + MatrizDeLaTanda[0] + '"' 

                    try:
                        duracion = str(subprocess.check_output(batcmd, shell=True))
                    except subprocess.CalledProcessError as e:
                        continue

                    duracion = str(duracion).replace("b'Media Duration                  : ","")
                    duracion = duracion[0:-5]
                    print("Duración de la tanda " + str(MatrizDeLaTanda[1]) + ":  " , str(duracion))
                    MatrizDeLaTanda.append(duracion)
                    
                    
                
              

                
                if len(MatrizDeLaTanda) != 0:

                    matrizDatos.append(MatrizDeLaTanda)

    
    data = corregirDobleComilla(str(matrizDatos))
    archi =  open ("Datos/Tandas.json","w")
    archi.write(data)
    archi.close()




def obtenerDuracionTandaRelleno():

    config_tandas = leerConfiguracion("Torta")
    
    # Por cada Tipo de Tanda
    for i in config_tandas['tandasRelleno']:
        print ("BUCLE DE " + str(i))

       
        

        # Según este en mayus o minus las carpetas
        if config_tandas['CarpetasenMayusculas']:
            i_string = str(i['tipo']).upper()
        else:
            i_string = str(i['tipo']).lower()

        # Forma la ruta probable
        ruta = str(config_rutas["rutaTandas"] + i_string)
    
        # Confirma la existencia de ruta probable + carpeta de programa
        if os.path.isdir(ruta):
            imprimir= "\n LEYENDO CARPETA: " + ruta
            print(imprimir)
            
            
            

            
            
            todasLasTandas = listdir(ruta)

            for tanda in todasLasTandas:
                
                MatrizDeLaTanda = []

                tanda = str(tanda)    

                #print(tanda[len(tanda) - 4:len(tanda)])
            
                if tanda[len(tanda) - 4:len(tanda)] == ".mp4":
                    MatrizDeLaTanda.append(ruta + "\\" + tanda)
                    MatrizDeLaTanda.append(tanda)
                    
                    
                    print("Existe :" + MatrizDeLaTanda[0])
                    
                    batcmd = '"' + config_rutas["rutaExif"] + '" -api largefilesupport=1 -MediaDuration "'  + MatrizDeLaTanda[0] + '"' 

                    try:
                        duracion = str(subprocess.check_output(batcmd, shell=True))
                    except subprocess.CalledProcessError as e:
                        continue

                    duracion = str(duracion).replace("b'Media Duration                  : ","")
                    duracion = duracion[0:-5]
                    print("Duración de la tanda " + str(MatrizDeLaTanda[1]) + ":  " , str(duracion))
                    MatrizDeLaTanda.append(duracion)
                    
                    
                
              

                
                if len(MatrizDeLaTanda) != 0:

                    matrizDatos.append(MatrizDeLaTanda)

    
    data = corregirDobleComilla(str(matrizDatos))
    archi =  open ("Datos/TandasRelleno.json","w")
    archi.write(data)
    archi.close()



def obtenerDuracionPromos(transmision,temporada):

    config_promos = leerConfiguracion("Torta")

    # Por cada Tipo de Promo
    for i in config_promos['Promos']:

        if i["dePrograma"] == 1:
            
            # Forma la ruta probable
            ruta = str(config_promos["rutaPromos"])
            todasLasPromos = listdir(ruta)

            for promo in todasLasPromos:
                
                promoCorrecta = promo.find("PROMOS - " + i["tipo"] + " - ")

                if promo[len(tanda) - 4:len(tanda)] == ".mp4" and promoCorrecta != -1:

                    
                    





    
    


    
    data = corregirDobleComilla(str(matrizDatos))
    archi =  open ("Datos/TandasRelleno.json","w")
    archi.write(data)
    archi.close()



obtenerDuracionTanda()
obtenerDuracionTandaRelleno()
#obtenerDuracionProgramas(4,2)
