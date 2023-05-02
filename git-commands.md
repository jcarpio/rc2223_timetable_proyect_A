
## Secuencia de trabajo colaborativo en Github

1. git pull
(actualiza el repositorio local con los últimos cambios, a partir de aquí puedo empezar a trabajar y modificar ficheros)

2. git add .
Esto si añadí ficheros nuevos al proyecto

3. git commit -a -m "<mensaje> <fixed #<issue_number>>"

4. git push


## Más ayuda

git add "archivo"                           -->    Seguimiento del archivo
git add .                                   -->    Seguimiento de todos los archivos a la vez
git status -s                               -->    Informacion de en que estado se encuentran los archivos
git commit -m "version"                     -->    Pasa a repositorio local lo que habia en seguimiento
git reset --hard "codigo_version"           -->    Restaura a la version que desemos (borra hasta esa version)
git commit --amend                          -->    Cambiamos el nombre de la version que esta en el HEAD. (si nos hemos 
                                                   equivocado al escribir la version)

git tag "nombretag" -m "descripcion"        -->    Permite poner un tag a cada version que vayamos subiendo. 
git push --tags                             -->    Permite subir los tags a github.

CONECTAR REPO A GITHUB
--------------------------


git remote add origin "enlace del repo"    -->    Ambos comandos debemos ejecutarlos para crear un vínculo entre 
git push -u origin master


git push para el resto de las veces
git pull para descargar los cambios        -->    Te informa de cuales son los archivos que son diferentes en 
                                                  el remoto en comparacion con el local.
