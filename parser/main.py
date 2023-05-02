# -*- coding: utf-8 -*-

import os
try:
    import requests
except:
    os.system("py -m pip install requests")
finally:
    import requests

import html

URL = "http://apppruebaetsi.uhu.es/simplesaml/app_gestion_cursos/Teoria/xml/plantilla_xml_horarios_2.php?tit=G26&year=2021&cuatr=1"
FICHERO = "Datos.txt"
ASIGNATURA_TAG = "<Asignatura "
ASIGNATURA_TAG_CLOSE = "</Asignatura>"


class ATRIBUTES:
    CODIGO: str = "codigo"
    NOMBRE: str = "nombre"
    TITULACION: str = "titulacion"
    ITINERARIO: str = "itinerario"
    CURSO: str = "curso"
    NOMBREINGLES: str = "nombreingles"
    TIPO: str = "tipo"
    TIMES: str = "times"

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

class Asignatura:
    atributos: dict[str, str]

    def __init__(self, line: str):
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip(ASIGNATURA_TAG).split("\" ")
        self.atributos = {}
                
        with open(FICHERO, "a") as file:
            for a in atributes:
                data = a.strip().split("=\"")
                data[1] = html.unescape(data[1])

                self.atributos[data[0]] = data[1]

                data: str = f"{data[0]}  {data[1]}\n"
                file.write(data)
            file.write("\n\n")

    def set(self, atributo: ATRIBUTES, value):
        self.atributos[atributo] = value
        return self
    
    def get(self, atributo: ATRIBUTES) -> str:
        return self.atributos[atributo]

def main():
    response = requests.get(URL)
    data = response.text
    asignaturas: list[Asignatura] = []

    if os.path.exists(FICHERO):
        f = open(FICHERO, "w")
        f.close()

    times_asignatura: bool = False
    contador: int = 0
    for line in data.split("\n"):
        if ASIGNATURA_TAG_CLOSE in line:
            asignaturas.append(asignaturas.pop().set(ATRIBUTES.TIMES, str(contador)))
            contador = 0
            times_asignatura = False
        elif times_asignatura:
            contador += 1
        elif ASIGNATURA_TAG in line:
            asignaturas.append(Asignatura(line))
            times_asignatura = True

    prolog_data: list[PrologSubjectData] = []

    for asignatura in asignaturas:
        aula = "Gen"
        profesor = "Prof"
        nombre = asignatura.get(ATRIBUTES.NOMBRE).replace(" ", "_")
        times = asignatura.get(ATRIBUTES.TIMES)
        prolog_data.append(PrologSubjectData(aula, nombre, profesor, times))


    with open("reqs_uhu.pl", "w", encoding="utf8") as file:
        for pd in prolog_data:
            file.write((str(pd)+"\n"))

    for data in prolog_data:
        print(f"{data}")


if __name__ =="__main__":
    main()