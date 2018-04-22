#!/usr/bin/env python
""" 
Este modulo contiene funciones para asistir en el cálculo de tiempo

"""

__author__ = "Ignacio Tula"
__copyright__ = "Ignacio Tula, Logos Consultora, Logosfera, Zero, 2018"
__credits__ = ["Ignacio Tula", "Tamara Polo"]
__license__ = "AGPL"
__version__ = "0.0.1"
__maintainer__ = "Ignacio Tula"
__email__ = "itula@logos.net.ar"
__status__ = "Desarrollo"



def DuracionHaciaSegundos(cadena):
    cadena = cadena.split(":")
    horas = int(cadena[0])
    minutos = int(cadena[1])
    segundos = int(cadena[2])

    segundosTotales = horas * 3600 + minutos * 60 + segundos
    return segundosTotales


def SegundosHaciaDuracion(timestamp):
    horas = timestamp // 3600
    minutos = (timestamp % 3600 ) // 60
    segundos =  (timestamp % 3600) % 60
    cadena = str(horas) + ":" + str(minutos) + ":" + str(segundos)
    return cadena