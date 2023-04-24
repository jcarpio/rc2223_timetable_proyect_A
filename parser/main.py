# -*- coding: utf-8 -*-

import requests
import os
import html

URL = "http://apppruebaetsi.uhu.es/simplesaml/app_gestion_cursos/Teoria/xml/plantilla_xml_horarios_2.php?tit=G26&year=2021&cuatr=1"
FICHERO = "Datos.txt"
ASIGNATURA_TAG = "<Asignatura "


class ATRIBUTES:
    CODIGO: str = "codigo"
    NOMBRE: str = "nombre"
    TITULACION: str = "titulacion"
    ITINERARIO: str = "itinerario"
    CURSO: str = "curso"
    NOMBREINGLES: str = "nombreingles"
    TIPO: str = "tipo"


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

def main():
    response = requests.get(URL)
    data = response.text
    asignaturas: list[Asignatura] = []

    if os.path.exists(FICHERO):
        f = open(FICHERO, "w")
        f.close()

    for line in data.split("\n"):
        if ASIGNATURA_TAG in line:
            asignaturas.append(Asignatura(line))

    primero = [x.atributos.get(ATRIBUTES.NOMBRE) for x in asignaturas if x.atributos.get(ATRIBUTES.CURSO) == "1"]
    print(f"{primero}")


if __name__ =="__main__":
    main()