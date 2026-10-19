# Guía paso a paso para ejecutar y entregar el laboratorio 2

El código ya está implementado. Esta guía explica qué ejecutar, qué observar y
qué registrar para que el equipo compruebe y complete la entrega del PDF.
No hace falta volver a programar el laboratorio ni copiar libros manualmente.

**Repositorio:** https://github.com/TheVillegas/laboratorio2

## Cómo usar esta guía

Seguí las secciones en orden. Ejecutá los comandos en una terminal; las consultas
se escriben dentro del buscador, no como comandos del sistema.

| Archivo | Para qué sirve |
|---|---|
| `scraper.py` | Descarga e interpreta la primera página del catálogo |
| `procesamiento.py` | Extrae, limpia y exporta los datos a `libros.csv` |
| `buscador.py` | Busca títulos del CSV usando TF-IDF y similitud del coseno |
| `requirements.txt` | Fija las versiones de las dependencias |
| `EVIDENCIAS.md` | Reúne respuestas y resultados de la ejecución ya verificada |
| `README.md` | Documento final de entrega que debe completar el equipo |

**Importante:** esta guía describe acciones por realizar. No acredita que ustedes
ya hayan hecho la inspección del navegador o probado sus propios equipos.

## 1. Obtener el proyecto

Si todavía no tenés una copia local:

```bash
git clone https://github.com/TheVillegas/laboratorio2.git
cd laboratorio2
```

Si ya lo tenés, abrí una terminal en su carpeta. No vuelvas a clonarlo dentro de
ella. La copia original está en:

```text
/home/thevillegas/Documents/UNIVERSIDAD-CURSOS/laboratorio2
```

Antes de actualizar una copia existente, ejecutá `git status`. Si hay cambios
locales, coordiná con su autor y preservalos antes de intentar integrar cambios.
**No uses `git reset --hard`, `git clean` ni un push forzado.**
Si está limpia y estás en `main`, podés actualizarla con `git pull --ff-only`.
Si Git rechaza la actualización, detenete y revisá el motivo, no la fuerces.

**Comprobación:** tenés que ver los tres archivos `.py`, el CSV y `requirements.txt`.

## 2. Crear y activar el entorno virtual — preparación 0.1 y 0.2

El entorno verificado usa **Python 3.14.7 en Linux**. Para reproducir las versiones
fijadas, usá Python 3.14. Los comandos de Windows se proporcionan como instrucciones;
no fueron ejecutados en este entorno.

### Linux / macOS

```bash
python --version
python -m venv .venv
source .venv/bin/activate
```

Si tu instalación ofrece `python3` en lugar de `python`, usá `python3` para crear
el entorno y comprobá que sea la versión indicada. Si `.venv` ya existe, activalo;
no hace falta recrearlo ni borrarlo.

### Windows PowerShell

