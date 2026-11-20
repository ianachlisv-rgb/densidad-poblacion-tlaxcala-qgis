"""Densidad de población por polígono (AGEB o municipios) con Jenks de 4 clases.

Reproduce en Python los pasos hechos en QGIS en el artículo:
  1. Verifica que la capa esté en un sistema métrico (EPSG:6372 para las capas del SCINCE 2020).
  2. Superficie:  AREA_HA = area / 10000   (o AREA_KM2 = area / 1e6)
  3. Densidad:    DEN_POB = POB1 / superficie
  4. Clasificación en 4 rangos por rupturas naturales de Jenks.
  5. Verificación: suma de la población y densidad global de la capa.

Uso:
    python calcular_densidad.py municipal.shp --unidad km2 --salida salida/municipios
    python calcular_densidad.py ageb_urb.shp  --unidad ha  --salida salida/ageb

Requiere: geopandas, mapclassify, matplotlib.  Los datos (SCINCE, INEGI) no se incluyen.
"""
import argparse
import os
import sys

import geopandas as gpd
import mapclassify
import matplotlib.pyplot as plt
import pandas as pd

FACTOR = {"ha": 1e4, "km2": 1e6}   # m² por unidad de superficie


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capa", help="shapefile o GeoPackage con los polígonos")
    ap.add_argument("--campo", default="POB1", help="campo de población total (por defecto POB1)")
    ap.add_argument("--unidad", choices=["ha", "km2"], default="km2", help="unidad de superficie")
    ap.add_argument("--clases", type=int, default=4, help="número de rangos de Jenks")
    ap.add_argument("--epsg", type=int, default=6372, help="EPSG métrico esperado")
    ap.add_argument("--reproyectar", action="store_true", help="reproyectar si la capa viene en otro sistema")
    ap.add_argument("--salida", default="salida/densidad", help="prefijo de los archivos de salida")
    a = ap.parse_args()

    g = gpd.read_file(a.capa)
    if g.crs is None:
        sys.exit("La capa no tiene sistema de referencia definido.")
    if g.crs.to_epsg() != a.epsg:
        if not a.reproyectar:
            sys.exit(f"La capa está en {g.crs}, no en EPSG:{a.epsg}. Usa --reproyectar para convertirla "
                     "(una superficie calculada en grados o en EPSG:3857 sería incorrecta).")
        g = g.to_crs(epsg=a.epsg)

    if a.campo not in g.columns:
        sys.exit(f"No existe el campo {a.campo}. Campos disponibles: {', '.join(g.columns)}")
    g[a.campo] = pd.to_numeric(g[a.campo], errors="coerce")        # los '*' del INEGI pasan a NaN

    col_sup = "AREA_HA" if a.unidad == "ha" else "AREA_KM2"
    g[col_sup] = g.geometry.area / FACTOR[a.unidad]
    g["DEN_POB"] = g[a.campo] / g[col_sup]

    ok = g["DEN_POB"].notna() & (g[col_sup] > 0)
    jk = mapclassify.NaturalBreaks(g.loc[ok, "DEN_POB"], k=a.clases)
    g.loc[ok, "RANGO"] = jk.yb + 1
    g["RANGO"] = g["RANGO"].astype("Int64")

    # --- verificación
    pob, sup = g.loc[ok, a.campo].sum(), g.loc[ok, col_sup].sum()
    print(f"Polígonos: {len(g)}  (con densidad válida: {int(ok.sum())})")
    print(f"Suma de {a.campo}: {pob:,.0f}")
    print(f"Superficie total: {sup:,.1f} {a.unidad}")
    print(f"Densidad global: {pob / sup:,.1f} hab/{a.unidad}")
    print("Rupturas de Jenks:", [round(float(b), 1) for b in jk.bins])
    print(g.loc[ok].groupby("RANGO").agg(n=("RANGO", "size"), poblacion=(a.campo, "sum"), sup=(col_sup, "sum")))
    print("Compara la suma de la población con el total oficial del INEGI antes de interpretar.")

    os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
    g.to_file(a.salida + ".gpkg", driver="GPKG")
    g.drop(columns="geometry").to_csv(a.salida + ".csv", index=False, encoding="utf-8")
    ax = g.plot(column="RANGO", cmap="Blues", categorical=True, legend=True, edgecolor="0.4",
                linewidth=0.2, missing_kwds={"color": "lightgrey"}, figsize=(8, 8))
    ax.set_axis_off()
    ax.set_title(f"Densidad de población ({a.clases} rangos, Jenks)")
    plt.savefig(a.salida + ".png", dpi=200, bbox_inches="tight")
    print("Archivos:", a.salida + ".gpkg / .csv / .png")


if __name__ == "__main__":
    main()
