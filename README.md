# MT Inversion (1D & 2D)

Este repositorio contiene scripts y notebooks para realizar inversiones magnetotelúricas (MT) en 1D y 2D utilizando Python. Apoyado por el equipo de trabajo*, conformado por [Johan Páez](https://github.com/JohanPaez14/), [Camilo Caballero](https://github.com/Camilojaimes973), Ana Mantilla y Paul Goyes.

_*Semillero de Investigación de Geofísica Aplicada y Computacional (SIGAC)_

## Tabla de Contenidos
- [Introducción](#introducción)
- [Instalación](#instalación)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Licencia](#licencia)

## Introducción

Este proyecto implementa métodos de inversión magnetotelúrica (MT) para perfiles 1D y 2D. Utilizamos la biblioteca [SimPEG](https://simpeg.xyz) y otros paquetes científicos en Python para procesar datos y realizar la inversión.

## Instalación

Para utilizar este repositorio, necesitas tener instalado Python 3.11.0. Para ello creas un ambiente conda:
```bash
conda create --name simpeg0230 python==3.11
```
Y activas el ambiente:
```bash
conda activate simpeg0220
```
### Instalación de librerías
Se debe instalar las siguientes librerías: simpeg (v0.23.0) y mpty (v2.0.11). Así mismo, para generar un ambiente iterativo es necesario instalar ipywidgets
```bash
pip install simpeg
pip install mtpy-v2
conda install ipywidgets
```

Para facilitar la instalación, puedes instalar el ambiente donde están todas las librerías:
```bash
conda env create --file environment.yml
```

## Estructura del Repositorio
* `analisis/`: contiene el notebook necesario para hacer el análisis de dimensionalidad.
* `data/`: contiene los datos utilizados para las inversiones, ya sea edis o transfers_functions.
* `inversion/`: notebooks para realizar y visualizar las inversion 1D, 2D y 3D.
* `procesamiento/`: contiene el notebook para realizar el acondicionamiento de los datos, ya sea interpolar, seleccionar un rango, eliminar estaciones [...].

## Atribución
Este repositorios contiene código que fue originalmente desarrollado por [Seogi Kang](https://github.com/sgkang) con su equipo de trabajo y puede ser encontrado en [iri-mt-course-2022](https://github.com/simpeg-research/iris-mt-course-2022/tree/main). \
Este proyecto utiliza datos del [Repositorio UIS de datos geofísicos](https://n9.cl/repositoriouisdatosgeofisicos) proporcionado por SIGAC (2022).

## Licencia
Este proyecto está bajo la misma Licencia MIT que el código original. Ver el archivo [LICENSE](LICENSE) para más detalles.
