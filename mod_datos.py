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
config_programas = leerConfiguracion("Torta")
matrizDatos = []





def obtenerDuracionProgramas(transmision,temporada):


    
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









                


obtenerDuracionProgramas(4,2)