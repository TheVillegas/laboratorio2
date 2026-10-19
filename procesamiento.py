"""Clean extracted records and export the reproducible UTF-8 dataset."""

from pathlib import Path

import pandas as pd

from scraper import obtener_libros

ARCHIVO_CSV = Path(__file__).with_name("libros.csv")


def procesar_libros(registros, archivo_salida=ARCHIVO_CSV):
    df = pd.DataFrame(registros, columns=["titulo", "precio", "disponibilidad", "calificacion"])
    df = df.dropna(subset=["titulo"]).copy()
    df["titulo"] = df["titulo"].str.split().str.join(" ")
    df = df[df["titulo"] != ""].drop_duplicates(subset=["titulo"]).copy()
    df["disponibilidad"] = df["disponibilidad"].str.split().str.join(" ")
    df["titulo_normalizado"] = df["titulo"].str.lower()
    df["precio"] = pd.to_numeric(df["precio"], errors="raise").astype(float)
    df["calificacion"] = pd.to_numeric(df["calificacion"], errors="raise").astype(int)
    df = df.reset_index(drop=True)
    df.to_csv(archivo_salida, index=False, encoding="utf-8")
    return df


if __name__ == "__main__":
    df = procesar_libros(obtener_libros())
    print(df.head())
    df.info()
    print(f"Dimensiones: {df.shape}")
    print(f"Cantidad de libros: {len(df)}")
    print(f"Precio promedio: £{df['precio'].mean():.2f}")
    print(f"CSV guardado: {ARCHIVO_CSV.name}")
