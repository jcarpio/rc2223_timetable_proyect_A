# -*- coding: utf-8 -*-

import requests
import os
import html

URL = "http://apppruebaetsi.uhu.es/simplesaml/app_gestion_cursos/Teoria/xml/plantilla_xml_horarios_2.php?tit=G26&year=2021&cuatr=1"
FICHERO = "Datos.txt"
class Asignatura:
    codigo:         str
    nombre:         str
    titulacion:     str
    itinerario:     str
    curso:          str
    nombreingles:   str
    tipo:           str

    def __new__(self, line: str):
        line = line[1:len(line)-2]
        atributes: list[str] = line.strip("<Asignatura ").split("\" ")
                
        with open(FICHERO, "a") as file:
            for a in atributes:
                data = a.strip().split("=\"")
                data: str = f"{data[0]}  {html.unescape(data[1])}\n"
                file.write(data)
            file.write("\n\n")

def main():
    response = requests.get(URL)
    data = response.text

    if os.path.exists(FICHERO):
        f = open(FICHERO, "w")
        f.close()

    for line in data.split("\n"):
        if "<Asignatura" in line:
            a = Asignatura(line)



if __name__ =="__main__":
    main()