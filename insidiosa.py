#!/usr/bin/env python
""" Programa principal de Insidiosa, este es el ejecutable

Sirve para crear una lista de reproducción automatizada basada en tortas repetibles
de 24hs de duración. Combina videos de programas, con tandas y promos para mantener
el horario. Es una paparruchada que sirve para automatizar transmisiones sin mucha
importancia.

"""

import requests
import json
from aux_config import * 

__author__ = "Ignacio Tula"
__copyright__ = "Ignacio Tula, Logos Consultora, Logosfera, Zero, 2018"
__credits__ = ["Ignacio Tula", "Tamara Polo"]
__license__ = "AGPL"
__version__ = "0.0.1"
__maintainer__ = "Ignacio Tula"
__email__ = "itula@logos.net.ar"
__status__ = "Desarrollo"



config_rutas = leerConfiguracion("Rutas")
config_programas = leerConfiguracion("Programas")

