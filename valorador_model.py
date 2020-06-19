#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo con el modelo del valorador.

Autor: Andrés Salinas Lima <i52salia@uco.es>.
"""

from __future__ import print_function
from valorador_view import MessageBoxes
import sys
import os


class ValoradorModel():
    """
    Clase con el modelo del valorador.
    """
    pass


class Caso():
    """
    TODO: Documentar
    """

    def __init__(self):
        self.__nombre = None
        self.__descripcion = None
        self.__criterios = []

    def load(self, filePath):
        """
        TODO: Documentar
        """
        pass

    def parse_JSON(self, filePath):
        """
        TODO: Documentar
        """
        pass


class Criterio(object):
    """
    Clase base para representar los criterios.

    Esta clase no debe ser instanciada; es solo una interfaz (clase base
    abstracta).

    Argumentos:
        nombre: String con el nombre del criterio.
        descripcion: (opcional) String con la descripción del criterio.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio).
    """

    def __init__(self, nombre, descripcion=None):
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__valor = None

    @property
    def nombre(self):
        """
        Getter de la propiedad nombre.
        """
        return self.__nombre

    @property
    def descripcion(self):
        """
        Getter de la propiedad descripcion.
        """
        return self.__descripcion

    @property
    def valor(self):
        """
        Getter de la propiedad valor.
        """
        return self.__valor

    @valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Deberá ser implementado por la clase heredera.
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
        return "Nombre: " + str(self.nombre) + \
               "\nDescripcion: " + str(self.descripcion) + \
               "\nTipo: " + str(self.tipo)

    def evaluate(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Deberá ser implementado por la clase heredera.
        """
        raise NotImplementedError


class CriterioBooleano(Criterio):
    """
    Representa un criterio del tipo booleano.

    Argumentos:
        nombre: String con el nombre del criterio.
        descripcion: (opcional) String con la descripción del criterio.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio).
    """

    def __init__(self, nombre, descripcion=None):
        super(CriterioBooleano, self).__init__(nombre, descripcion)

    @Criterio.valor.setter
    def valor(self, valor):
        """
        Setter de la propierdad valor.

        Excepciones:
            TypeError: El argumento valor debe ser un booleano.
        """
        if (not isinstance(valor, bool)):
            raise TypeError("El valor introducido debe ser un booleano")

        self._Criterio__valor = valor

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.
        """
        return("Booleano")

    def evaluate(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.
        """
        return self.valor


class CriterioPorcentaje(Criterio):
    """
    Representa un criterio del tipo Porcentaje.

    Argumentos:
        nombre: String con el nombre del criterio.
        valor_minimo: Porcentaje mínimo necesario para evaluar el criterio como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el criterio como
                      True.
        descripcion: (opcional) String con la descripción del criterio.

    Excepciones:
        ValueError: El argumento valor_minimo debe estar entre 0 y 1.
        ValueError: El argumento valor_maximo debe estar entre 0 y 1.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio).
        valor_minimo: Porcentaje mínimo necesario para evaluar el criterio como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el criterio como
                      True.
    """

    def __init__(self, nombre, valor_minimo, valor_maximo, descripcion=None):
        super(CriterioPorcentaje, self).__init__(nombre, descripcion)

        if(valor_minimo < 0 or valor_minimo > 1):
            raise ValueError("El valor introducido debe estar entre 0 y 1")
        if(valor_maximo < 0 or valor_maximo > 1):
            raise ValueError("El valor introducido debe estar entre 0 y 1")

        self.__valor_minimo = valor_minimo
        self.__valor_maximo = valor_maximo

    @Criterio.valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Excepciones:
            ValueError: El argumento valor_minimo debe estar entre 0 y 1.
        """
        if (valor < 0 or valor > 1):
            raise ValueError("El valor introducido debe estar entre 0 y 1")

        self._Criterio__valor = valor

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
        return self.__valor_minimo

    @property
    def valor_maximo(self):
        """
        Getter de la propiedad valor_maximo.
        """
        return self.__valor_maximo

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return super(CriterioPorcentaje, self).__str__() + \
            "\nValor minimo: " + str(self.valor_minimo) + \
            "\nValor maximo: " + str(self.valor_maximo)

    def evaluate(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.
        """
        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


class CriterioEntero(Criterio):
    """
    Representa un criterio del tipo Entero.

    Argumentos:
        nombre: String con el nombre del criterio.
        valor_minimo: Valor mínimo necesario para evaluar el criterio como True.
        valor_maximo: Valor máximo posible para evaluar el criterio como True.
        descripcion: (opcional) String con la descripción del criterio.

    Excepciones:
        TypeError: El argumento valor_minimo debe ser un entero.
        TypeError: El argumento valor_maximo debe ser un entero.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio).
        valor_minimo: Valor mínimo necesario para evaluar el criterio como True.
        valor_maximo: Valor máximo posible para evaluar el criterio como True.
    """

    def __init__(self, nombre, valor_minimo, valor_maximo, descripcion=None):
        super(CriterioEntero, self).__init__(nombre, descripcion)

        if (not isinstance(valor_minimo, int)):
            raise TypeError("El valor introducido debe ser un entero")
        if (not isinstance(valor_maximo, int)):
            raise TypeError("El valor introducido debe ser un entero")

        self.__valor_minimo = valor_minimo
        self.__valor_maximo = valor_maximo

    @Criterio.valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Excepciones:
            TypeError: El argumento valor debe ser un entero.
        """
        if (not isinstance(valor, int)):
            raise TypeError("El valor introducido debe ser un entero")

        self._Criterio__valor = valor

    @property
    def tipo(self):
        """
        Getter de la propiedad tipo.
        """
        return("Entero")

    @property
    def valor_minimo(self):
        """
        Getter de la propiedad valor_minimo.
        """
        return self.__valor_minimo

    @property
    def valor_maximo(self):
        """
        Getter de la propiedad valor_maximo.
        """
        return self.__valor_maximo

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return super(CriterioEntero, self).__str__() + \
            "\nValor minimo: " + str(self.valor_minimo) + \
            "\nValor maximo: " + str(self.valor_maximo)

    def evaluate(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.
        """
        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    # print("Este módulo no puede ser ejecutado", file=sys.stderr)

    criterios = []

    x = CriterioBooleano("Test booleano", "Descripcion test del Test booleano")
    x.valor = True
    criterios.append(x)

    x = CriterioPorcentaje("Test porcentaje", 0.5, 0.5, "Test")
    x.valor = 0.5
    criterios.append(x)

    x = CriterioEntero("Test entero", 5, 10)
    x.valor = 15
    criterios.append(x)

    for criterio in criterios:
        print("---------------------------")
        print(criterio)
        print("-")
        print("VALOR: " + str(criterio.valor))
        print("VALORACION: " + str(criterio.evaluate()))
    print("---------------------------")
