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
        main_widget: QWidget con la interfaz del valorador (objeto de la clase
            ValoradorWidget).
        main_window: Ventana principal (objeto de la clase ValoradorMainWindow).
    """

    def __init__(self):
        self.main_widget = ValoradorWidget()
        self.main_window = ValoradorMainWindow(self.main_widget)

    def show(self):
        """
        Hace visible la ventana principal.
        """
        self.main_window.show()


class ValoradorWidget(QtGui.QWidget):
    """
    QWidget con la interfaz del valorador.

    Atributos/Propiedades:
        abrir_Button: QPushButton para abrir fichero del caso.
        valorar_Button: QPushButton para valorar el caso.
        reset_Button: QPushButton para reinicializar el caso.
        ruta_caso_LineEdit: QLineEdit de solo lectura que muestra la ruta del
                            fichero del caso.
        valor_LineEdit: QLineEdit para introducir el valor de un requisito
                        del tipo Porcentaje o Numero.
        valor_ComboBox: QComboBox para introducir el valor de un requisito
                        del tipo Booleano.
        desc_caso_TextEdit: QTextEdit de solo lectura que muestra la
                            descripción del caso.
        desc_requisito_TextEdit: QTextEdit de solo lectura que muestra la
                                descricpión del requisito seleccionado.
        valoracion_LineEdit: QLineEdit de solo lectura que muestra el resultado
                             de la valoración.
        explicacion_TextEdit: QTextEdit de solo lectura que muestra la
                              explicación de la valoración.
        requisitos_List: QListWidget con la lista de requisitos del caso.
    """

    # Espacio vertical entre los elementos del grid layout.
    _VERTICAL_SPACING = 10

    # Espacio horizontal entre los elementos del grid layout.
    _HORIZONTAL_SPACING = 20

    # Ancho mínimo de las columnas del grid layout.
    _COLUMN_0_MIN_WIDTH = 200
    _COLUMN_1_MIN_WIDTH = 250
    _COLUMN_2_MIN_WIDTH = 250

    # Factor de estiramiento de las columnas del grid layout.
    _COLUMN_0_STRETCH = 2
    _COLUMN_1_STRETCH = 3
    _COLUMN_2_STRETCH = 3

    # Altura mínima de las filas del grid layout.
    _ROW_1_MIN_HEIGHT = 75
    _ROW_4_MIN_HEIGHT = 100
    _ROW_7_MIN_HEIGHT = 100

    # Factor de estiramiento de las filas del grid layout.
    _ROW_1_STRETCH = 1
    _ROW_4_STRETCH = 3
    _ROW_7_STRETCH = 6

    def __init__(self):
        super(ValoradorWidget, self).__init__()
        self._init_UI()

    def _init_UI(self):
        """
        Inicialización de la interfaz.
        """
        ##### Fuentes #####
        bold_font = QtGui.QFont()
        bold_font.setBold(True)

        big_bold_font = QtGui.QFont()
        big_bold_font.setBold(True)
        big_bold_font.setPointSize(40)

        ##### Etiquetas #####
        ruta_caso_label = QtGui.QLabel(u"Caso")
        ruta_caso_label.setFont(bold_font)

        desc_caso_label = QtGui.QLabel(u"Descripción del Caso")
        desc_caso_label.setFont(bold_font)

        requisito_label = QtGui.QLabel(u"Requisitos")
        requisito_label.setFont(bold_font)

        desc_requisito_label = QtGui.QLabel(u"Descripción del Requisito")
        desc_requisito_label.setFont(bold_font)

        valor_requisito_label = QtGui.QLabel(u"Valor del Requisito")
        valor_requisito_label.setFont(bold_font)

        valoracion_label = QtGui.QLabel(u"Valoración")
        valoracion_label.setFont(bold_font)

        explicacion_label = QtGui.QLabel(u"Explicación")
        explicacion_label.setFont(bold_font)

        ##### Botones #####
        self.abrir_Button = QtGui.QPushButton(u"Abrir Caso")
        self.abrir_Button.setStatusTip(
            u"Abrir fichero JSON con el caso a valorar")

        self.valorar_Button = QtGui.QPushButton(u"VALORAR")
        self.valorar_Button.setFont(bold_font)
        self.valorar_Button.setStatusTip(
            u"Iniciar proceso de valoración")

        self.reset_Button = QtGui.QPushButton(u"Reset")
        self.reset_Button.setStatusTip(
            u"Reinicializar resultado y valores de los requisitos")

        ##### Campos de texto de una línea #####
        self.ruta_caso_LineEdit = QtGui.QLineEdit()
        self.ruta_caso_LineEdit.setReadOnly(True)
        self.ruta_caso_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.ruta_caso_LineEdit.setStatusTip(u"Ruta del caso abierto")

        self.valoracion_LineEdit = QtGui.QLineEdit()
        self.valoracion_LineEdit.setReadOnly(True)
        self.valoracion_LineEdit.setMinimumHeight(1)
        self.valoracion_LineEdit.setFont(big_bold_font)
        self.valoracion_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.valoracion_LineEdit.setStatusTip(u"Resultado de la valoración")

        ##### Campos para los distintos tipos del valor del requisito #####
        self.valor_LineEdit = QtGui.QLineEdit()
        self.valor_LineEdit.setStatusTip(
            u"Valor del requisito seleccionado (número entero)")

        self.valor_ComboBox = QtGui.QComboBox()
        self.valor_ComboBox.addItems([u"None", u"True", u"False"])
        self.valor_ComboBox.setVisible(False)
        self.valor_ComboBox.setStatusTip(
            u"Valor del requisito seleccionado (True o False)")

        ##### Campos de texto #####
        self.desc_caso_TextEdit = QtGui.QTextEdit()
        self.desc_caso_TextEdit.setReadOnly(True)
        self.desc_caso_TextEdit.setMinimumHeight(1)
        self.desc_caso_TextEdit.setStatusTip(u"Descripción del caso abierto")

        self.desc_requisito_TextEdit = QtGui.QTextEdit()
        self.desc_requisito_TextEdit.setReadOnly(True)
        self.desc_requisito_TextEdit.setMinimumHeight(1)
        self.desc_requisito_TextEdit.setStatusTip(
            u"Descripción del requisito seleccionado")

        self.explicacion_TextEdit = QtGui.QTextEdit()
        self.explicacion_TextEdit.setReadOnly(True)
        self.explicacion_TextEdit.setMinimumHeight(1)
        self.explicacion_TextEdit.setStatusTip(u"Explicación del resultado")

        ##### Lista de requisitos #####
        self.requisitos_List = QtGui.QListWidget()
        self.requisitos_List.setMinimumHeight(1)
        self.requisitos_List.setStatusTip(
            u"Requisitos del caso (seleccione uno para examinarlo e " +
            u"introducir su valor)")

        ##### Cajas de layout #####
        abrir_Layout = QtGui.QHBoxLayout()
        abrir_Layout.setAlignment(QtCore.Qt.AlignCenter)
        abrir_Layout.addWidget(self.abrir_Button)
        abrir_Layout_Widget = QtGui.QWidget()
        abrir_Layout_Widget.setLayout(abrir_Layout)

        valorar_Layout = QtGui.QHBoxLayout()
        valorar_Layout.setAlignment(QtCore.Qt.AlignCenter)
        valorar_Layout.addWidget(self.valorar_Button)
        valorar_Layout_Widget = QtGui.QWidget()
        valorar_Layout_Widget.setLayout(valorar_Layout)

        reset_Layout = QtGui.QHBoxLayout()
        reset_Layout.setAlignment(QtCore.Qt.AlignCenter)
        reset_Layout.addWidget(self.reset_Button)
        reset_Layout_Widget = QtGui.QWidget()
        reset_Layout_Widget.setLayout(reset_Layout)

        ruta_caso_Layout = QtGui.QVBoxLayout()
        ruta_caso_Layout.setAlignment(QtCore.Qt.AlignTop)
        ruta_caso_Layout.addWidget(self.ruta_caso_LineEdit)
        ruta_caso_Layout_Widget = QtGui.QWidget()
        ruta_caso_Layout_Widget.setLayout(ruta_caso_Layout)

        valoracion_Layout = QtGui.QVBoxLayout()
        valoracion_Layout.setAlignment(QtCore.Qt.AlignTop)
        valoracion_Layout.addWidget(self.valoracion_LineEdit)
        valoracion_caso_Layout_Widget = QtGui.QWidget()
        valoracion_caso_Layout_Widget.setLayout(valoracion_Layout)

        valor_Layout = QtGui.QVBoxLayout()
        valor_Layout.setAlignment(QtCore.Qt.AlignTop)
        valor_Layout.addWidget(self.valor_LineEdit)
        valor_Layout.addWidget(self.valor_ComboBox)
        valor_Layout_Widget = QtGui.QWidget()
        valor_Layout_Widget.setLayout(valor_Layout)

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
        grid.setRowMinimumHeight(7, self._ROW_7_MIN_HEIGHT)

        grid.setRowStretch(1, self._ROW_1_STRETCH)
        grid.setRowStretch(4, self._ROW_4_STRETCH)
        grid.setRowStretch(7, self._ROW_7_STRETCH)

        grid.addWidget(ruta_caso_label, 0, 0, 1, 2)
        grid.addWidget(desc_caso_label, 0, 2, 1, 1)

        grid.addWidget(ruta_caso_Layout_Widget, 1, 0, 1, 2)
        grid.addWidget(self.desc_caso_TextEdit, 1, 2, 1, 1)

        grid.addWidget(abrir_Layout_Widget, 2, 0, 1, 3)

        grid.addWidget(requisito_label, 3, 0, 1, 1)
        grid.addWidget(desc_requisito_label, 3, 1, 1, 1)
        grid.addWidget(valor_requisito_label, 3, 2, 1, 1)

        grid.addWidget(self.requisitos_List, 4, 0, 1, 1)
        grid.addWidget(self.desc_requisito_TextEdit, 4, 1, 1, 1)
        grid.addWidget(valor_Layout_Widget, 4, 2, 1, 1)

        grid.addWidget(valorar_Layout_Widget, 5, 0, 1, 3)

        grid.addWidget(valoracion_label, 6, 0, 1, 2)
        grid.addWidget(explicacion_label, 6, 2, 1, 1)

        grid.addWidget(valoracion_caso_Layout_Widget, 7, 0, 1, 2)
        grid.addWidget(self.explicacion_TextEdit, 7, 2, 1, 1)

        grid.addWidget(reset_Layout_Widget, 8, 0, 1, 3)

        self.setLayout(grid)


class ValoradorMainWindow(QtGui.QMainWindow):
    """
    Ventana principal del programa.

    Contiene la barra de menús, la barra de estado, y, por supuesto, el widget
    con el valorador.

    Argumentos constructor:
        valorador_Widget: Widget con el valorador (objeto de la clase
            valoradorWidget)

    Atributos/Propiedades:
        valorador_Widget: Widget con el valorador (objeto de la clase
            valoradorWidget)
        exit_Action: QAction para salir del programa.
        open_file_Action: QAction para abrir fichero de dominio.
    """

    def __init__(self, valorador_Widget):
        super(ValoradorMainWindow, self).__init__()

        self.valorador_Widget = valorador_Widget

        self._init_UI()

    def _init_UI(self):
        """
        Inicialización de la interfaz.
        """

        ##### Acciones #####
        self.exit_Action = QtGui.QAction(u"Salir", self)
        self.exit_Action.setShortcut('Ctrl+Q')
        self.exit_Action.setStatusTip(u"Salir del programa")

        self.open_file_Action = QtGui.QAction(
            u"Abrir Fichero JSON de Caso", self)
        self.open_file_Action.setShortcut('Ctrl+O')
        self.open_file_Action.setStatusTip(
            u"Abrir fichero JSON con el caso a valorar")

        ##### Barra de menús #####
        menu_bar = self.menuBar()
        file_Menu = menu_bar.addMenu(u"Archivo")
        file_Menu.addAction(self.open_file_Action)
        file_Menu.addSeparator()
        file_Menu.addAction(self.exit_Action)

        ##### Barra de estado #####
        self.statusBar()  # Activa la barra de estado.

        ##### Widget contador #####
        # Añade a la ventana principal el contador.
        self.setCentralWidget(self.valorador_Widget)

        ##### Propiedades ventana #####
        self.setWindowTitle(u"Valorador de Requisitos")


class ValoradorMessageBoxes():
    """
    Contiene métodos para mostrar mensajes emergentes y ventanas de diálogo
    para abrir/guardar ficheros/directorios.
    """

    @staticmethod
    def show_error_message(error_text):
        """
        Muestra una ventana emergente de error con el mensaje indicado en
        el argumento error_text.

        Argumentos:
            error_text: String con el mensaje de error que se le mostrará al
                        usuario.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Error")
        msg.setIcon(QtGui.QMessageBox.Critical)
        msg.setText(error_text)
        msg.exec_()

    @staticmethod
    def show_info_message(info_text):
        """
        Muestra una ventana emergente de información con el mensaje indicado en
        el argumento info_text.

        Argumentos:
            info_text: String con el mensaje que se le mostrará al usuario.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Información")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(info_text)
        msg.exec_()

    @staticmethod
    def confirm_operation_message(info_text):
        """
        Muestra una ventana emergente de advertencia para confirmar que el
        usuario desea continuar con la operación.

        Argumentos:
            info_text: String con el mensaje que se le mostrará al usuario.

        Devuelve:
            True si el usuario hace click en Ok; False en caso contrario.
        """
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(u"Advertencia")
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText(info_text)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        retval = msg.exec_()

        if (retval == QtGui.QMessageBox.Ok):
            return True
        else:
            return False

    @staticmethod
    def open_file_dialog(parent, selectedFilter=""):
        """
        Muestra una ventana de diálogo para seleccionar el fichero a abrir.

        Argumentos:
            parent: QWidget padre.
            selectedFilter: (opcional) Filtro con la extensión de los archivos
                            que se mostrarán.

        Devuelve:
            String con la ruta del fichero seleccionado.
        """
        return unicode(QtGui.QFileDialog.getOpenFileName(
            parent, u"Abrir fichero", ".", selectedFilter))


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no debería ser ejecutado", file=sys.stderr)
