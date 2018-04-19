#!/usr/bin/env python
"""Define todas las funciones que leen configuraciones de archivos JSON

aux_config.py contiene las definiciones de las funciones que se encargan de
leer archivos JSON que contienen valores sobre configuraciones necesarias
para el funcionamiento de INSIDIOSA. Dichos valores obtenidos en JSON son
retornados como arreglos.
"""

import requests
import json

__author__ = "Ignacio Tula"
__copyright__ = "Ignacio Tula, Logos Consultora, Logosfera, Zero, 2018"
__credits__ = ["Ignacio Tula", "Tamara Polo"]
__license__ = "AGPL"
__version__ = "0.0.1"
__maintainer__ = "Ignacio Tula"
__email__ = "itula@logos.net.ar"
__status__ = "Producción"


def leerConfiguracion(solicitud):
    json_file = "Configuracion/" + solicitud + ".json"
    json_data= open(json_file,"r")
    json_prueba = json_data.readlines()
    json_data.close()
    if len(json_prueba) == 0:
        return ""
    json_data= open(json_file,"r")
    data = json.load(json_data)
    json_data.close()
    return data



def corregirDobleComilla(string):
    nuevoString = ""
    for i in string:
        if i == "'":
            nuevoString = nuevoString + "\""
        else:
            nuevoString = nuevoString + i

    return nuevoString