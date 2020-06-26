#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Trabajo final de ISSBC.

Módulo principal.

Programa valorador de criterios desarrollado con PyQt4 siguiendo la arquitectura
Modelo-Vista-Controlador y la metodología CommonKADS. Permite llevar a cabo la
tarea de valoración de CommonKADS sobre diferentes dominios de aplicación.

El programa cuenta una interfaz gráfica para que el usuario pueda introducir el
valor de cada criterio y comprobar el resultado de la tarea de valoración de
forma cómoda.

Cada caso (dominio) cuenta con una serie de criterios que serán evaluados de
forma independiente: si un solo criterio es rechazado todo el caso será
rechazado.

Los casos y todos sus criterios se cargan a través de un fichero JSON con un
formato determinado. Puede ver un ejemplo en /casos-de-ejemplo/ejemplo.json

El programa trabaja con tres tipos de criterios:
    Criterio Booleano: Su valor es True o False. El criterio será valorado como
                       "Aprobado" si el valor introducido coincide con el
                       'valor_deseado' indicado en el JSON.
    Criterio Porcentaje: Su valor es un porcentaje (0% - 100%) expresado con un
                         número decimal (0.0 - 1.0). El criterio será valorado
                         como "Aprobado" si el valor introducido se encuentra
                         entre los valores 'valor_minimo' y 'valor_maximo'
                         especificados en el JSON.
    Criterio Numero: Su valor es un número (entero o decimal). El criterio será
                     valorado como "Aprobado" si el valor introducido se
                     encuentra entre los valores 'valor_minimo' y 'valor_maximo'
                     especificados en el JSON.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from valorador_model import ValoradorModel
from valorador_view import ValoradorView
from valorador_controller import ValoradorController
import sys
from PyQt4 import QtGui


class Valorador():
    """
    Monta todas las piezas del MVC e inicia el programa.
    """

    def __init__(self):
        app = QtGui.QApplication(sys.argv)

        controller = ValoradorController(ValoradorModel(), ValoradorView())

        sys.exit(app.exec_())


if __name__ == "__main__":
    """
    Función principal: Inicia el programa.
    """
    valorador_program = Valorador()
