#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el modelo del valorador.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
from valorador_view import ValoradorMessageBoxes
import sys
import os
import json


class ValoradorModel():
    """
    Clase con el modelo del valorador.

    Atributos/Propiedades:
        caso: El caso a valorar.
        opened_file_path: String con la ruta del fichero de caso abierto.
    """

    def __init__(self):
        self.caso = Caso()
        self.opened_file_path = ""


class Caso(object):
    """
    Representa un caso (contiene los requisitos a valorar).

    Atributos/Propiedades:
        nombre: String con el nombre del caso.
        descripcion: String con la descripción del caso.
        explicacion: String con la explicación del resultado de la valoración.
        requisitos: Los requisitos a evaluar (array con objectos de la clase
                   Requisito).
    """

    def __init__(self):
        self._nombre = ""
        self._descripcion = ""
        self._explicacion = ""
        self._requisitos = []

    @property
    def nombre(self):
        """
        Getter de la propiedad nombre.
        """
        return self._nombre

    @property
    def descripcion(self):
        """
        Getter de la propiedad descripcion.
        """
        return self._descripcion

    @property
    def explicacion(self):
        """
        Getter de la propiedad explicacion.
        """
        return self._explicacion

    @property
    def requisitos(self):
        """
        Getter de la propiedad requisitos.
        """
        return self._requisitos

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (u"- NOMBRE: " + unicode(self.nombre) +
                u"\n- DESCRIPCIÓN: " + unicode(self.descripcion) +
                u"\n- NÚMERO DE REQUISITOS: " + str(len(self.requisitos)))

    def load_from_JSON_file(self, file_path):
        """
        Carga el caso y todos sus requisitos a partir de un fichero JSON con el
        formato adecuado.

        Argumentos:
            file_path: Ruta hacia el fichero.

        Excepciones:
            IOError: El fichero JSON no tiene el formato correcto.
        """
        # Primero reinicializamos el caso
        self._full_reset()

        parsed_json = self._parse_JSON_file(file_path)

        try:
            # Cargamos los datos del caso
            self._nombre = parsed_json['caso']['nombre']
            self._descripcion = parsed_json['caso']['descripcion']

            # Cargamos los datos de cada requisito dependiendo de su tipo
            for requisito in parsed_json['caso']['requisitos']:
                if (requisito['tipo'] == "Booleano"):
                    x = RequisitoBooleano(requisito['nombre'],
                                          requisito['descripcion'],
                                          requisito['valor_deseado'])
                    self.requisitos.append(x)

                elif (requisito['tipo'] == "Porcentaje"):
                    x = RequisitoPorcentaje(requisito['nombre'],
                                            requisito['descripcion'],
                                            float(requisito['valor_minimo']),
                                            float(requisito['valor_maximo']))
                    self.requisitos.append(x)

                elif (requisito['tipo'] == "Numero"):
                    x = RequisitoNumero(requisito['nombre'],
                                        requisito['descripcion'],
                                        float(requisito['valor_minimo']),
                                        float(requisito['valor_maximo']))
                    self.requisitos.append(x)
        except:
            self._full_reset()
            raise IOError(u"El fichero JSON no tiene el formato correcto!")

        # Comprobamos que todos los requisitos se han cargado
        if (len(self.requisitos) != len(parsed_json['caso']['requisitos'])):
            self._full_reset()
            raise IOError(u"El fichero JSON no tiene el formato correcto!")

    def _parse_JSON_file(self, file_path):
        """
        Lee y parsea un fichero JSON.

        Argumentos:
            file_path: Ruta hacia el fichero.

        Excepciones:
            IOError: Error al abrir el fichero JSON.
        """
        try:
            with open(file_path, 'r') as f:
                parsed_json = json.load(f)
                f.close()
        except:
            raise IOError(u"Error al abrir el fichero JSON!")

        return parsed_json

    def _full_reset(self):
        """
        Reinicializa el caso completamente (elimina todo, incluido los
        requisitos).
        """
        self._nombre = ""
        self._descripcion = ""
        self._requisitos = []
        self._explicacion = ""

    def reset(self):
        """
        Reinicializa el caso (elimina la explicación y el valor de los
        requisitos).
        """
        self._explicacion = ""

        for requisito in self.requisitos:
            requisito.reset()

    def valorar(self):
        """
        Evalúa todos los requisitos, devuelve el resultado de la valoración y
        actualiza el atributo explicacion con la explicación del resultado.

        Excepciones:
            RuntimeError: El caso debe tener al menos un requisito para poder ser
            valorado.
        """
        n_requisitos = len(self.requisitos)

        if(n_requisitos == 0):
            raise RuntimeError(
                u"El caso debe tener al menos un requisito para poder ser "
                "valorado!")

        result = True
        self._explicacion = u""
        i = 1

        for requisito in self.requisitos:
            self._explicacion += (
                u"*** Requisito " + str(i) + u"/" +
                str(n_requisitos) + u" ***\n"
                + unicode(requisito)
                + u"\n* VALOR INTRODUCIDO: " + unicode(requisito.valor))

            if(requisito.valorar()):
                self._explicacion += u"\n===> APROBADO <===\n\n"
            else:
                self._explicacion += u"\n===> RECHAZADO <===\n\n"
                result = False

            i += 1

        return result


