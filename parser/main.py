# -*- coding: utf-8 -*-

import os
try:
    import requests
    from unidecode import unidecode
except:
    os.system("py -m pip install requests")
    os.system("py -m pip install Unidecode")
finally:
    import requests
    from unidecode import unidecode

import html
from enum import Enum

URL = "http://apppruebaetsi.uhu.es/simplesaml/app_gestion_cursos/Teoria/xml/plantilla_xml_horarios_2.php?tit=G26&year=2022&cuatr=1"
FICHERO = "Datos.txt"
FICHERO_REQUISITOS = "req_pro.pl"
ASIGNATURA_TAG = "<Asignatura "
ASIGNATURA_TAG_CLOSE = "</Asignatura>"
AULA_TAG = "<Aulas_gr "
HORARIO_TAG = "<Horario_t "

ASIGNATURA_PROFESORES: dict[str, list[str]] = {
    "Fundamentos de Análisis de Algoritmos": ["Teresa Santos", "Fco. J. Baquero"],
    "Metodología de la Programación": ["Antonio A. Márquez", "Fco. J. Baquero", "Mario Márquez"],
    "Inteligencia Artificial": ["Nacho"],
    "Algorítmica y Modelos de Computación": ["Antonio A. Márquez", "Francisco J. Baquero"],
    "Realidad Virtual": ["Fco. Moreno"],
    "Sistemas Inteligentes": ["Gonzalo A. Aranda", "Antonio Palanco"],
    "Procesadores de Lenguajes": ["Fco. Moreno"],
    "Representación del Conocimiento": ["José Carpio"],
    "Representación del Conocimiento (inglés)": ["José Carpio"],
    "Modelos Avanzados de Computación": ["Fco. Moreno", "Antonio Palanco"],
    "Aprendizaje Automático": ["Gonzalo Aranda", "Miguel A. Rodríguez"],
    "Aprendizaje Automático (inglés)": ["Gonzalo Aranda", "Miguel A. Rodríguez"]
}

"""
                   Inf1Turno_1Cua1
room_ingles(aula, "               ", matematicas_i, 2)


"""

def fix_string(text: str) -> str:
    return unidecode(html.unescape(text))   \
    .replace(" ", "_")  \
    .replace(",", "")   \
    .replace(".", "_")

class PrologInglesSubject:

    def __init__(self, aula, turno, asig_esp, times):
        self.aula: str = aula
        self.turno: str = turno
        self.asig_esp: str = asig_esp
        self.times: str = times

    def __str__(self) -> str:
        return f"room_ingles({self.aula},'{self.turno}',{self.asig_esp.lower()},{self.times})"

class PrologSubjectData:
    # class_subject_teacher_times('1a', ph, fiz1, 2).
    #                              ^     ^    ^   ^
    #                            Aula  Asig  Prof Veces/semana



    def __init__(self, aula, asignatura, profesor, times):
        self.aula = aula
        self.asignatura = asignatura
        self.profesor = profesor
        self.times = times

    def __str__(self) -> str:
        return f"class_subject_teacher_times('{self.aula}', {fix_string(self.asignatura.lower())}, {fix_string(self.profesor.lower())}, {self.times})"


class AulasAtributes(str, Enum):
    TITULACION = "Titulacion"
    CURSO = "Curso"
    CUATRIMESTRE = "cuatrimestre"
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
    CUATRIMESTRE = "cuatrimestre"


class Aula:
    atributos: dict[str, str]

    def __init__(self, line: str):
        self.atributos = {}
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(AULA_TAG).split("\" ")
        self.atributos = {data.strip().split("=\"")[0]:  fix_string(data.strip().split("=\"")[1]) for data in atributes}


class Hora:
    atributos: dict[str, str]

    def __init__(self, line: str):
        self.atributos = {}
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(HORARIO_TAG).split("\" ")
        self.atributos = {data.strip().split("=\"")[0]: fix_string(data.strip().split("=\"")[1]) for data in atributes}

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
        self.atributos = {data.strip().split("=\"")[0]: fix_string(data.strip().split("=\"")[1]) for data in atributes}

    def set(self, atributo: str, value: str) -> "Asignatura":
        self.atributos[atributo] = value
        return self
    
    def get(self, atributo: str) -> str:
        attr: (str | None) = self.atributos.get(atributo)
        if attr is not  None:
            return attr
        return  ""

    def get_aula_ingles(self) -> str:
        for hora in self.horas:
            if hora.get(HoraAtributes.TURNO) == "Ingles":
                return hora.get(HoraAtributes.AULA)
        return ""

    def get_cuatri(self) -> str:
        try:
            return self.horas[0].get(HoraAtributes.CUATRIMESTRE)
        except IndexError:
            return " "

def main():
    response = requests.get(URL)
    data = response.text
    asignaturas: list[Asignatura] = []
    aulas: list[Aula] = []

    if os.path.exists(FICHERO):
        f = open(FICHERO, "w")
        f.close()

    times_asignatura: bool = False
    for line in data.split("\n"):
        if AULA_TAG in line:
            aulas.append(Aula(line))

        if ASIGNATURA_TAG_CLOSE in line:
            times_asignatura = False
        elif ASIGNATURA_TAG in line:
            asignaturas.append(Asignatura(line))
            times_asignatura = True
        elif times_asignatura:
            asignaturas[-1].horas.append(Hora(line))

    prolog_data: list[PrologSubjectData] = []
    prolog_data_asig_ingles: list[PrologInglesSubject] = []

    for asignatura in asignaturas:
       
        turno_times: dict[str, int] = {}
        for hora in asignatura.horas:
            turno = hora.get(HoraAtributes.TURNO)
            if turno in turno_times:
                turno_times[turno] += 1
            else:
                turno_times[turno] = 1

        # FIXME!
        # Si la asignatura no 
        cuatri = asignatura.get_cuatri()[0]


        for turno, veces in turno_times.items():
            nombre_turno = ("Inf"+asignatura.get(AsigAtributes.CURSO)+turno) if turno != "" else "TurnoGenerico"
            nombre_turno += "Cua"+cuatri

            times = veces

            nombre = asignatura.get(AsigAtributes.NOMBRE)
            profesor = "Profesor_"+nombre

            if turno == "Turno 2" or turno == "Turno 4":
                profesor += "_tarde"
                
            if turno == "Ingles":
                nombre_turno = nombre_turno.replace("Ingles","Turno_1")
                # aula_ingles = asignatura.get_aula_ingles()
                aula_ingles = "r1"
                ingles_subject = PrologInglesSubject(aula_ingles, nombre_turno, nombre, veces)
                prolog_data_asig_ingles.append(ingles_subject)
                
            else:
                prolog_data.append(PrologSubjectData(nombre_turno, nombre, profesor, times))


    with open(FICHERO_REQUISITOS, "w", encoding="utf8") as file:

        slots = "slots_per_week(40).\nslots_per_day(8).\n\n"
        file.write(slots)
        curso = None
        for pd in prolog_data:
            curso_act: str = [x.get(AsigAtributes.CURSO) for x in asignaturas if x.get(AsigAtributes.NOMBRE) == pd.asignatura.removesuffix("_Ingles")][0]
            if curso != curso_act:
                file.write(f"\n\n%########## CURSO {curso_act} ################%\n\n")
                curso = curso_act

            file.write((str(pd)+".\n"))

        file.write("\n\n\n\n")

        for subject_ingles in prolog_data_asig_ingles:
            file.write( str(subject_ingles)+".\n" )

    for data in prolog_data:
        print(f"{data}")


if __name__ =="__main__":
    main()