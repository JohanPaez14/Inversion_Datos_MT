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
conda create -n simpeg0220 python==3.11
```
Y activas el ambiente:
```bash
conda activate simpeg0220
```
### Intalación de librerías
Algunas de las dependencias listadas en `requirements.txt` son importantes instalarlas en una versión en específico para evitar errores, tal como:
```bash
pip install numpy==1.26.4
```
Para fácilitar la instalación, puedes instalarlas rápidamente utilizando:
```bash
pip install -r requirements.txt
```

## Estructura del Repositorio
* `Caso 1D/`: Notebooks de Jupyter para realizar y visualizar las inversiones 1D.
* `Caso 2D/`: Notebooks de Jupyter para realizar y visualizar las inversiones 2D.
* `Data/`: Contiene los datos utilizados para las inversiones.
* `Funciones_transferencia/`: Contiene archivos de formato Mth5 que contiene la información de los datos en `data/`.

## Atribución
Este repositorios contiene código que fue originalmente desarrollado por [Seogi Kang](https://github.com/sgkang) con su equipo de trabajo y puede ser encontrado en [iri-mt-course-2022](https://github.com/simpeg-research/iris-mt-course-2022/tree/main). El código original está licenciado bajo la Licencia MIT. \
Este proyecto utiliza datos del Repositorio UIS de datos geofísicos proporcionado por SIGAC (2022). Puedes encontrar el repositorio original en el siguiente enlace: [Repositorio](https://n9.cl/repositoriouisdatosgeofisicos).

## Licencia
Este proyecto está bajo la misma Licencia MIT que el código original. Ver el archivo [LICENSE](LICENSE) para más detalles.
