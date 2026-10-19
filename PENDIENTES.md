# Pendientes para entregar el laboratorio 2

El código está implementado y publicado; las 11 pruebas automatizadas pasaron.
Este checklist reúne lo que queda por completar o confirmar por el equipo.
No implica que estas tareas sigan sin hacerse si alguien ya avanzó: coordinen y
marquen cada casilla únicamente después de comprobarla.

## 1. Completar el README final

**Responsable sugerido:** compañero que ya está editando el README.

- [x] Registrar los nombres y aportes de Matias Villegas, Matias Romero y Francisco Cortes.
- [ ] Comprobar la URL del repositorio en el README final.
- [ ] Incluir creación y activación de `.venv`, verificación del intérprete,
      instalación desde `requirements.txt` y orden de ejecución.
- [ ] Incorporar las respuestas a las preguntas 1–6 y revisarlas en grupo.
- [ ] Incluir cantidad de libros, precio promedio y tratamiento de datos ausentes.
- [ ] Incorporar dos búsquedas reales con títulos, precios, similitudes y comparación del ranking.
- [ ] Incorporar la tabla T1–T4 con consulta, resultado observado y Cumple / No cumple.

Las respuestas y los resultados ya obtenidos están en [EVIDENCIAS.md](EVIDENCIAS.md).
Integren lo necesario sin reemplazar ni pisar el trabajo del compañero.

## 2. Realizar la inspección manual del HTML

**Responsable:** por acordar. Instrucciones: paso 4 de [la guía](GUIA_PASO_A_PASO.md).

- [ ] Abrir https://books.toscrape.com/ y quedarse en la primera página.
- [ ] Usar Inspeccionar para localizar `article.product_pod`, `h3 a`,
      `.price_color`, `.availability` y `.star-rating`.
- [ ] Comprobar el título completo en el atributo `title`, el precio,
      la disponibilidad y la clase de calificación `One`–`Five`.
- [ ] Registrar en el README lo efectivamente observado y su relación con `scraper.py`.

Una captura es una ayuda opcional, no un requisito adicional del laboratorio.
Esta inspección no fue realizada desde el entorno donde se implementó el código.

## 3. Confirmar la ejecución en un equipo del grupo

**Responsable:** Francisco Cortes. Instrucciones: pasos 1–8 de [la guía](GUIA_PASO_A_PASO.md).

**Validación informada por el equipo:** Francisco Cortes validó el entorno en
otro equipo con un entorno limpio. Matias Romero validó el contenido del trabajo
realizado por Matias Villegas.

Las pruebas ya pasaron en el entorno original. Las casillas siguientes se
mantienen sin marcar porque no se informó el resultado individual de cada
comprobación en el otro equipo; no implican que la validación esté pendiente.

- [ ] Clonar el repositorio, crear un `.venv` propio e instalar `requirements.txt`.
- [ ] Comprobar el intérprete del entorno y ejecutar `python -m pip check`.
- [ ] Ejecutar `python scraper.py` y observar total y primeros cinco registros.
- [ ] Ejecutar `python procesamiento.py` y comprobar el CSV, sus tipos y el promedio.
- [ ] Ejecutar `python buscador.py` para cada caso:
      **T1:** `the`; **T2:** `zzxyz123`; **T3:** `THE`; **T4:** Enter sin texto.
- [ ] Confirmar T1 positivo y ordenado, T2 sin coincidencias, T3 equivalente a T1
      y T4 informativo sin excepción. Registrar cualquier fallo, no marcarlo como aprobado.
- [ ] Buscar también `life` para tener el segundo ejemplo y comprobar el máximo
      de tres resultados con similitud positiva.
- [ ] Ejecutar `python -m unittest discover -s tests -v` y comprobar `Ran 11 tests` y `OK`.

Si el catálogo cambia, registren sus resultados reales: no editen el CSV para
forzar los valores de referencia. No hace falta probar en Windows si el grupo
usa otro sistema; los comandos de Windows están documentados, pero no se ejecutaron aquí.

## 4. Cerrar y entregar

**Responsables:** equipo completo. Instrucciones de Git: paso 10 de [la guía](GUIA_PASO_A_PASO.md).

- [ ] Revisar juntos el README final y poder explicar las seis respuestas.
- [ ] Subir los cambios acordados sin incluir `.venv`, temporales ni secretos;
      coordinar antes de integrar cambios y no usar un push forzado.
- [ ] Comprobar en GitHub que la rama de entrega contiene el README final,
      `scraper.py`, `procesamiento.py`, `buscador.py`, `libros.csv`,
      `requirements.txt` y `.gitignore`.
- [ ] Entregar https://github.com/TheVillegas/laboratorio2 por el medio indicado por el docente.

**No falta programar nuevas funcionalidades según la verificación realizada.**
Si alguna comprobación detecta un problema, registren el error exacto antes de dar la entrega por cerrada.
