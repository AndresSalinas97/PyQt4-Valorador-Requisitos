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
        self._nombre = None
        self._descripcion = None
        self._explicacion = None
        self._criterios = []

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
    def criterios(self):
        """
        Getter de la propiedad criterios.
        """
        return self._criterios

    def __str__(self):
        """
        Devuelve la representación en string del objecto (para usar con print).
        """
        return (u"- Nombre: " + unicode(self.nombre) +
                u"\n- Descripción: " + unicode(self.descripcion) +
                u"\n- Número de criterios: " + str(len(self.criterios)))

    def load_from_JSON_file(self, file_path):
        """
        Carga el caso y todos sus criterios a partir de un fichero JSON con el
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

            # Cargamos los datos de cada criterio dependiendo de su tipo
            for criterio in parsed_json['caso']['criterios']:
                if (criterio['tipo'] == "Booleano"):
                    x = CriterioBooleano(criterio['nombre'],
                                         criterio['descripcion'],
                                         criterio['valor_deseado'])
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
            self._full_reset()
            raise IOError(u"El fichero JSON no tiene el formato correcto")

        # Comprobamos que todos los criterios se han cargado
        if (len(self.criterios) != len(parsed_json['caso']['criterios'])):
            self._full_reset()
            raise IOError(u"El fichero JSON no tiene el formato correcto")

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
            raise IOError(u"Error al abrir el fichero JSON")

        return parsed_json

    def _full_reset(self):
        """
        Reinicializa el caso completamente (elimina todo, incluido los
        criterios).
        """
        self._nombre = None
        self._descripcion = None
        self._criterios = []
        self._explicacion = None

    def reset(self):
        """
        Reinicializa el caso (elimina la explicación y el valor de los
        criterios).
        """
        self._explicacion = None

        for criterio in self.criterios:
            criterio.reset()

    def valorar(self):
        """
        Evalúa todos los criterios, devuelve el resultado de la valoración y
        actualiza el atributo explicacion con la explicación del resultado.
        """
        result = True
        self._explicacion = u""
        i = 1
        n_criterios = len(self.criterios)

        for criterio in self.criterios:
            self._explicacion += (u"Criterio " + str(i) + u"/" + str(n_criterios)
                                  + u"\n" + unicode(criterio)
                                  + u"\n==> Valor introducido: "
                                  + unicode(criterio.valor))

            if(criterio.valorar()):
                self._explicacion += u"\n==> Valoración: APROBADO\n\n"
            else:
                self._explicacion += u"\n==> Valoración: RECHAZADO\n\n"
                result = False

            i += 1

        return result


class Criterio(object):
    """
    Clase base para representar los criterios.

    Esta clase no debe ser instanciada; es solo una interfaz (clase base
    abstracta).

    Argumentos constructor:
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
        return (u"- Nombre: " + unicode(self.nombre) +
                u"\n- Descripción: " + unicode(self.descripcion) +
                u"\n- Tipo: " + unicode(self.tipo))

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
        self._valor = None


class CriterioBooleano(Criterio):
    """
    Representa un criterio del tipo booleano.

    Argumentos constructor:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        valor_deseado: Valor que el criterio debe tener para ser evaluado como
                       True.

    Excepciones constructor:
        TypeError: El argumento valor_deseado debe ser un booleano.

    Atributos/Propiedades:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        tipo: String con el tipo del criterio (Booleano, Porcentaje o Entero).
        valor: Valor actualmente asignado al criterio (su tipo dependerá del
               tipo de criterio). El criterio será evaluado en base a este
               valor.
        valor_deseado: Valor que el criterio debe tener para ser evaluado como
                       True.
    """

    def __init__(self, nombre, descripcion, valor_deseado):
        super(CriterioBooleano, self).__init__(nombre, descripcion)

        if (not isinstance(valor_deseado, bool)):
            raise TypeError(u"El valor introducido debe ser un booleano")

        self._valor_deseado = valor_deseado

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
        return (super(CriterioBooleano, self).__str__() +
                u"\n- Valor deseado: " + str(self.valor_deseado))

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El criterio debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError(u"El criterio debe tener un valor asignado")

        return (self.valor == self.valor_deseado)


class CriterioPorcentaje(Criterio):
    """
    Representa un criterio del tipo Porcentaje.

    Argumentos constructor:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        valor_minimo: Porcentaje mínimo necesario para evaluar el criterio como
                      True.
        valor_maximo: Porcentaje máximo posible para evaluar el criterio como
                      True.

    Excepciones constructor:
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
            raise ValueError(u"El valor introducido debe estar entre 0 y 1")
        if(valor_maximo < 0 or valor_maximo > 1):
            raise ValueError(u"El valor introducido debe estar entre 0 y 1")

        self._valor_minimo = valor_minimo
        self._valor_maximo = valor_maximo

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
            raise ValueError(u"El valor introducido debe estar entre 0 y 1")

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
        return (super(CriterioPorcentaje, self).__str__() +
                u"\n- Valor mínimo: " + str(self.valor_minimo) +
                u"\n- Valor máximo: " + str(self.valor_maximo))

    def valorar(self):
        """
        Evalúa el criterio y devuelve True o False según corresponda.

        Excepciones:
            RuntimeError: El criterio debe tener un valor asignado antes de
                          poder ser valorado.
        """
        if(self.valor is None):
            raise RuntimeError(u"El criterio debe tener un valor asignado")

        return (self.valor >= self.valor_minimo and
                self.valor <= self.valor_maximo)


class CriterioEntero(Criterio):
    """
    Representa un criterio del tipo Entero.

    Argumentos constructor:
        nombre: String con el nombre del criterio.
        descripcion: String con la descripción del criterio.
        valor_minimo: Valor mínimo necesario para evaluar el criterio como True.
        valor_maximo: Valor máximo posible para evaluar el criterio como True.

    Excepciones constructor:
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
            raise TypeError(u"El valor introducido debe ser un entero")
        if (not isinstance(valor_maximo, int)):
            raise TypeError(u"El valor introducido debe ser un entero")

        self._valor_minimo = valor_minimo
        self._valor_maximo = valor_maximo

    @Criterio.valor.setter
    def valor(self, valor):
        """
        Setter de la propiedad valor.

        Excepciones:
            TypeError: El argumento valor debe ser un entero.
        """
        if (not isinstance(valor, int)):
            raise TypeError(u"El valor introducido debe ser un entero")

        self._valor = valor

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
        return (super(CriterioEntero, self).__str__() +
                u"\n- Valor mínimo: " + str(self.valor_minimo) +
                u"\n- Valor máximo: " + str(self.valor_maximo))

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
    print(u"Este módulo no debería ser ejecutado", file=sys.stderr)

    # TODO: Eliminar todo esto cuando acabemos con las pruebas

    caso = Caso()

    caso.load_from_JSON_file("casos-de-prueba/ejemplo.json")

    caso.criterios[0].valor = True
    caso.criterios[1].valor = 0.5
    caso.criterios[2].valor = 10000

    print("\n")
    print(unicode(caso))

    print("\n")
    print("VALORACIÓN CASO: " + str(caso.valorar()))

    print("\n")
    print(caso.explicacion)