class Requisito(object):
    """
    Clase base para representar los requisitos.

    Esta clase no debe ser instanciada; es solo una interfaz (clase base
    abstracta).

    Argumentos constructor:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.

    Atributos/Propiedades:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        tipo: String con el tipo del requisito (Booleano, Porcentaje o Numero).
        valor: Valor actualmente asignado al requisito (su tipo dependerá del
               tipo de requisito). El requisito será evaluado en base a este
               valor.
    """

    def __init__(self, nombre, descripcion):
        self._nombre = nombre
        self._descripcion = descripcion
        self._valor = None

    @property
    def nombre(self):
        """
        Getter de la propiedad nombre.
        """
        return self._nombre

    @property
    def descripcion(self):
        """
        Getter de la propiedad descripcion.
        """
        return self._descripcion

    @property
    def valor(self):
        """
        Getter de la propiedad valor.
        """
        return self._valor

    @valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Deberá ser implementado por la clase heredera.

        Argumentos:
            valor: El valor del requisito.
        """
        raise NotImplementedError

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.

        Deberá ser implementado por la clase heredera.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (u"- NOMBRE: " + unicode(self.nombre) +
                u"\n- DESCRIPCIÓN: " + unicode(self.descripcion) +
                u"\n- TIPO: " + unicode(self.tipo))

    def valorar(self):
        """
        Evalúa el requisito y devuelve True o False según corresponda.

        Deberá ser implementado por la clase heredera.
        """
        raise NotImplementedError

    def reset(self):
        """
        Reinicializa el valor del requisito.
        """
        self._valor = None


class RequisitoBooleano(Requisito):
    """
    Representa un requisito del tipo booleano.

    Argumentos constructor:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        valor_deseado: Valor que el requisito debe tener para ser evaluado como
                       True.

    Excepciones constructor:
        TypeError: El argumento valor_deseado debe ser un booleano.

    Atributos/Propiedades:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        tipo: String con el tipo del requisito ("Booleano").
        valor: Valor actualmente asignado al requisito.
        valor_deseado: Valor que el requisito debe tener para ser evaluado como
                       True.
    """

    def __init__(self, nombre, descripcion, valor_deseado):
        super(RequisitoBooleano, self).__init__(nombre, descripcion)

        if (not isinstance(valor_deseado, bool)):
            raise TypeError(u"El valor introducido debe ser un booleano!")

        self._valor_deseado = valor_deseado

    @Requisito.valor.setter
    def valor(self, valor):
        """
        Setter de la propierdad valor.

        Argumentos:
            valor: El valor del requisito.

        Excepciones:
            TypeError: El argumento valor debe ser un booleano.
        """
        if (not isinstance(valor, bool)):
            raise TypeError("El valor introducido debe ser un booleano!")

        self._valor = valor

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.
        """
        return("Booleano")

    @property
    def valor_deseado(self):
        """
        Getter de la propiedad valor_deseado.
        """
        return self._valor_deseado

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (super(RequisitoBooleano, self).__str__() +
                u"\n- VALOR DESEADO: " + str(self.valor_deseado))

    def valorar(self):
        """
        Evalúa el requisito y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El requisito debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError(u"El requisito \"" + self.nombre +
                               "\" debe tener un valor asignado!")

        return (self.valor == self.valor_deseado)


class RequisitoPorcentaje(Requisito):
    """
    Representa un requisito del tipo Porcentaje.

    Argumentos constructor:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        valor_minimo: Porcentaje mínimo necesario para evaluar el requisito como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el requisito como
                      True.

    Excepciones constructor:
        ValueError: El argumento valor_minimo debe estar entre 0 y 1.
        ValueError: El argumento valor_maximo debe estar entre 0 y 1.

    Atributos/Propiedades:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        tipo: String con el tipo del requisito ("Porcentaje").
        valor: Valor actualmente asignado al requisito.
        valor_minimo: Porcentaje mínimo necesario para evaluar el requisito como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el requisito como
                      True.
    """

    def __init__(self, nombre, descripcion, valor_minimo, valor_maximo):
        super(RequisitoPorcentaje, self).__init__(nombre, descripcion)

        if(valor_minimo < 0 or valor_minimo > 1):
            raise ValueError(
                u"El valor introducido debe ser un número decimal entre 0 y 1!")
        if(valor_maximo < 0 or valor_maximo > 1):
            raise ValueError(
                u"El valor introducido debe ser un número decimal entre 0 y 1!")

        self._valor_minimo = valor_minimo
        self._valor_maximo = valor_maximo

    @Requisito.valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Argumentos:
            valor: El valor del requisito.

        Excepciones:
            ValueError: El argumento valor_minimo debe estar entre 0 y 1.
        """
        if (valor < 0 or valor > 1):
            raise ValueError(
                u"El valor introducido debe ser un número decimal entre 0 y 1!")

        self._valor = valor

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.
        """
        return("Porcentaje")

    @property
    def valor_minimo(self):
        """
        Getter de la propiedad valor_minimo.
        """
        return self._valor_minimo

    @property
    def valor_maximo(self):
        """
        Getter de la propiedad valor_maximo.
        """
        return self._valor_maximo

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (super(RequisitoPorcentaje, self).__str__() +
                u"\n- VALOR MÍNIMO: " + str(self.valor_minimo) +
                u"\n- VALOR MÁXIMO: " + str(self.valor_maximo))

    def valorar(self):
        """
        Evalúa el requisito y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El requisito debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError(u"El requisito \"" + self.nombre +
                               "\" debe tener un valor asignado!")

        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


