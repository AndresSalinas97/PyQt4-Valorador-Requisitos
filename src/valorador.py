#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Trabajo final de ISSBC.

Módulo principal.

Programa valorador de criterios desarrollado con PyQt4 siguiendo la arquitectura Modelo-Vista-Controlador y la metodología CommonKADS. Permite realizar la tarea
de valoración de CommonKADS sobre diferentes dominios de aplicación.

TODO: Explicar qué es lo que hace y cómo funciona

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
    ValoradorProgram = Valorador()
