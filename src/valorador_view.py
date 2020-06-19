#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con la vista del valorador.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui


class ValoradorView():
    """
    Clase con la vista del valorador.

    Monta la interfaz del valorador a partir de las clases ValoradorWidget y
    ValoradorMainWindow y permite acceder a ellas a partir de sus atributos.

    Atributos/Propiedades:
        widget: QWidget con la interfaz del valorador (objeto de la clase
            ValoradorWidget).
        mainWindow: Ventana principal (objeto de la clase ValoradorMainWindow).
    """

    def __init__(self):
        self.widget = ValoradorWidget()
        self.mainWindow = ValoradorMainWindow(self.widget)

    def show(self):
        """
        Hace visible la ventana principal.
        """
        self.mainWindow.show()


class ValoradorWidget(QtGui.QWidget):
    """
    QWidget con la interfaz del valorador.

    Atributos/Propiedades:
        TODO: Documentar
    """

    def __init__(self):
        super(ValoradorWidget, self).__init__()

        self._initUI()

    def _initUI(self):
        """
        Inicialización de la interfaz.
        """
        pass


class ValoradorMainWindow(QtGui.QMainWindow):
    """
    Ventana principal del programa.

    Contiene la barra de menús, la barra de herramientas, la barra de estado, y,
    por supuesto, el widget con el valorador.

    Argumentos:
        valoradorWidget: Widget con el valorador (objeto de la clase
            valoradorWidget)

    Atributos/Propiedades:
        valoradorWidget: Widget con el valorador (objeto de la clase
            valoradorWidget)
        exitAction: QAction para salir del programa.
        openFileAction: QAction para abrir fichero de dominio.
    """

    def __init__(self, valoradorWidget):
        super(ValoradorMainWindow, self).__init__()

        self.valoradorWidget = valoradorWidget

        self._initUI()

    def _initUI(self):
        """
        Inicialización de la interfaz.
        """

        ##### Acciones #####
        self.exitAction = QtGui.QAction("Salir", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip("Salir del programa")

        self.openFileAction = QtGui.QAction("Abrir Fichero de dominio", self)
        self.openFileAction.setShortcut('Ctrl+O')
        self.openFileAction.setStatusTip("Abrir fichero")

        ##### Barra de menús #####
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Archivo')
        fileMenu.addAction(self.openFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        ##### Barra de estado #####
        self.statusBar()  # Activa la barra de estado.

        ##### Widget contador #####
        # Añade a la ventana principal el contador.
        self.setCentralWidget(self.valoradorWidget)

        ##### Propiedades ventana #####
        self.setWindowTitle("Valorador")


class MessageBoxes():
    """
    Contiene métodos para mostrar mensajes emergentes y ventanas de diálogo
    para abrir/guardar ficheros/directorios.
    """

    @staticmethod
    def showErrorMessage(errorText):
        """
        Muestra una ventana emergente de error con el mensaje indicado en
        el argumento errorText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(errorText)
        msg.exec_()

    @staticmethod
    def showInfoMessage(infoText):
        """
        Muestra una ventana emergente de información con el mensaje indicado en
        el argumento infoText.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Informacion")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(infoText)
        msg.exec_()

    @staticmethod
    def confirmOperationMessage(infoText):
        """
        Muestra una ventana emergente de advertencia para confirmar que el
        usuario desea continuar con la operación.

        Devuelve:
            True si el usuario hace click en Ok; False en caso contrario.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle("Advertencia")
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText(infoText)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        retval = msg.exec_()

        if (retval == QtGui.QMessageBox.Ok):
            return True
        else:
            return False

    @staticmethod
    def openFileDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar el fichero a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return QtGui.QFileDialog.getOpenFileName(parent, "Abrir fichero")

    @staticmethod
    def openFolderDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar la carpeta a abrir.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta de la carpeta seleccionada.
        """
        return QtGui.QFileDialog.getExistingDirectory(
            parent, "Seleccionar carpeta")

    @staticmethod
    def saveFileDialog(parent):
        """
        Muestra una ventana de diálogo para seleccionar dónde se guardará el
        fichero.

        Argumentos:
            parent: QWidget padre.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return QtGui.QFileDialog.getSaveFileName(parent, 'Guardar Como...')


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no puede ser ejecutado", file=sys.stderr)
