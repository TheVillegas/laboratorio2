"""Extract books from the first catalog page, without import-time requests."""

import json
import sys
import warnings

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
ESTRELLAS = {nombre: valor for valor, nombre in
             enumerate(("One", "Two", "Three", "Four", "Five"), 1)}


def obtener_libros():
    respuesta = requests.get(URL, timeout=10)
    respuesta.raise_for_status()
    respuesta.encoding = "utf-8"
    soup = BeautifulSoup(respuesta.text, "html.parser")
    libros = []
    for numero, elemento in enumerate(soup.select("article.product_pod"), 1):
        try:
            titulo = elemento.select_one("h3 a")["title"].strip()
            precio = float(elemento.select_one(".price_color").get_text(strip=True).replace("£", ""))
            disponibilidad = elemento.select_one(".availability").get_text(" ", strip=True)
            clases = elemento.select_one(".star-rating").get("class", [])
            calificacion = next(ESTRELLAS[clase] for clase in clases if clase in ESTRELLAS)
            if not titulo or not disponibilidad:
                raise ValueError("Título o disponibilidad vacíos")
        except (AttributeError, TypeError, KeyError, ValueError, StopIteration):
            warnings.warn(f"Se omite el libro {numero}: datos incompletos o inválidos.", stacklevel=2)
            continue
        libros.append(dict(titulo=titulo, precio=precio,
                           disponibilidad=disponibilidad, calificacion=calificacion))
    if not libros:
        raise ValueError("No se extrajeron libros válidos; revise el HTML del catálogo.")
    return libros


if __name__ == "__main__":
    try:
        libros = obtener_libros()
        print(f"Total extraído: {len(libros)}")
        print(json.dumps(libros[:5], ensure_ascii=False, indent=2))
    except (requests.RequestException, ValueError) as error:
        print(f"Error de extracción: {error}", file=sys.stderr)
        sys.exit(1)
