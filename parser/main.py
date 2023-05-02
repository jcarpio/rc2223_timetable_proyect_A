# -*- coding: utf-8 -*-

import os
try:
    import requests
except:
    os.system("py -m pip install requests")
finally:
    import requests

import html
from enum import Enum

URL = "http://apppruebaetsi.uhu.es/simplesaml/app_gestion_cursos/Teoria/xml/plantilla_xml_horarios_2.php?tit=G26&year=2021&cuatr=1"
FICHERO = "Datos.txt"
FICHERO_REQUISITOS = "req_pro.pl"
ASIGNATURA_TAG = "<Asignatura "
ASIGNATURA_TAG_CLOSE = "</Asignatura>"
AULA_TAG = "<Aulas_gr "
HORARIO_TAG = "<Horario_t "

class PrologSubjectData:
    # class_subject_teacher_times('1a', ph, fiz1, 2).
    #                              ^     ^    ^   ^
    #                            Aula  Asig  Prof Veces/semana

    aula: str
    asignatura: str
    profesor: str
    times: str

    def __init__(self, aula, asignatura, profesor, times):
        self.aula = aula
        self.asignatura = asignatura
        self.profesor = profesor
        self.times = times

    def __str__(self) -> str:
        return f"class_subject_teacher_times('{self.aula}', {self.asignatura}, {self.profesor}, {self.times})"


class AulasAtributes(str, Enum):
    TITULACION = "Titulacion"
    CURSO = "Curso"
    CUATRIMESTRE = "Cuatrimestre"
    TURNO = "Turno"
    AULA = "Aula"


class AsigAtributes(str, Enum):
    CODIGO = "codigo"
    NOMBRE = "nombre"
    TITULACION = "titulacion"
    ITINERARIO = "itinerario"
    CURSO = "curso"
    NOMBREINGLES = "nombreingles"
    TIPO = "tipo"
    TIMES = "times"


class HoraAtributes(str, Enum):
    AULA = "Aula"
    SEMANAS = "Semanas"
    DIA = "Dia"
    HORA_I = "Hora_i"
    HORA_F = "Hora_f"
    TURNO = "Turno"
    CUATRIMESTRE = "Cuatrimestre"


class Aula:
    atributos: dict[str, str]

    def __init__(self, line: str):
        self.atributos = {}
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(AULA_TAG).split("\" ")
        self.atributos = {data.strip().split("=\"")[0]: html.unescape(data.strip().split("=\"")[1]) for data in atributes}


class Hora:
    atributos: dict[str, str]

    def __init__(self, line: str):
        self.atributos = {}
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(HORARIO_TAG).split("\" ")
        self.atributos = {data.strip().split("=\"")[0]: html.unescape(data.strip().split("=\"")[1]) for data in atributes}

    def get(self, atributo: HoraAtributes) -> str:
        attr: (str | None) = self.atributos.get(atributo)
        if attr is not  None:
            return attr
        return  ""


class Asignatura:
    atributos: dict[str, str]
    horas: list[Hora]

    def __init__(self, line: str):
        self.atributos = {}
        self.horas = []

        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(ASIGNATURA_TAG).split("\" ")
        self.atributos = {data.strip().split("=\"")[0]: html.unescape(data.strip().split("=\"")[1]) for data in atributes}

    def set(self, atributo: str, value):
        self.atributos[atributo] = value
        return self
    
    def get(self, atributo: str) -> str:
        attr: (str | None) = self.atributos.get(atributo)
        if attr is not  None:
            return attr
        return  ""


def main():
    response = requests.get(URL)
    data = response.text
    asignaturas: list[Asignatura] = []
    aulas: list[Aula] = []

    if os.path.exists(FICHERO):
        f = open(FICHERO, "w")
        f.close()

    times_asignatura: bool = False
    contador: int = 0
    for line in data.split("\n"):
        if AULA_TAG in line:
            aulas.append(Aula(line))

        if ASIGNATURA_TAG_CLOSE in line:
            times_asignatura = False
        elif ASIGNATURA_TAG in line:
            asignaturas.append(Asignatura(line))
            times_asignatura = True
        elif times_asignatura:
            asignaturas[(len(asignaturas)-1)].horas.append(Hora(line))

    prolog_data: list[PrologSubjectData] = []

    for asignatura in asignaturas:
        """ 
            Cortesia de chatGPT

            Esto crea un diccionario que contiene como clave las aulas en el que
            se imparte la asignatura y como valor las veces que se imparte en ese
            aula.

            Este codigo es equivalente:

                for hora in horas_clase:
                    aula = hora.get(HoraAtributes.AULA)
                    if aula in aulas:
                        aulas[aula] += 1
                    else:
                        aulas[aula] = 1

        """
        aulas_times: dict[str, int] = {hora.get(HoraAtributes.AULA): sum(1 for h in asignatura.horas if h.get(HoraAtributes.AULA) == hora.get(HoraAtributes.AULA)) for hora in asignatura.horas}

        for aula, hora in aulas_times.items():
            aula = aula if aula != "" else "Aula_Generica"
            profesor = "Profesor_Generico"
            nombre = asignatura.get(AsigAtributes.NOMBRE).replace(" ", "_")
            times = hora
            prolog_data.append(PrologSubjectData(aula, nombre, profesor, times))


    with open(FICHERO_REQUISITOS, "w", encoding="utf8") as file:
        for pd in prolog_data:
            file.write((str(pd)+"\n"))

    for data in prolog_data:
        print(f"{data}")


if __name__ =="__main__":
    main()