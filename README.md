# MT Inversion (1D & 2D)

Este repositorio contiene scripts y notebooks para realizar inversiones magnetotelúricas (MT) en 1D y 2D utilizando Python. Apoyado por el equipo de trabajo*, conformado por Johan Páez, Camilo Caballero, Ana Mantilla y Paul Goyes.

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


## Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.
