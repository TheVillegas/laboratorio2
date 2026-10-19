# Laboratorio 2 — Catálogo de libros

Proyecto de Ingeniería Web Avanzada: extracción de la primera página de
https://books.toscrape.com/, procesamiento con Pandas y búsqueda TF-IDF.

**Estado:** implementación en curso; todavía no está listo para entregar.
**Integrantes:** 
* Francisco Cortés Jorquera
* Matias Villegas Muñoz
* Matias Romero Alvarez

## Entorno local

```bash
python -m venv .venv
source .venv/bin/activate
```

El entorno `.venv/`, las cachés y los archivos `.env` no se versionan.
No se necesitan credenciales para acceder al catálogo de práctica.


## Preguntas:
* **Pregunta 1** ¿Para qué sirve BeautifulSoup y cómo se diferencia de requests?


* **Pregunta 2:** ¿Qué riesgo existe al depender de selectores HTML específicos si el sitio cambia?


* **Pregunta 3:**


* **Pregunta 4:** En el código entregado, ¿qué función cumple fit_transform() sobre los títulos y por qué se usa transform() para la consulta?


* **Pregunta 5:** Si dos libros obtienen similitudes de 0.75 y 0.20 para la misma consulta, ¿cuál se muestra primero? Explique qué indica una puntuación cercana a cero.


* **Pregunta 6:** ¿Qué limitación tiene buscar solo por palabras presentes en títulos mediante TF-IDF? Proponga una mejora concreta.