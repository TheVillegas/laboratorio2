# Laboratorio 2 — Catálogo de libros

Proyecto de Ingeniería Web Avanzada: extracción de la primera página de
https://books.toscrape.com/, procesamiento con Pandas y búsqueda TF-IDF.

**Estado:** implementación en curso; todavía no está listo para entregar.
**Integrantes:** pendiente de completar con los nombres reales.

## Entorno local

El proyecto requiere **Python 3.14** (fijado en `.python-version`). Con una
versión anterior, como 3.9, la instalación falla:
`No matching distribution found for joblib==1.6.0`.

```bash
python3.14 -m venv .venv          # o: "$(uv python find 3.14)" -m venv .venv
source .venv/bin/activate
python --version                  # debe mostrar Python 3.14.x
python -m pip install -r requirements.txt
python -m pip check
```

El entorno `.venv/`, las cachés y los archivos `.env` no se versionan.
No se necesitan credenciales para acceder al catálogo de práctica.

## Verificación de ejecución

Ejecutado el 2026-10-19 en macOS arm64 con Python 3.14.8, sobre un clon limpio
de `main` (`32ac93f`). `pip check`: `No broken requirements found.`

- Scraper: `Total extraído: 20`; primeros cinco desde *A Light in the Attic* hasta *Sapiens*.
- Procesamiento: forma `(20, 5)`, `precio` float64, `calificacion` int64,
  precio promedio £38.05; el CSV regenerado es idéntico al versionado.
- T1 `the` y T3 `THE`: los mismos tres resultados ordenados (0.4181, 0.3630, 0.3282) → Cumple.
- T2 `zzxyz123`: `No se encontraron coincidencias.` → Cumple.
- T4 vacío: `Ingrese una consulta no vacia.` sin excepción → Cumple.
- `life`: tres resultados positivos (0.2459, 0.2250, 0.2231) → Cumple.
- Pruebas: `Ran 11 tests` y `OK`.
