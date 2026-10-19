"""Search book titles with one reusable TF-IDF index and cosine similarity."""

from functools import lru_cache
from pathlib import Path
import sys

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ARCHIVO_CSV = Path(__file__).with_name("libros.csv")


class Buscador:
    def __init__(self, archivo_csv=ARCHIVO_CSV):
        libros = pd.read_csv(archivo_csv).dropna(subset=["titulo_normalizado"]).copy()
        libros["titulo_normalizado"] = libros["titulo_normalizado"].astype(str).str.strip()
        self.libros = libros[libros["titulo_normalizado"] != ""].reset_index(drop=True)
        if self.libros.empty:
            raise ValueError("No hay títulos válidos; ejecute procesamiento.py.")
        self.vectorizador = TfidfVectorizer()
        self.matriz_tfidf = self.vectorizador.fit_transform(self.libros["titulo_normalizado"])

    def buscar(self, consulta: str, top_k: int = 5):
        consulta = consulta.strip().lower()
        if not consulta:
            print("Ingrese una consulta no vacia.")
            return []
        vector_consulta = self.vectorizador.transform([consulta])
        puntuaciones = cosine_similarity(vector_consulta, self.matriz_tfidf).ravel()
        indices = puntuaciones.argsort()[::-1]
        return [{"titulo": self.libros.iloc[i]["titulo"],
                 "precio": float(self.libros.iloc[i]["precio"]),
                 "similitud": float(puntuaciones[i])}
                for i in indices[:max(0, top_k)] if puntuaciones[i] > 0]


@lru_cache(maxsize=1)
def _buscador_predeterminado():
    return Buscador()


def buscar(consulta: str, top_k: int = 5):
    return _buscador_predeterminado().buscar(consulta, top_k)


if __name__ == "__main__":
    try:
        consulta = input("Ingrese una palabra o titulo: ")
        resultados = buscar(consulta, top_k=3)
        if not resultados:
            print("No se encontraron coincidencias.")
        for r in resultados:
            print(f"{r['titulo']} | Precio: {r['precio']} | Similitud: {r['similitud']:.4f}")
    except (OSError, ValueError, KeyError, EOFError) as error:
        print(f"Error de búsqueda: {error}", file=sys.stderr)
        sys.exit(1)
