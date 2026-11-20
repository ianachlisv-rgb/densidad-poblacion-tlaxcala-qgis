# Cálculo y mapeo de la densidad de población de Tlaxcala con QGIS (Censo 2020)

Análisis espacial de la densidad de población del estado de Tlaxcala con datos del Censo de Población y Vivienda 2020 del INEGI, en QGIS.

**Autor:** Ian A. Sandoval-Valderrábano, Colegio de Geofísica, Facultad de Ingeniería, Benemérita Universidad Autónoma de Puebla (BUAP).

## Contenido
- [`paper/Densidad_Poblacion_Tlaxcala_IEEE.pdf`](paper/Densidad_Poblacion_Tlaxcala_IEEE.pdf): artículo en formato IEEE (5 páginas, 5 figuras y 3 tablas).

## Qué se hizo
- Cálculo de la superficie y la densidad de 60 municipios y 668 AGEB urbanas con la calculadora de campos de QGIS, sobre EPSG:6372 (Cónica Conforme de Lambert).
- Clasificación de la densidad en cuatro rangos con rupturas naturales de Jenks y mapas temáticos a dos escalas.
- Validación contra cifras oficiales: la población coincidió exactamente y la densidad estatal difirió solo 0.6 %.

## Resultados
Tlaxcala ocupa el lugar 28 de 32 en población, pero el 4 en densidad (336 hab/km², frente a 64.3 hab/km² de promedio nacional). Los 12 municipios de densidad muy alta ocupan el 7.2 % del territorio y alojan el 34.9 % de la población.

## Qué no incluye
Los datos del INEGI y el proyecto de QGIS no están en este repositorio. Los datos del Censo 2020 (SCINCE) se pueden descargar en inegi.org.mx.
