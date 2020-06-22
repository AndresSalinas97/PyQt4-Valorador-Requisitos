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

    # Espacio vertical entre los elementos del grid layout
    _VERTICAL_SPACING = 10

    # Espacio horizontal entre los elementos del grid layout
    _HORIZONTAL_SPACING = 30

    # Ancho mínimo de las columnas del grid layout
    _COLUMN_0_MIN_WIDTH = 200
    _COLUMN_1_MIN_WIDTH = 250
    _COLUMN_2_MIN_WIDTH = 250

    # Factor de estiramiento de las columnas del grid layout
    _COLUMN_0_STRETCH = 1
    _COLUMN_1_STRETCH = 2
    _COLUMN_2_STRETCH = 2

    # Altura mínima de las final del grid layout
    _ROW_1_MIN_HEIGHT = 100
    _ROW_4_MIN_HEIGHT = 100
    _ROW_8_MIN_HEIGHT = 100

    def __init__(self):
        super(ValoradorWidget, self).__init__()
        self._initUI()

    def _initUI(self):
        """
        Inicialización de la interfaz.
        """
        ##### Fuentes #####
        self.bold_label_font = QtGui.QFont()
        self.bold_label_font.setBold(True)

        ##### Etiquetas #####
        caso_label = QtGui.QLabel(u"Caso")
        caso_label.setFont(self.bold_label_font)

        desc_caso_label = QtGui.QLabel(u"Descripción del caso")
        desc_caso_label.setFont(self.bold_label_font)

        criterio_label = QtGui.QLabel(u"Criterio")
        criterio_label.setFont(self.bold_label_font)

        desc_criterio_label = QtGui.QLabel(u"Descripción del criterio")
        desc_criterio_label.setFont(self.bold_label_font)

        valor_criterio_label = QtGui.QLabel(u"Valor")
        valor_criterio_label.setFont(self.bold_label_font)

        valoracion_label = QtGui.QLabel(u"Valoración")
        valoracion_label.setFont(self.bold_label_font)

        explicacion_label = QtGui.QLabel(u"Explicación")
        explicacion_label.setFont(self.bold_label_font)

        ##### Botones #####
        self.abrir_Button = QtGui.QPushButton(u"Abrir fichero de caso")
        self.abrir_Button.setStatusTip(
            u"Abrir fichero JSON con el caso a valorar")

        self.valorar_Button = QtGui.QPushButton(u"VALORAR")
        self.valorar_Button.setStatusTip(
            u"Iniciar proceso de valoración")

        self.reset_Button = QtGui.QPushButton(u"Reset")
        self.reset_Button.setStatusTip(
            u"Reinicializar resultado y valores de los criterios")

        ##### Campos de texto de una línea #####
        self.ruta_caso_LineEdit = QtGui.QLineEdit()
        self.ruta_caso_LineEdit.setReadOnly(True)
        self.ruta_caso_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ruta_caso_LineEdit.setStatusTip(u"Ruta del caso abierto")

        ##### Campos de texto #####
        self.desc_caso_TextEdit = QtGui.QTextEdit()
        self.desc_caso_TextEdit.setReadOnly(True)
        self.desc_caso_TextEdit.setMinimumHeight(1)
        self.desc_caso_TextEdit.setStatusTip(u"Descripción del caso abierto")

        self.desc_criterio_TextEdit = QtGui.QTextEdit()
        self.desc_criterio_TextEdit.setReadOnly(True)
        self.desc_criterio_TextEdit.setMinimumHeight(1)
        self.desc_criterio_TextEdit.setStatusTip(
            u"Descripción del criterio seleccionado")

        self.valoracion_TextEdit = QtGui.QTextEdit()
        self.valoracion_TextEdit.setReadOnly(True)
        self.valoracion_TextEdit.setMinimumHeight(1)
        self.valoracion_TextEdit.setStatusTip(u"Resultado de la valoración")

        self.explicacion_TextEdit = QtGui.QTextEdit()
        self.explicacion_TextEdit.setReadOnly(True)
        self.explicacion_TextEdit.setMinimumHeight(1)
        self.explicacion_TextEdit.setStatusTip(u"Explicación del resultado")

        ##### Lista de criterios #####
        self.criterios_List = QtGui.QListWidget()
        self.criterios_List.setMinimumHeight(1)
        # Mostramos siempre las barras de scroll para evitar bug en el que
        # dichas barras de scroll no aparecen cuando deberían.
        self.criterios_List.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.criterios_List.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.criterios_List.setStatusTip(
            "Criterios del caso (seleccione uno para examinarlo e introducir " +
            "su valor)")

        ##### Configuración grid layout #####
        grid = QtGui.QGridLayout()

        grid.setVerticalSpacing(self._VERTICAL_SPACING)
        grid.setHorizontalSpacing(self._HORIZONTAL_SPACING)

        grid.setColumnMinimumWidth(0, self._COLUMN_0_MIN_WIDTH)
        grid.setColumnMinimumWidth(1, self._COLUMN_1_MIN_WIDTH)
        grid.setColumnMinimumWidth(2, self._COLUMN_2_MIN_WIDTH)

        grid.setColumnStretch(0, self._COLUMN_0_STRETCH)
        grid.setColumnStretch(1, self._COLUMN_1_STRETCH)
        grid.setColumnStretch(2, self._COLUMN_2_STRETCH)

        grid.setRowMinimumHeight(1, self._ROW_1_MIN_HEIGHT)
        grid.setRowMinimumHeight(4, self._ROW_4_MIN_HEIGHT)
        grid.setRowMinimumHeight(7, self._ROW_8_MIN_HEIGHT)

        grid.addWidget(caso_label, 0, 0, 1, 2)
        grid.addWidget(desc_caso_label, 0, 2, 1, 1)

        grid.addWidget(self.ruta_caso_LineEdit, 1, 0, 1, 2)
        grid.addWidget(self.desc_caso_TextEdit, 1, 2, 1, 1)

        grid.addWidget(self.abrir_Button, 2, 0, 1, 3)

        grid.addWidget(criterio_label, 3, 0, 1, 1)
        grid.addWidget(desc_criterio_label, 3, 1, 1, 1)
        grid.addWidget(valor_criterio_label, 3, 2, 1, 1)

        grid.addWidget(self.criterios_List, 4, 0, 1, 1)
        grid.addWidget(self.desc_criterio_TextEdit, 4, 1, 1, 1)
        # grid.addWidget(self., 4, 2, 1, 1)

        grid.addWidget(self.valorar_Button, 5, 0, 1, 3)

        grid.addWidget(valoracion_label, 6, 0, 1, 2)
        grid.addWidget(explicacion_label, 6, 2, 1, 1)

        grid.addWidget(self.valoracion_TextEdit, 7, 0, 1, 2)
        grid.addWidget(self.explicacion_TextEdit, 7, 2, 1, 1)

        grid.addWidget(self.reset_Button, 8, 0, 1, 3)

        self.setLayout(grid)


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
    print("Este módulo no debería ser ejecutado", file=sys.stderr)

    execfile('src/valorador.py')  # TODO: Eliminar esto
