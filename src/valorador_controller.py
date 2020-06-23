#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el controlador del valorador.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
from valorador_view import MessageBoxes
import sys
from PyQt4 import QtGui


class ValoradorController():
    """
    Clase con el controlador del valorador.

    Argumentos constructor:
        model: objeto de la clase ValoradorModel.
        view: objeto de la clase ValoradorView.

    Atributos/Propiedades:
        model: objeto de la clase ValoradorModel.
        view: objeto de la clase ValoradorView.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._initModel()
        self._initView()
        self._initController()

    def _initModel(self):
        """
        Inicializa el modelo.
        """
        pass

    def _initView(self):
        """
        Inicializa la vista.
        """
        self._updateView()
        self.view.show()

    def _initController(self):
        """
        Inicializa el controlador.

        Conecta los botones y acciones de la vista con métodos del controlador.
        """
        pass

    def _updateView(self):
        """
        Actualiza la vista.
        """
        pass


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no debería ser ejecutado", file=sys.stderr)

    execfile('src/valorador.py')  # TODO: Eliminar esto
