# Evidencias y borrador para el README del equipo

El README principal lo está preparando un compañero. Este archivo reúne
instrucciones, respuestas y resultados verificados para que los integre
sin sobrescribir su trabajo. No reemplaza el README final exigido por la consigna.

# Laboratorio 2 — Catálogo de libros

Extracción de la **primera página** de https://books.toscrape.com/, limpieza
con Pandas y búsqueda de títulos con TF-IDF y similitud del coseno.

- **Asignatura:** Ingeniería Web Avanzada, OII436-1.
- **Integrantes:** PENDIENTE: completar los nombres reales antes de entregar.
- **Repositorio:** https://github.com/TheVillegas/laboratorio2 (público).
- **Entorno comprobado:** Python 3.14.7 en Linux; versiones en `requirements.txt`.

## Reproducir desde cero

Necesitás Git y Python 3.14 con soporte para `venv` y `pip`.

```bash
git clone https://github.com/TheVillegas/laboratorio2.git
cd laboratorio2
python -m venv .venv
source .venv/bin/activate   # Linux / macOS: activación usada en este proyecto
python -c "import sys; print(sys.executable); assert sys.prefix != sys.base_prefix"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

En Windows, creá el entorno con `py -m venv .venv`. Activación:

```powershell
# PowerShell
.venv\Scripts\Activate.ps1
```

```bat
:: CMD
.venv\Scripts\activate.bat
```

En la preparación original se ejecutó `python -m pip install requests beautifulsoup4 pandas scikit-learn`
y después `python -m pip freeze > requirements.txt`. Para reproducirla, usá el
archivo de versiones, no una instalación sin versiones fijadas.

## Orden de ejecución

Con el entorno activo y desde la carpeta del proyecto:

```bash
python scraper.py          # Comprobación independiente: total y primeros cinco libros
python procesamiento.py    # Una petición; limpia y genera libros.csv
python buscador.py         # Consulta interactiva; muestra hasta tres resultados
python -m unittest discover -s tests -v
```

`scraper.py` es una comprobación opcional: `procesamiento.py` ya invoca la
extracción. Ejecutarlos ambos hace dos peticiones, no es necesario para generar
el CSV. No hay paginación, reintentos automáticos ni peticiones al importar módulos.
El buscador usa el CSV entregado sin acceder a Internet. Los scripts resuelven
la ubicación del CSV respecto de su propio archivo.

## Extracción y procesamiento

Los selectores usados son `article.product_pod`, `h3 a` (atributo `title`, no
el texto truncado), `.price_color`, `.availability` y `.star-rating`.
El precio se convierte a `float` y las clases `One`–`Five` a enteros de 1 a 5.
Se interpreta el HTML como UTF-8 para conservar correctamente el símbolo £.

La petición usa `requests.get(URL, timeout=10)` y `raise_for_status()`.
Si un libro tiene campos ausentes o inválidos, se omite con una advertencia;
la extracción continúa con los demás. Si no queda ningún libro válido, se
informa un error en lugar de fabricar datos. Un error HTTP tampoco genera datos.

Pandas elimina espacios sobrantes, deduplica por título ya limpio, crea
`titulo_normalizado` en minúsculas y convierte los campos numéricos. Se exporta
`libros.csv` en UTF-8, sin índice. Los datos provienen del programa, no de carga manual.

| Evidencia de la ejecución real | Resultado |
|---|---|
| Libros extraídos / procesados | 20 / 20 |
| Columnas del CSV | titulo, precio, disponibilidad, calificacion, titulo_normalizado |
| Tipo de precio / calificacion | float64 / int64 |
| Precio promedio | £38.0485; mostrado como £38.05 |
| Primeros cinco títulos | A Light in the Attic; Tipping the Velvet; Soumission; Sharp Objects; Sapiens: A Brief History of Humankind |

## Buscador y ejemplos reales

Se descartan títulos normalizados nulos o vacíos antes de construir el índice.
`fit_transform()` se ejecuta una vez por instancia de `Buscador`; las consultas
reutilizan el vectorizador con `transform()`. La función `buscar(consulta)` tiene
`top_k=5` por defecto. La llamada del programa usa **`buscar(consulta, top_k=3)`**
para cumplir el desafío: solo resultados positivos, en orden descendente.

Estas fueron las salidas reales, con similitud redondeada a cuatro decimales:

**Consulta 1: `the`**

```text
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: 17.93 | Similitud: 0.4181
The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics | Precio: 22.6 | Similitud: 0.3630
The Black Maria | Precio: 52.15 | Similitud: 0.3282
```

**Consulta 2: `life`**

```text
Scott Pilgrim's Precious Little Life (Scott Pilgrim #1) | Precio: 52.29 | Similitud: 0.2459
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: 17.93 | Similitud: 0.2250
Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991 | Precio: 57.25 | Similitud: 0.2231
```

El orden cambia porque cada consulta comparte términos diferentes con los títulos.
Por ejemplo, “The Coming Woman” aparece primero con `the`, pero segundo con `life`.
Las puntuaciones no son probabilidades ni comprensión semántica.

## Validación funcional — T1 a T4

Se ejecutó `python buscador.py` en un proceso separado para cada consulta,
con el intérprete del entorno virtual. Todas finalizaron con código 0 y stderr vacío.

| Caso | Consulta | Resultado observado | Estado |
|---|---|---|---|
| T1 | `the` | Tres resultados positivos: 0.4181, 0.3630, 0.3282; títulos y precios en el ejemplo 1 | Cumple |
| T2 | `zzxyz123` | `No se encontraron coincidencias.` | Cumple |
| T3 | `THE` | Salida completa y ranking idénticos a T1; solo cambió la capitalización de la entrada | Cumple |
| T4 | [vacía] | `Ingrese una consulta no vacia.` seguido de `No se encontraron coincidencias.`; sin excepción | Cumple |

No se detectaron problemas en estos cuatro casos. También se comprobó que
`buscar('the', top_k=3)` devuelve exactamente tres resultados positivos ordenados;
la llamada por defecto permite cinco. Las pruebas automatizadas usan datos
sintéticos y carpetas temporales: no hacen peticiones ni alteran el CSV entregado.

## Respuestas 1–6

1. **BeautifulSoup y requests.** `requests` realiza la petición HTTP y obtiene la
   respuesta. BeautifulSoup analiza el HTML y permite seleccionar elementos y
   extraer sus atributos o texto; no descarga la página por sí solo.
2. **Riesgo de selectores específicos.** Si cambian las etiquetas, clases o la
   estructura del sitio, pueden dejar de encontrarse datos o extraerse campos
   incorrectos. Hay que revisar selectores, validar campos y controlar la cantidad
   extraída; las advertencias ayudan a detectar cambios.
3. **Normalización.** Quitar espacios sobrantes y unificar minúsculas evita que
   diferencias superficiales separen textos equivalentes, mejora la consistencia
   del índice y permite consultas con distinta capitalización.
4. **fit_transform y transform.** `fit_transform()` aprende el vocabulario y los
   pesos IDF de los títulos y genera su matriz TF-IDF. `transform()` representa
   la consulta en ese mismo espacio. Volver a ajustar sobre la consulta cambiaría
   el vocabulario y los pesos, impidiendo una comparación coherente.
5. **Orden y puntuación.** Primero se muestra el libro con 0.75, luego el de 0.20.
   Una puntuación cercana a cero indica poca coincidencia de términos ponderados;
   cero significa que no hay términos compartidos en el vocabulario del índice.
   No demuestra que los temas de ambos textos sean diferentes.
6. **Limitación y mejora.** Buscar solo términos de los títulos no recupera bien
   sinónimos ni conceptos ausentes del título. Una mejora concreta es incorporar
   descripciones y representar textos y consultas mediante embeddings semánticos.
   Eso ampliaría el trabajo; este laboratorio conserva TF-IDF sobre títulos.

## Git y trabajo en equipo

`.venv/`, cachés, temporales y archivos `.env` están excluidos. Verificá con:

```bash
git check-ignore .venv/pyvenv.cfg
git status --short
```

El repositorio es público; no suban contraseñas, tokens ni datos personales ajenos.
El propietario puede invitar colaboradores desde **Settings → Collaborators**.
Cada compañero clona el repositorio y crea su propio entorno; no compartan `.venv`.
Para trabajar sin pisarse, usen una rama por cambio y revisen el diff antes de subirlo.

### Antes de entregar

- Completar los nombres reales de integrantes y revisar las respuestas en grupo.
- Abrir el catálogo en el navegador y comprobar los selectores con las herramientas
  de desarrollo, como pide el paso 2. Esa inspección manual no se realizó desde este entorno.
- Repetir las consultas y entender los resultados; el catálogo puede cambiar.
