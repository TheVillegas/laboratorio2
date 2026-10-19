import importlib
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import requests

from procesamiento import procesar_libros
from scraper import obtener_libros


class DatosTests(unittest.TestCase):
    def test_scraping_campos_tipos_estrellas_y_elemento_incompleto(self):
        html = ''.join(
            f'<article class="product_pod"><h3><a title=" Libro {n} ">x</a></h3>'
            f'<p class="price_color">£12.50</p><p class="instock availability"> In stock </p>'
            f'<p class="star-rating {estrella}"></p></article>'
            for n, estrella in enumerate(['One', 'Two', 'Three', 'Four', 'Five'], 1)
        ) + '<article class="product_pod"><h3>Sin datos</h3></article>'
        respuesta = Mock(text=html)
        with patch('scraper.requests.get', return_value=respuesta) as get:
            with warnings.catch_warnings(record=True) as avisos:
                warnings.simplefilter('always')
                libros = obtener_libros()
        get.assert_called_once_with('https://books.toscrape.com/', timeout=10)
        respuesta.raise_for_status.assert_called_once_with()
        self.assertEqual(len(libros), 5)
        self.assertEqual(len(avisos), 1)
        self.assertEqual(libros[0], dict(titulo='Libro 1', precio=12.5,
                                       disponibilidad='In stock', calificacion=1))
        self.assertEqual([libro['calificacion'] for libro in libros], [1, 2, 3, 4, 5])
        self.assertTrue(all(isinstance(libro['precio'], float) for libro in libros))

    def test_error_http_no_genera_datos(self):
        respuesta = Mock()
        respuesta.raise_for_status.side_effect = requests.HTTPError('503')
        with patch('scraper.requests.get', return_value=respuesta):
            with self.assertRaises(requests.HTTPError):
                obtener_libros()

    def test_importar_no_realiza_peticiones(self):
        with patch('requests.get') as get:
            importlib.reload(importlib.import_module('scraper'))
            importlib.reload(importlib.import_module('procesamiento'))
        get.assert_not_called()

    def test_limpieza_indicadores_y_csv_utf8_sin_indice(self):
        registros = [dict(titulo='  Árbol   azul ', precio='10.50',
                          disponibilidad=' In stock ', calificacion='3'),
                     dict(titulo='Árbol azul', precio=99, disponibilidad='In stock', calificacion=1),
                     dict(titulo='Otro', precio=20.5, disponibilidad='In stock', calificacion=5)]
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / 'libros.csv'
            df = procesar_libros(registros, archivo)
            guardado = pd.read_csv(archivo)
            self.assertIn('Árbol azul', archivo.read_text(encoding='utf-8'))
        self.assertEqual(list(guardado.columns), ['titulo', 'precio', 'disponibilidad',
                                                'calificacion', 'titulo_normalizado'])
        self.assertEqual(df['titulo_normalizado'].tolist(), ['árbol azul', 'otro'])
        self.assertEqual(df['disponibilidad'].tolist(), ['In stock', 'In stock'])
        self.assertEqual(df.shape, (2, 5))
        self.assertAlmostEqual(df['precio'].mean(), 15.5)
        self.assertEqual(df['precio'].dtype.kind, 'f')
        self.assertEqual(df['calificacion'].dtype.kind, 'i')


if __name__ == '__main__':
    unittest.main()
