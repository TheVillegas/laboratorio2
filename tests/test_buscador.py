import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from buscador import Buscador


class BuscadorTests(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        archivo = Path(self.carpeta.name) / 'libros.csv'
        titulos = ['Music', 'Music and life', 'Music and art', 'Music history', 'Travel', None, '  ']
        pd.DataFrame({'titulo': titulos, 'precio': [10.0] * 7,
                      'titulo_normalizado': titulos}).to_csv(archivo, index=False)
        self.buscador = Buscador(archivo)

    def test_t1_positivos_ordenados_titulo_precio_y_similitud(self):
        resultados = self.buscador.buscar('music')
        self.assertEqual(len(resultados), 4)
        self.assertEqual(resultados[0]['titulo'], 'Music')
        self.assertEqual(resultados[0]['precio'], 10.0)
        puntuaciones = [r['similitud'] for r in resultados]
        self.assertEqual(puntuaciones, sorted(puntuaciones, reverse=True))
        self.assertTrue(all(0 < valor <= 1 for valor in puntuaciones))

    def test_t2_termino_inexistente(self):
        self.assertEqual(self.buscador.buscar('zzxyz123'), [])

    def test_t3_mayusculas_ranking_equivalente(self):
        self.assertEqual(self.buscador.buscar('music'), self.buscador.buscar('MUSIC'))

    def test_t4_vacia_mensaje_sin_excepcion(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            resultados = self.buscador.buscar('   ')
        self.assertEqual(resultados, [])
        self.assertEqual(salida.getvalue(), 'Ingrese una consulta no vacia.\n')

    def test_desafio_top_tres(self):
        resultados = self.buscador.buscar('music', top_k=3)
        self.assertEqual(len(resultados), 3)
        self.assertTrue(all(r['similitud'] > 0 for r in resultados))

    def test_cli_cuatro_casos_sin_modificar_csv(self):
        carpeta = Path(self.carpeta.name)
        shutil.copyfile(Path(__file__).resolve().parents[1] / 'buscador.py', carpeta / 'buscador.py')
        archivo = carpeta / 'libros.csv'
        original = archivo.read_bytes()
        salidas = {}
        for consulta in ['music', 'MUSIC', 'zzxyz123', '']:
            proceso = subprocess.run([sys.executable, str(carpeta / 'buscador.py')],
                                     input=consulta + '\n', capture_output=True, text=True,
                                     cwd=carpeta, timeout=15)
            self.assertEqual(proceso.returncode, 0)
            self.assertEqual(proceso.stderr, '')
            self.assertEqual(archivo.read_bytes(), original)
            salidas[consulta] = proceso.stdout
        self.assertEqual(salidas['music'], salidas['MUSIC'])
        self.assertEqual(salidas['music'].count(' | Similitud: '), 3)
        esperada = 'Ingrese una palabra o titulo: '
        esperada += ''.join(f"{r['titulo']} | Precio: {r['precio']} | Similitud: {r['similitud']:.4f}\n"
                            for r in self.buscador.buscar('music', top_k=3))
        self.assertEqual(salidas['music'], esperada)
        self.assertEqual(salidas['zzxyz123'],
                         'Ingrese una palabra o titulo: No se encontraron coincidencias.\n')
        self.assertEqual(salidas[''], 'Ingrese una palabra o titulo: '
                         'Ingrese una consulta no vacia.\nNo se encontraron coincidencias.\n')

    def test_sin_titulos_validos_informa_problema(self):
        archivo = Path(self.carpeta.name) / 'vacio.csv'
        pd.DataFrame({'titulo': [''], 'precio': [10],
                      'titulo_normalizado': ['']}).to_csv(archivo, index=False)
        with self.assertRaisesRegex(ValueError, 'No hay títulos válidos'):
            Buscador(archivo)


if __name__ == '__main__':
    unittest.main()