class RequisitoNumero(Requisito):
    """
    Representa un requisito del tipo Numero.

    Argumentos constructor:
        nombre: String con el nombre del requisito.
        descripcion: String con la descripción del requisito.
        valor_minimo: Valor mínimo necesario para evaluar el requisito como True.
        valor_maximo: Valor máximo posible para evaluar el requisito como True.

    Excepciones constructor:
        TypeError: El argumento valor_minimo debe ser un número.
        TypeError: El argumento valor_maximo debe ser un número.

    Atributos/Propiedades:
        nombre: String con el nombre del requisito.
        tipo: String con el tipo del requisito ("Numero").
        valor: Valor actualmente asignado al requisito
        valor_minimo: Valor mínimo necesario para evaluar el requisito como True.
        valor_maximo: Valor máximo posible para evaluar el requisito como True.
    """

    def __init__(self, nombre, descripcion, valor_minimo, valor_maximo):
        super(RequisitoNumero, self).__init__(nombre, descripcion)

        if (not isinstance(valor_minimo, float)):
            raise TypeError(u"El valor introducido debe ser un número!")
        if (not isinstance(valor_maximo, float)):
            raise TypeError(u"El valor introducido debe ser un número!")

        self._valor_minimo = valor_minimo
        self._valor_maximo = valor_maximo

    @Requisito.valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Excepciones:
            TypeError: El argumento valor debe ser un número.
        """
        if (not isinstance(valor, float)):
            raise TypeError(u"El valor introducido debe ser un número!")

        self._valor = valor

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.
        """
        return("Numero")

    @property
    def valor_minimo(self):
        """
        Getter de la propiedad valor_minimo.
        """
        return self._valor_minimo

    @property
    def valor_maximo(self):
        """
        Getter de la propiedad valor_maximo.
        """
        return self._valor_maximo

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (super(RequisitoNumero, self).__str__() +
                u"\n- VALOR MÍNIMO: " + str(self.valor_minimo) +
                u"\n- VALOR MÁXIMO: " + str(self.valor_maximo))

    def valorar(self):
        """
        Evalúa el requisito y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El requisito debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError(u"El requisito \"" + self.nombre +
                               "\" debe tener un valor asignado!")

        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print(u"Este módulo no debería ser ejecutado", file=sys.stderr)
