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

- [`codigo/calcular_densidad.py`](codigo/calcular_densidad.py): los mismos pasos en Python, para repetirlos sin QGIS con cualquier capa de polígonos con población (probado con datos sintéticos).

## Pasos en QGIS (calculadora de campos)
1. Cargar `ageb_urb.shp` o `municipal.shp` del SCINCE 2020 y comprobar que la capa esté en **EPSG:6372** (Cónica Conforme de Lambert, metros).
2. Crear campos de tipo *Decimal number (real)*:
   - AGEB: `AREA_HA = $area / 10000` y `DEN_POB = "POB1" / "AREA_HA"`.
   - Municipios: `AREA_KM2 = $area / 1000000` y `DEN_POB = "POB1" / "AREA_KM2"`.
3. Simbología graduada sobre `DEN_POB` con modo *Rupturas naturales (Jenks)* y 4 clases.
4. Verificar: la suma de `POB1` debe coincidir con el total oficial del INEGI. Clasificar por error el campo `POB1` en lugar de `DEN_POB` da un mapa de población absoluta, no de densidad.

## Uso del script
```
pip install geopandas mapclassify matplotlib
python codigo/calcular_densidad.py municipal.shp --unidad km2 --salida salida/municipios
python codigo/calcular_densidad.py ageb_urb.shp  --unidad ha  --salida salida/ageb
```
Si la capa no está en EPSG:6372 el script se detiene (usa `--reproyectar` para convertirla). Escribe un GeoPackage, un CSV y un mapa, e imprime la suma de la población, la densidad global y las rupturas de Jenks.

## Qué no incluye
Los datos del INEGI y el proyecto de QGIS no están en este repositorio. Los datos del Censo 2020 (SCINCE) se pueden descargar en inegi.org.mx.

## Licencia
Código bajo licencia MIT (ver [`LICENSE`](LICENSE)). El texto y las figuras del artículo son del autor; los datos del INEGI pertenecen a la institución.
