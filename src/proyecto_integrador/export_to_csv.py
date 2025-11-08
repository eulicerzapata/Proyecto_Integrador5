"""
Script de Exportación desde SQLite a CSV
=========================================

Este script exporta los datos desde la base de datos SQLite (db/proyecto.db)
a un archivo CSV (db/export.csv).

"""

import os
import sqlite3
import sys
from pathlib import Path
import pandas as pd


def exportar_tabla_a_csv(db_path, output_csv, tabla="transacciones"):
    """
    Exporta una tabla de SQLite a un archivo CSV.
    
    Args:
        db_path: Ruta a la base de datos SQLite
        output_csv: Ruta del archivo CSV de salida
        tabla: Nombre de la tabla a exportar (default: "transacciones")
    """
    # Verificar que la base de datos existe
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"La base de datos {db_path} no existe. Ejecuta primero load_to_sqlite.py")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    
    try:
        # Leer la tabla completa en un DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
        
        # Exportar a CSV
        df.to_csv(output_csv, index=False, encoding='utf-8')
        
        # Mensaje simple
        print(f" {len(df):,} registros exportados a {output_csv}")
        
    except Exception as e:
        print(f" Error durante la exportación: {e}")
        raise
    finally:
        conn.close()


def main():
    """
    Función principal que orquesta el proceso de exportación.
    """
    print("=" * 60)
    print("EXPORTACIÓN DE SQLITE A CSV")
    print("=" * 60)
    
    # Configuración de rutas
    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "db" / "proyecto.db"
    output_csv = project_root / "db" / "export.csv"
    
    try:
        # Exportar datos
        exportar_tabla_a_csv(db_path, output_csv)
        
        print("\n" + "=" * 60)
        print(" PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\nFlujo completado:")
        print(f"Kaggle Dataset")
        print(f"SQLite: {db_path}")
        print(f"CSV: {output_csv}")

    except Exception as e:
        print(f"\n Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
