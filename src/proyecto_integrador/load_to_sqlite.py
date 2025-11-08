"""
Script de Carga de Datos a SQLite
===================================

Este script descarga el dataset de transacciones de tarjetas de crédito desde Kaggle
y lo carga en una base de datos SQLite (db/proyecto.db).


"""

import os
import sqlite3
import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar Ingestar
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.proyecto_integrador.ingestar import Ingestar


def insertar_datos(conn, df):
    """
    Inserta los datos del DataFrame en la tabla de transacciones.
    
    Args:
        conn: Conexión a la base de datos SQLite
        df: DataFrame con los datos a insertar
    """
    # Insertar datos usando pandas
    df.to_sql('transacciones', conn, if_exists='replace', index=False)
    print(f" {len(df):,} registros insertados en la base de datos")


def cargar_desde_directorio(data_dir, db_path):
    """
    Carga datos desde un directorio con archivos CSV a SQLite.
    
    Args:
        data_dir: Directorio con los archivos CSV
        db_path: Ruta a la base de datos SQLite
    
    Returns:
        Número de registros insertados
    """
    import pandas as pd
    import os
    
    # Buscar archivos CSV
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f'No se encontraron archivos CSV en {data_dir}')
    
    # Leer y concatenar todos los CSV
    dfs = []
    for csv_file in csv_files:
        path = os.path.join(data_dir, csv_file)
        print(f'Leyendo {path}...')
        df_tmp = pd.read_csv(path, low_memory=False)
        dfs.append(df_tmp)
    
    df_all = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    if df_all.empty:
        print('No hay datos para cargar.')
        return 0
    
    # Conectar y cargar
    conn = sqlite3.connect(db_path, timeout=60)
    insertar_datos(conn, df_all)
    conn.close()
    
    return len(df_all)


def main():
    """
    Función principal - ejecuta el proceso completo desde cero.
    """
    print("=" * 60)
    print("CARGA DE DATOS A SQLITE")
    print("=" * 60)
    
    # Configuración de rutas
    db_dir = project_root / "db"
    db_path = db_dir / "proyecto.db"
    
    # Crear directorio db si no existe
    db_dir.mkdir(exist_ok=True)
    
    # Inicializar la clase Ingestar
    ingestar = Ingestar()
    
    try:
        # Descargar y extraer
        print("\n Descargando dataset desde Kaggle...")
        kaggle_ref = "priyamchoksi/credit-card-transactions-dataset"
        dataset_path = ingestar.download_dataset_zip(kaggle_ref)
        
        print("\n Procesando archivos descargados...")
        data_dir = ingestar.extract_zip_files(dataset_path)
        
        # Cargar a SQLite
        print(f"\n Cargando datos a {db_path}...")
        count = cargar_desde_directorio(data_dir, db_path)
        
        print("\n" + "=" * 60)
        print(" PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"Base de datos: {db_path}")
        print(f"Total de registros: {count:,}")
        
    except Exception as e:
        print(f"\n Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