```powershell
py --version
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, podés abrir **CMD** y usar la alternativa
siguiente; no es necesario cambiar políticas de seguridad para seguir esta guía.

### Windows CMD

```bat
py --version
py -m venv .venv
.venv\Scripts\activate.bat
```

Cada compañero crea su propio entorno. No se comparte ni se sube `.venv`.
En una terminal nueva hay que volver a activarlo.

## 3. Verificar el intérprete e instalar bibliotecas — preparación 0.3 y 0.4

Con el entorno activo:

```bash
python -c "import sys; print(sys.executable); assert sys.prefix != sys.base_prefix"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
git check-ignore .venv/pyvenv.cfg
```

**Qué observar:**

- La ruta del intérprete debe estar dentro de `.venv`; el `assert` no debe fallar.
- `pip check` debe mostrar `No broken requirements found.`.
- `git check-ignore` debe mostrar `.venv/pyvenv.cfg`.

La instalación original usó los comandos del PDF:

```bash
python -m pip install requests beautifulsoup4 pandas scikit-learn
python -m pip freeze > requirements.txt
```

**No repitas esos dos últimos comandos para reproducir el proyecto:** ya existe un
archivo fijado; usá `pip install -r requirements.txt`. Volver a congelar otro entorno
podría cambiar las versiones compartidas. No instales dependencias globalmente si
falla la instalación: revisá primero versión de Python, activación y conexión.

**Registrar en el README:** versión de Python, comando de activación utilizado y
comando de instalación desde `requirements.txt`.

## 4. Inspeccionar el HTML en el navegador — parte I, paso 2

1. Abrí https://books.toscrape.com/ y quedate en la primera página.
2. Hacé clic derecho sobre el título del primer libro y elegí **Inspeccionar**.
   También podés abrir las herramientas con `F12` o `Ctrl+Shift+I`.
3. En **Elementos / Inspector**, ubicá el enlace del título dentro de `h3`.
4. Subí por sus elementos padre hasta encontrar `<article class="product_pod">`.
   Ese elemento contiene los datos de un libro, no los de toda la página.
5. Expandí sus elementos hijos y comprobá los cuatro campos de esta tabla.

| Campo | Selector usado en Python | Qué mirar en el inspector |
|---|---|---|
| Contenedor | `article.product_pod` | Un bloque por libro |
| Título | `h3 a` | Atributo `title` del enlace: contiene el título completo |
| Precio | `.price_color` | Texto del precio con el símbolo `£` |
| Disponibilidad | `.availability` | Texto como `In stock`; puede incluir espacios y saltos |
| Estrellas | `.star-rating` | Clase adicional `One`, `Two`, `Three`, `Four` o `Five` |

Ejemplo **ilustrativo** de la calificación:

```html
<p class="star-rating Three">
```

La clase `Three` se transforma en el entero `3`. El punto de `.star-rating`
significa buscar una clase CSS; no forma parte del nombre de la clase en el HTML.

El título visible puede terminar en puntos suspensivos. Por eso el scraper lee
el atributo `title`, en vez de quedarse con el texto truncado del enlace.
Podés usar `Ctrl+F` dentro del panel del inspector para localizar `product_pod`.

**Relacionar con el código:** abrí `scraper.py` y compará lo observado con
`soup.select("article.product_pod")` y las llamadas a `select_one(...)`.

**Registrar después de hacerlo:** selectores comprobados y una explicación de
cómo identificaron cada campo. Una captura con el HTML seleccionado es evidencia
adicional útil, pero no un requisito nuevo de esta guía. No escriban que realizaron
la inspección si todavía no la hicieron. No naveguen a otras páginas del catálogo
para ampliar el conjunto de datos de este laboratorio.

## 5. Ejecutar la extracción — parte I, pasos 1, 3 y 4

```bash
python scraper.py
```

El programa hace una petición con `timeout=10`, valida la respuesta HTTP y muestra:

- El total extraído.
- Los primeros cinco registros con `titulo`, `precio`, `disponibilidad` y `calificacion`.

En la ejecución ya verificada se obtuvieron **20 libros**. Compará algunos con
los que acabás de inspeccionar. El precio debe ser numérico y la calificación un
entero de 1 a 5. Un libro incompleto se omite con una advertencia; no interrumpe a
los demás. Si no hay libros válidos o falla la petición, hay un error que revisar.

**Registrar:** total, muestra y tratamiento de datos ausentes. No ingreses libros
manualmente al CSV ni repitas peticiones en un bucle si aparece un error.

## 6. Limpiar y generar el CSV — parte II, pasos 5 a 7

```bash
python procesamiento.py
```

Este comando llama una vez a `obtener_libros()`, construye un DataFrame, limpia
espacios, elimina duplicados por título, crea `titulo_normalizado` en minúsculas
y convierte los campos numéricos. Muestra una muestra, información de tipos,
dimensiones, cantidad y promedio. Guarda `libros.csv` en UTF-8 y sin índice.

**Atención:** vuelve a extraer la primera página y reemplaza el CSV generado.
No lo ejecutes sobre cambios de datos de un compañero sin coordinar. Ejecutar los
pasos 5 y 6 una vez hace dos peticiones moderadas. Para regenerar solamente los
datos alcanza con el paso 6: el paso 5 es la demostración independiente del scraper.

**Resultado de referencia, no garantía de un catálogo inmutable:**

| Comprobación | Resultado ya observado |
|---|---|
| Dimensiones | `(20, 5)` |
| Cantidad | 20 libros |
| Precio promedio | £38.05, sin redondear 38.0485 |
| Tipo de precio | `float64` |
| Tipo de calificacion | `int64` |
| Columnas | `titulo`, `precio`, `disponibilidad`, `calificacion`, `titulo_normalizado` |

**Registrar:** los valores que realmente muestre tu ejecución. Si cambian,
compará el catálogo y el código; no edites los datos para forzar estos números.

## 7. Probar el buscador y documentar dos consultas — parte III, pasos 8 a 11

```bash
python buscador.py
```

Cuando aparezca `Ingrese una palabra o titulo:`, escribí `the` y presioná Enter.
Después ejecutá el programa otra vez y consultá `life`. Ambas palabras estaban
presentes en los títulos extraídos. Si el catálogo cambia, comprobalo primero.

Por cada resultado debés ver **título, precio y similitud**. Compará el orden de
los libros. Las dos salidas de referencia están en [EVIDENCIAS.md](EVIDENCIAS.md).
El buscador no descarga datos; usa `libros.csv`.

### Comprobar el desafío de tres resultados

En `buscador.py`, la llamada del programa ya es `buscar(consulta, top_k=3)`.
Comprobá que la consulta `the` muestra como máximo tres libros y que todas las
similitudes son positivas y aparecen de mayor a menor. La función mantiene
`top_k=5` por defecto; el programa utiliza explícitamente tres.

**Registrar:** las dos consultas con sus títulos, precios, puntuaciones y una
breve comparación del ranking. No copies los ejemplos ficticios del PDF como
si fueran resultados del programa.

## 8. Ejecutar T1–T4 — parte IV, paso 12

Ejecutá `python buscador.py` **una vez por cada fila**:

| Caso | Qué escribir cuando el programa pregunte | Qué comprobar |
|---|---|---|
| T1 | `the` | Resultados con puntuación positiva, ordenados de mayor a menor |
| T2 | `zzxyz123` | `No se encontraron coincidencias.` |
| T3 | `THE` | Los mismos libros, orden y puntuaciones que T1 |
| T4 | No escribas nada: presioná Enter | Mensaje informativo, sin traceback ni excepción |

T3 tiene que ser exactamente la consulta de T1 cambiando solo mayúsculas y
minúsculas. Si elegís otro término para T1, usá su equivalente en T3.
En T4 el programa muestra `Ingrese una consulta no vacia.` y después
`No se encontraron coincidencias.`. Ese comportamiento es válido.

Para el README, completá esta tabla **después de ejecutar las consultas**:

| Caso | Consulta utilizada | Resultado observado | Estado |
|---|---|---|---|
| T1 | Por completar | Por completar | Cumple / No cumple |
| T2 | Por completar | Por completar | Cumple / No cumple |
| T3 | Por completar | Por completar | Cumple / No cumple |
| T4 | [vacía] | Por completar | Cumple / No cumple |

Si un caso falla, marcá **No cumple**, registrá el problema y revisalo antes de
entregar. No marques todos como aprobados solo porque existe esta guía.

### Ejecutar también las pruebas automatizadas

```bash
python -m unittest discover -s tests -v
```

La versión publicada tiene **11 pruebas**, que ya pasaron. En tu equipo esperá el
resumen `Ran 11 tests` y `OK`. Son pruebas sin red y usan datos temporales;
no reemplazan la inspección del navegador ni la demostración manual anterior.

## 9. Completar el README — preguntas 1–6 y paso 13

Esta parte la está preparando un compañero. Coordiná con él: no reemplaces su
README completo por otro archivo. Puede integrar lo necesario de `EVIDENCIAS.md`,
que contiene respuestas desarrolladas y resultados reales de referencia.

El README final debe incluir:

- Nombres de todos los integrantes y URL del repositorio.
- Creación y activación del entorno, comprobación del intérprete e instalación
  desde `requirements.txt`; orden de ejecución de los programas.
- Cantidad de libros extraídos, precio promedio y manejo de elementos sin datos.
- Dos consultas, sus resultados y comparación del ranking.
- Tabla T1–T4 con consulta, resultado observado y estado; explicación de fallos.
- Respuestas a las seis preguntas del PDF:
  1. Para qué sirve BeautifulSoup y cómo se diferencia de requests.
  2. Riesgo de que cambien los selectores HTML.
  3. Por qué normalizar los títulos.
  4. Diferencia entre `fit_transform()` para títulos y `transform()` para consultas.
  5. Orden entre similitudes 0.75 y 0.20 y significado de un valor cercano a cero.
  6. Limitación de TF-IDF sobre títulos y una mejora concreta.

Agreguen también el registro de la inspección efectivamente realizada en el paso 4.
Un enlace a esta guía sirve como ayuda, pero **no reemplaza el contenido obligatorio
del README**. Revisen las respuestas en grupo para poder explicarlas.

## 10. Revisar Git y entregar — paso 14

Antes de subir nada:

```bash
git status --short
git diff -- README.md
git check-ignore .venv/pyvenv.cfg
```

Revisá que no haya credenciales, archivos `.env`, cachés ni el entorno virtual entre
los archivos a subir. El repositorio es público. Agregá únicamente los archivos
que revisaste; no uses `git add .` sin comprobar qué incluiría.

Si el README ya quedó acordado, estos comandos suben **solo ese archivo** a la
rama actual; antes confirmá con el equipo cuál están usando:

```bash
git branch --show-current
git add README.md
git diff --cached --check
git diff --cached -- README.md
git commit -m "docs: complete lab report and execution evidence"
git push
```

No los ejecutes si el diff incluye trabajo ajeno que todavía no revisaron. Si el
push se rechaza porque otro compañero actualizó la rama, no fuerces la subida:
coordinen la integración. Si trabajan en una rama de equipo, revisen y fusionen
sus cambios a `main` antes de entregar la URL de `main`.

Después abrí GitHub y comprobá que la rama de entrega muestra el README final y:

```text
scraper.py
procesamiento.py
buscador.py
libros.csv
requirements.txt
README.md
.gitignore
```

Entreguen la URL https://github.com/TheVillegas/laboratorio2 según el mecanismo
indicado por el docente. No es necesario subir `.venv`, crear un ZIP ni publicar
una aplicación web para cumplir el entregable descrito en el PDF.

## Checklist final del equipo

- [ ] Cada integrante puede activar su propio entorno e instalar las dependencias.
- [ ] Se inspeccionó el HTML de la primera página en el navegador.
- [ ] Se verificaron extracción, limpieza, tipos y CSV generado por el programa.
- [ ] Se registraron cantidad de libros, precio promedio y dos búsquedas reales.
- [ ] Se ejecutaron y documentaron T1, T2, T3 y T4.
- [ ] El buscador muestra como máximo tres resultados de similitud positiva.
- [ ] Las pruebas automatizadas terminan en `OK`.
- [ ] El README tiene integrantes, URL, instrucciones, evidencias y seis respuestas.
- [ ] Los cambios finales están visibles en GitHub, sin entorno virtual ni secretos.

## Si algo no funciona

| Síntoma | Qué revisar |
|---|---|
| `ModuleNotFoundError` | Activación de `.venv`, intérprete e instalación con `python -m pip` |
| No encuentra `libros.csv` | Ejecutar `python procesamiento.py` y comprobar dónde guardó el archivo |
| Error HTTP, conexión o timeout | Conexión y disponibilidad del sitio; no eludir restricciones ni hacer peticiones repetitivas |
| Cero libros válidos o advertencias nuevas | Inspeccionar HTML y comprobar los selectores; no fabricar filas en el CSV |
| `No hay títulos válidos` | Revisar `titulo_normalizado` y la salida de procesamiento |
| No hay coincidencias para una palabra | Comprobar que la palabra esté en un título; TF-IDF no interpreta sinónimos |
| Git impide actualizar o subir | Revisar cambios locales y remotos con el equipo; no descartar ni forzar |
