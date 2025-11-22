"""
Proyecto Integrador 5 - Análisis de Transacciones de Tarjetas de Crédito
=========================================================================

Módulos disponibles:
- ingestar: Descarga y extracción de datasets desde Kaggle
- limpiar_datos: Limpieza y enriquecimiento de datos ⭐
- load_to_sqlite: Carga de datos a base de datos SQLite
- export_to_csv: Exportación de datos desde SQLite a CSV
"""

from .ingestar import Ingestar
from .limpiar_datos import LimpiadorDatos, limpiar_dataset

__all__ = [
    'Ingestar',
    'LimpiadorDatos',
    'limpiar_dataset'
]

__version__ = '2.0.0'
