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
import json


class ValoradorModel():
    """
    Clase con el modelo del valorador.
    """
    pass


class Caso(object):
    """
    Representa un caso (contiene los criterios a valorar).

    Atributos/propiedades:
        nombre: String con el nombre del caso.
        descripcion: String con la descripción del caso.
        explicacion: String con la explicación del resultado de la valoración.
        criterios: Los criterios a evaluar (array con objectos de la clase
                   Criterio).
    """

    def __init__(self):
        self.__nombre = None
        self.__descripcion = None
        self.__explicacion = None
        self.__criterios = []

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
    def explicacion(self):
        """
        Getter de la propiedad explicacion.
        """
        return self.__explicacion

    @property
    def criterios(self):
        """
        Getter de la propiedad criterios.
        """
        return self.__criterios

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return "Nombre: " + str(self.nombre) + \
               "\nDescripcion: " + str(self.descripcion) + \
               "\nNumero de criterios: " + str(len(self.criterios))

    def load_from_JSON_file(self, filePath):
        """
        Carga el caso y todos sus criterios a partir de un fichero JSON con el
        formato adecuado.

        Argumentos:
            filePath: Ruta hacia el fichero.

        Excepciones:
            IOError: El fichero JSON no tiene el formato correcto.
        """
        # Primero reinicializamos el caso
        self.__full_reset()

        parsed_json = self.__parse_JSON_file(filePath)

        try:
            # Cargamos los datos del caso
            self.__nombre = parsed_json['caso']['nombre']
            self.__descripcion = parsed_json['caso']['descripcion']

            # Cargamos los datos de cada criterio dependiendo de su tipo
            for criterio in parsed_json['caso']['criterios']:
                if (criterio['tipo'] == "Booleano"):
                    x = CriterioBooleano(criterio['nombre'],
                                         criterio['descripcion'])
                    self.criterios.append(x)

                elif (criterio['tipo'] == "Porcentaje"):
                    x = CriterioPorcentaje(criterio['nombre'],
                                           criterio['descripcion'],
                                           float(criterio['valor_minimo']),
                                           float(criterio['valor_maximo']))
                    self.criterios.append(x)

                elif (criterio['tipo'] == "Entero"):
                    x = CriterioEntero(criterio['nombre'],
                                       criterio['descripcion'],
                                       int(criterio['valor_minimo']),
                                       int(criterio['valor_maximo']))
                    self.criterios.append(x)
        except:
            self.__full_reset()
            raise IOError("El fichero JSON no tiene el formato correcto")

        # Comprobamos que todos los criterios se han cargado
        if (len(self.criterios) != len(parsed_json['caso']['criterios'])):
            self.__full_reset()
            raise IOError("El fichero JSON no tiene el formato correcto")

    def __parse_JSON_file(self, filePath):
        """
        Lee y parsea un fichero JSON.

        Argumentos:
            filePath: Ruta hacia el fichero.

        Excepciones:
            IOError: Error al abrir el fichero JSON.
        """
        try:
            with open(filePath, 'r') as f:
                parsed_json = json.load(f)
                f.close()
        except:
            raise IOError("Error al abrir el fichero JSON")

        return parsed_json

    def __full_reset(self):
        """
        Reinicializa el caso completamente (elimina todo, incluido los
        criterios).
        """
        self.__nombre = None
        self.__descripcion = None
        self.__criterios = []
        self.__explicacion = None

    def reset(self):
        """
        Reinicializa el caso (elimina la explicación y el valor de los
        criterios).
        """
        self.__explicacion = None

        for criterio in self.criterios:
            criterio.reset()

    def valorar(self):
        """
        Evalúa todos los criterios, devuelve el resultado de la valoración y
        actualiza el atributo explicacion con la explicación del resultado.
        """
        result = True
        self.__explicacion = ""

        for criterio in self.criterios:
            self.__explicacion += str(criterio)
            self.__explicacion += "\n==> Valor introducido: " + \
                str(criterio.valor)

            if(criterio.valorar()):
                self.__explicacion += "\n==> Valoracion: APROBADO\n\n"
            else:
                self.__explicacion += "\n==> Valoracion: RECHAZADO\n\n"
                result = False

        return result


class Criterio(object):
    """
    Clase base para representar los criterios.

    Esta clase no debe ser instanciada; es solo una interfaz (clase base
    abstracta).

    Argumentos:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio). El criterio será evaluado en base a este
               valor.
    """

    def __init__(self, nombre, descripcion):
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

        Argumentos:
            valor: El valor del criterio.
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

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Deberá ser implementado por la clase heredera.
        """
        raise NotImplementedError

    def reset(self):
        """
        Reinicializa el valor del criterio.
        """
        self.__valor = None


class CriterioBooleano(Criterio):
    """
    Representa un criterio del tipo booleano.

    Argumentos:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio). El criterio será evaluado en base a este
               valor.
    """

    def __init__(self, nombre, descripcion):
        super(CriterioBooleano, self).__init__(nombre, descripcion)

    @Criterio.valor.setter
    def valor(self, valor):
        """
        Setter de la propierdad valor.

        Argumentos:
            valor: El valor del criterio.

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

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El criterio debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError("El criterio debe tener un valor asignado")

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
        descripcion: String con la descripción del criterio.

    Excepciones:
        ValueError: El argumento valor_minimo debe estar entre 0 y 1.
        ValueError: El argumento valor_maximo debe estar entre 0 y 1.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio). El criterio será evaluado en base a este
               valor.
        valor_minimo: Porcentaje mínimo necesario para evaluar el criterio como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el criterio como
                      True.
    """

    def __init__(self, nombre, descripcion, valor_minimo, valor_maximo):
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

        Argumentos:
            valor: El valor del criterio.

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

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El criterio debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError("El criterio debe tener un valor asignado")

        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


class CriterioEntero(Criterio):
    """
    Representa un criterio del tipo Entero.

    Argumentos:
        nombre: String con el nombre del criterio.
        valor_minimo: Valor mínimo necesario para evaluar el criterio como True.
        valor_maximo: Valor máximo posible para evaluar el criterio como True.
        descripcion: String con la descripción del criterio.

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

    def __init__(self, nombre, descripcion, valor_minimo, valor_maximo):
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

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El criterio debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError("El criterio debe tener un valor asignado")

        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


if __name__ == "__main__":
    """
    En caso de que intentemos ejecutar este módulo.
    """
    print("Este módulo no debería ser ejecutado", file=sys.stderr)

    # TODO: Quitar todo esto de aquí

    caso = Caso()

    caso.load_from_JSON_file("casos-de-prueba/ejemplo.json")

    caso.criterios[0].valor = True
    caso.criterios[1].valor = 0.5
    caso.criterios[2].valor = 10000

    print("\n")
    print(caso)

    # print("\n")
    # for criterio in caso.criterios:
    #     print("---------------------------")
    #     print(criterio)
    #     print("VALOR: " + str(criterio.valor))
    #     print("VALORACION: " + str(criterio.valorar()))
    # print("---------------------------")

    print("\n")
    print("VALORACIÓN CASO: " + str(caso.valorar()))

    print("\n")
    print(caso.explicacion)
