"""
Módulo de Limpieza de Datos - Proyecto Integrador 5
====================================================

Este módulo realiza la limpieza y enriquecimiento del dataset enfocado
en las variables necesarias para el análisis de transacciones por género
y ubicación geográfica.

COLUMNAS SELECCIONADAS (13 originales + 5 derivadas = 18 total):

ORIGINALES:
1. trans_num              - ID único de transacción
2. trans_date_trans_time  - Fecha y hora completa
3. gender                 - Género del titular
4. city                   - Ciudad del titular
5. state                  - Estado del titular (abreviatura)
6. lat                    - Latitud del titular
7. long                   - Longitud del titular
8. city_pop               - Población de la ciudad
9. merchant               - Nombre del comercio
10. category              - Categoría del comercio
11. amt                   - Monto de la transacción
12. merch_lat             - Latitud del comercio
13. merch_long            - Longitud del comercio

DERIVADAS:
14. state_name            - Nombre completo del estado
15. anio                  - Año de la transacción
16. mes                   - Mes (1-12)
17. dia                   - Día del mes (1-31)
18. hora                  - Hora del día (0-23)

Autor: Proyecto Integrador 5
Fecha: 2025-11-22
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict


class LimpiadorDatos:
    """
    Limpiador de datos enfocado en las variables del análisis.
    """
    
    # Columnas que necesitamos del dataset original
    COLUMNAS_NECESARIAS = [
        'trans_num',              # ID único
        'trans_date_trans_time',  # Fecha y hora
        'gender',                 # Género
        'city',                   # Ciudad
        'state',                  # Estado
        'lat',                    # Latitud usuario
        'long',                   # Longitud usuario
        'city_pop',               # Población ciudad
        'merchant',               # Nombre comercio
        'category',               # Categoría comercio
        'amt',                    # Monto
        'merch_lat',              # Latitud comercio
        'merch_long',             # Longitud comercio
    ]
    
    # Columnas temporales que vamos a crear
    COLUMNAS_TEMPORALES = ['anio', 'mes', 'dia', 'hora']
    
    # Mapeo de abreviaturas de estados a nombres completos
    STATE_NAMES = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el limpiador con un DataFrame.
        
        Args:
            df: DataFrame completo del dataset
        """
        self.df_original = df.copy()
        self.df_limpio = None
        self.reporte = {
            'filas_originales': len(df),
            'columnas_originales': len(df.columns),
            'columnas_seleccionadas': len(self.COLUMNAS_NECESARIAS),
            'duplicados_eliminados': 0,
            'nulos_procesados': {},
            'columnas_agregadas': [],
            'filas_finales': 0,
            'columnas_finales': 0
        }
    
    def seleccionar_columnas(self) -> 'LimpiadorDatos':
        """
        Selecciona solo las columnas necesarias para el análisis.
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 1] Seleccionando columnas necesarias para el analisis")
        print(f"   - Filas totales: {len(self.df_original):,}")
        
        # Verificar que todas las columnas existen
        columnas_faltantes = [col for col in self.COLUMNAS_NECESARIAS 
                             if col not in self.df_original.columns]
        
        if columnas_faltantes:
            print(f"   ADVERTENCIA: Columnas faltantes: {columnas_faltantes}")
            columnas_disponibles = [col for col in self.COLUMNAS_NECESARIAS 
                                   if col in self.df_original.columns]
        else:
            columnas_disponibles = self.COLUMNAS_NECESARIAS
        
        # Seleccionar solo las columnas necesarias
        self.df_limpio = self.df_original[columnas_disponibles].copy()
        
        print(f"   - Columnas seleccionadas: {len(columnas_disponibles)} de {len(self.df_original.columns)} originales")
        print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        return self
    
    def eliminar_duplicados(self) -> 'LimpiadorDatos':
        """
        Elimina filas duplicadas basándose en trans_num.
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 2] Eliminando transacciones duplicadas")
        print("   - Criterio: Numero de transaccion (trans_num)")
        
        filas_antes = len(self.df_limpio)
        
        if 'trans_num' in self.df_limpio.columns:
            self.df_limpio.drop_duplicates(subset=['trans_num'], keep='first', inplace=True)
            duplicados = filas_antes - len(self.df_limpio)
            self.reporte['duplicados_eliminados'] = duplicados
            
            print(f"   - Filas duplicadas encontradas: {duplicados:,}")
            print(f"   - Filas eliminadas: {duplicados:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        else:
            print("   ADVERTENCIA: Columna 'trans_num' no encontrada")
        
        return self
    
    def limpiar_gender(self) -> 'LimpiadorDatos':
        """
        Limpia la columna gender.
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 3] Limpiando columna 'gender' (genero del titular)")
        
        if 'gender' not in self.df_limpio.columns:
            print("   ADVERTENCIA: Columna 'gender' no encontrada")
            return self
        
        filas_antes = len(self.df_limpio)
        nulos_antes = self.df_limpio['gender'].isnull().sum()
        
        # Contar valores que necesitan transformación
        valores_originales = self.df_limpio['gender'].copy()
        
        print(f"   - Transformacion: Convertir a mayusculas y eliminar espacios")
        print(f"   - Valores nulos encontrados: {nulos_antes:,}")
        
        # Convertir a mayúsculas y limpiar
        self.df_limpio['gender'] = self.df_limpio['gender'].str.strip().str.upper()
        
        # Contar cuántos valores fueron transformados
        valores_transformados = (valores_originales != self.df_limpio['gender']).sum()
        print(f"   - Valores transformados a mayusculas: {valores_transformados:,}")
        
        # Eliminar filas con gender nulo o inválido
        valores_validos = ['M', 'F']
        print(f"   - Valores validos: {valores_validos}")
        
        # Contar valores inválidos antes de eliminar
        valores_invalidos = (~self.df_limpio['gender'].isin(valores_validos)).sum()
        print(f"   - Valores invalidos encontrados: {valores_invalidos:,}")
        
        self.df_limpio = self.df_limpio[self.df_limpio['gender'].isin(valores_validos)]
        filas_eliminadas = filas_antes - len(self.df_limpio)
        
        self.reporte['nulos_procesados']['gender'] = {
            'antes': nulos_antes,
            'filas_eliminadas': filas_eliminadas,
            'accion': 'eliminar_invalidos'
        }
        
        print(f"   - Filas eliminadas: {filas_eliminadas:,}")
        print(f"   - Filas aceptadas: {len(self.df_limpio):,}")

        
        return self
    
    def limpiar_ubicacion(self) -> 'LimpiadorDatos':
        """
        Limpia las columnas de ubicación (city, state, lat, long, city_pop).
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 4] Limpiando columnas de ubicacion")
        
        # City
        if 'city' in self.df_limpio.columns:
            print("\n   [4.1] Procesando columna 'city' (ciudad del titular)")
            nulos_antes = self.df_limpio['city'].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            # Guardar valores originales para comparar
            valores_originales = self.df_limpio['city'].copy()
            
            print(f"   - Transformacion: Capitalizar primera letra de cada palabra (Title Case)")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio['city'].notna()]
            
            # Normalizar texto (Title Case para ciudades)
            self.df_limpio['city'] = self.df_limpio['city'].str.strip().str.title()
            
            # Contar transformaciones
            valores_transformados = (valores_originales[self.df_limpio.index] != self.df_limpio['city']).sum()
            print(f"   - Valores transformados (capitalizados): {valores_transformados:,}")
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            ciudades_unicas = self.df_limpio['city'].nunique()
            
            self.reporte['nulos_procesados']['city'] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
            print(f"   - Ciudades unicas: {ciudades_unicas:,}")
        
        # State (mantener en mayúsculas para coincidir con el diccionario)
        if 'state' in self.df_limpio.columns:
            print("\n   [4.2] Procesando columna 'state' (estado del titular - abreviatura)")
            nulos_antes = self.df_limpio['state'].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            # Guardar valores originales para comparar
            valores_originales = self.df_limpio['state'].copy()
            
            print(f"   - Transformacion: Convertir a MAYUSCULAS (para mapeo posterior)")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio['state'].notna()]
            
            # Normalizar texto (MAYÚSCULAS para estados)
            self.df_limpio['state'] = self.df_limpio['state'].str.strip().str.upper()
            
            # Contar transformaciones
            valores_transformados = (valores_originales[self.df_limpio.index] != self.df_limpio['state']).sum()
            print(f"   - Valores transformados a MAYUSCULAS: {valores_transformados:,}")
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            estados_unicos = self.df_limpio['state'].nunique()
            
            self.reporte['nulos_procesados']['state'] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
            print(f"   - Estados unicos: {estados_unicos}")
        
        # Coordenadas (lat, long)
        for col in ['lat', 'long']:
            if col not in self.df_limpio.columns:
                continue
            
            nombre_col = "latitud" if col == 'lat' else "longitud"
            print(f"\n   [4.{3 if col == 'lat' else 4}] Procesando columna '{col}' ({nombre_col} del titular)")
            nulos_antes = self.df_limpio[col].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            print(f"   - Transformacion: Convertir a numerico")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Convertir a numérico
            self.df_limpio[col] = pd.to_numeric(self.df_limpio[col], errors='coerce')
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio[col].notna()]
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            
            self.reporte['nulos_procesados'][col] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        # Población de ciudad
        if 'city_pop' in self.df_limpio.columns:
            print("\n   [4.5] Procesando columna 'city_pop' (poblacion de la ciudad)")
            nulos_antes = self.df_limpio['city_pop'].isnull().sum()
            invalidos_antes = (self.df_limpio['city_pop'] <= 0).sum()
            filas_antes = len(self.df_limpio)
            
            print(f"   - Transformacion: Convertir a numerico y eliminar valores <= 0")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Convertir a numérico
            self.df_limpio['city_pop'] = pd.to_numeric(self.df_limpio['city_pop'], errors='coerce')
            
            # Eliminar nulos o valores <= 0
            self.df_limpio = self.df_limpio[
                (self.df_limpio['city_pop'].notna()) & 
                (self.df_limpio['city_pop'] > 0)
            ]
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            
            self.reporte['nulos_procesados']['city_pop'] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos_y_negativos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        return self
    
    def enriquecer_estado_nombre(self) -> 'LimpiadorDatos':
        """
        Enriquece con una nueva columna 'state_name' que contiene el nombre completo del estado.
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 5] Enriqueciendo con nombres completos de estados")
        print("   - Nueva columna: 'state_name'")
        
        if 'state' not in self.df_limpio.columns:
            print("   ADVERTENCIA: Columna 'state' no encontrada")
            return self
        
        filas_antes = len(self.df_limpio)
        estados_unicos_antes = self.df_limpio['state'].nunique()
        
        print(f"   - Estados unicos (abreviaturas): {estados_unicos_antes}")
        print(f"   - Mapeo: Abreviatura (ej: NY) -> Nombre completo (ej: New York)")
        
        # Crear la columna state_name mapeando las abreviaturas
        self.df_limpio['state_name'] = self.df_limpio['state'].map(self.STATE_NAMES)
        
        # Verificar si hay estados sin mapear
        estados_sin_mapear = self.df_limpio[self.df_limpio['state_name'].isna()]['state'].unique()
        
        if len(estados_sin_mapear) > 0:
            print(f"   ADVERTENCIA: Estados sin mapear encontrados: {list(estados_sin_mapear)}")
            # Eliminar filas con estados no reconocidos
            self.df_limpio = self.df_limpio[self.df_limpio['state_name'].notna()]
            filas_eliminadas = filas_antes - len(self.df_limpio)
            print(f"   - Filas eliminadas (estados no reconocidos): {filas_eliminadas:,}")
        
        # Agregar a las columnas agregadas
        if 'state_name' not in self.reporte['columnas_agregadas']:
            self.reporte['columnas_agregadas'].append('state_name')
        
        print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        # Mostrar algunos ejemplos
        print(f"\n   Ejemplos de mapeo:")
        ejemplos = self.df_limpio[['state', 'state_name']].drop_duplicates().head(5)
        for _, row in ejemplos.iterrows():
            print(f"      {row['state']} -> {row['state_name']}")

        
        return self
    
    def limpiar_comercio(self) -> 'LimpiadorDatos':
        """
        Limpia las columnas de comercio (merchant, category, merch_lat, merch_long).
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 6] Limpiando columnas de comercio")
        
        # Merchant
        if 'merchant' in self.df_limpio.columns:
            print("\n   [6.1] Procesando columna 'merchant' (nombre del comercio)")
            nulos_antes = self.df_limpio['merchant'].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            # Guardar valores originales para comparar
            valores_originales = self.df_limpio['merchant'].copy()
            
            print(f"   - Transformacion: Eliminar espacios en blanco al inicio/final")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio['merchant'].notna()]
            
            # Normalizar texto
            self.df_limpio['merchant'] = self.df_limpio['merchant'].str.strip()
            
            # Contar transformaciones (valores con espacios al inicio/final)
            valores_con_espacios = (valores_originales[self.df_limpio.index] != self.df_limpio['merchant']).sum()
            print(f"   - Valores con espacios en blanco eliminados: {valores_con_espacios:,}")
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            comercios_unicos = self.df_limpio['merchant'].nunique()
            
            self.reporte['nulos_procesados']['merchant'] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
            print(f"   - Comercios unicos: {comercios_unicos:,}")
        
        # Category
        if 'category' in self.df_limpio.columns:
            print("\n   [6.2] Procesando columna 'category' (categoria del comercio)")
            nulos_antes = self.df_limpio['category'].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            # Guardar valores originales para comparar
            valores_originales = self.df_limpio['category'].copy()
            
            print(f"   - Transformacion: Convertir a minusculas y eliminar espacios")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio['category'].notna()]
            
            # Normalizar texto
            self.df_limpio['category'] = self.df_limpio['category'].str.strip().str.lower()
            
            # Contar transformaciones
            valores_transformados = (valores_originales[self.df_limpio.index] != self.df_limpio['category']).sum()
            print(f"   - Valores transformados a minusculas: {valores_transformados:,}")
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            categorias_unicas = self.df_limpio['category'].nunique()
            
            self.reporte['nulos_procesados']['category'] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
            print(f"   - Categorias unicas: {categorias_unicas}")
        
        # Coordenadas del comercio
        for col in ['merch_lat', 'merch_long']:
            if col not in self.df_limpio.columns:
                continue
            
            nombre_col = "latitud" if col == 'merch_lat' else "longitud"
            print(f"\n   [6.{3 if col == 'merch_lat' else 4}] Procesando columna '{col}' ({nombre_col} del comercio)")
            nulos_antes = self.df_limpio[col].isnull().sum()
            filas_antes = len(self.df_limpio)
            
            print(f"   - Transformacion: Convertir a numerico")
            print(f"   - Valores nulos encontrados: {nulos_antes:,}")
            
            # Convertir a numérico
            self.df_limpio[col] = pd.to_numeric(self.df_limpio[col], errors='coerce')
            
            # Eliminar nulos
            self.df_limpio = self.df_limpio[self.df_limpio[col].notna()]
            
            filas_eliminadas = filas_antes - len(self.df_limpio)
            
            self.reporte['nulos_procesados'][col] = {
                'antes': nulos_antes,
                'filas_eliminadas': filas_eliminadas,
                'accion': 'eliminar_nulos'
            }
            
            print(f"   - Filas eliminadas: {filas_eliminadas:,}")
            print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        return self
    
    def limpiar_monto(self) -> 'LimpiadorDatos':
        """
        Limpia la columna amt (monto).
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 7] Limpiando columna 'amt' (monto de la transaccion)")
        
        if 'amt' not in self.df_limpio.columns:
            print("   ADVERTENCIA: Columna 'amt' no encontrada")
            return self
        
        nulos_antes = self.df_limpio['amt'].isnull().sum()
        filas_antes = len(self.df_limpio)
        
        print(f"   - Transformacion: Convertir a numerico y eliminar valores <= 0")
        print(f"   - Valores nulos encontrados: {nulos_antes:,}")
        
        # Convertir a numérico
        self.df_limpio['amt'] = pd.to_numeric(self.df_limpio['amt'], errors='coerce')
        
        # Eliminar nulos o valores <= 0
        self.df_limpio = self.df_limpio[
            (self.df_limpio['amt'].notna()) & 
            (self.df_limpio['amt'] > 0)
        ]
        filas_eliminadas = filas_antes - len(self.df_limpio)
        
        self.reporte['nulos_procesados']['amt'] = {
            'antes': nulos_antes,
            'filas_eliminadas': filas_eliminadas,
            'accion': 'eliminar_nulos_y_negativos'
        }
        
        print(f"   - Filas eliminadas: {filas_eliminadas:,}")
        print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        # Estadísticas
        print(f"   - Estadisticas de monto:")
        print(f"      Minimo: ${self.df_limpio['amt'].min():.2f}")
        print(f"      Maximo: ${self.df_limpio['amt'].max():.2f}")
        print(f"      Promedio: ${self.df_limpio['amt'].mean():.2f}")
        print(f"      Mediana: ${self.df_limpio['amt'].median():.2f}")
        
        return self
    
    def enriquecer_fechas(self) -> 'LimpiadorDatos':
        """
        Enriquece con columnas temporales: anio, mes, dia, hora.
        
        Returns:
            self para encadenamiento
        """
        print("\n[PASO 8] Enriqueciendo con columnas temporales")
        print("   - Nuevas columnas: anio, mes, dia, hora")
        
        if 'trans_date_trans_time' not in self.df_limpio.columns:
            print("   ADVERTENCIA: Columna 'trans_date_trans_time' no encontrada")
            return self
        
        filas_antes = len(self.df_limpio)
        
        print(f"   - Transformacion: Extraer componentes de fecha/hora")
        
        # Convertir a datetime
        self.df_limpio['trans_date_trans_time'] = pd.to_datetime(
            self.df_limpio['trans_date_trans_time'], 
            errors='coerce'
        )
        
        # Eliminar fechas inválidas
        fechas_invalidas = self.df_limpio['trans_date_trans_time'].isnull().sum()
        self.df_limpio = self.df_limpio[self.df_limpio['trans_date_trans_time'].notna()]
        filas_eliminadas = filas_antes - len(self.df_limpio)
        
        if fechas_invalidas > 0:
            print(f"   - Fechas invalidas encontradas: {fechas_invalidas:,}")
        
        print(f"   - Filas eliminadas: {filas_eliminadas:,}")
        
        # Crear columnas temporales
        self.df_limpio['anio'] = self.df_limpio['trans_date_trans_time'].dt.year
        self.df_limpio['mes'] = self.df_limpio['trans_date_trans_time'].dt.month
        self.df_limpio['dia'] = self.df_limpio['trans_date_trans_time'].dt.day
        self.df_limpio['hora'] = self.df_limpio['trans_date_trans_time'].dt.strftime('%I:%M:%S %p')
             
        self.reporte['columnas_agregadas'] = self.COLUMNAS_TEMPORALES.copy()
        
        print(f"   - Filas aceptadas: {len(self.df_limpio):,}")
        
        # Rango de fechas
        fecha_min = self.df_limpio['trans_date_trans_time'].min()
        fecha_max = self.df_limpio['trans_date_trans_time'].max()
        print(f"   - Rango de fechas:")
        print(f"      Desde: {fecha_min}")
        print(f"      Hasta: {fecha_max}")
        
        # Distribución por año
        anios_unicos = self.df_limpio['anio'].nunique()
        print(f"   - Anos unicos en el dataset: {anios_unicos}")
        
        return self
    
    def obtener_dataframe_limpio(self) -> pd.DataFrame:
        """
        Retorna el DataFrame limpio.
        
        Returns:
            DataFrame procesado
        """
        return self.df_limpio.copy()
    
    def generar_reporte(self) -> Dict:
        """
        Genera un reporte completo de la limpieza.
        
        Returns:
            Diccionario con estadísticas
        """
        self.reporte['filas_finales'] = len(self.df_limpio)
        self.reporte['columnas_finales'] = len(self.df_limpio.columns)
        return self.reporte
    
    def imprimir_reporte(self):
        """
        Imprime un reporte formateado de la limpieza.
        """
        print("\n" + "=" * 70)
        print("REPORTE DE LIMPIEZA DE DATOS")
        print("=" * 70)
        
        print(f"\nDIMENSIONES:")
        print(f"   - Filas originales:    {self.reporte['filas_originales']:,}")
        print(f"   - Filas finales:       {self.reporte['filas_finales']:,}")
        print(f"   - Filas eliminadas:    {self.reporte['filas_originales'] - self.reporte['filas_finales']:,}")
        print(f"   - Columnas originales: {self.reporte['columnas_originales']}")
        print(f"   - Columnas finales:    {self.reporte['columnas_finales']}")
        
        if self.reporte['duplicados_eliminados'] > 0:
            print(f"\nDUPLICADOS ELIMINADOS: {self.reporte['duplicados_eliminados']:,}")
        
        if self.reporte['nulos_procesados']:
            print(f"\nVALORES NULOS/INVALIDOS PROCESADOS:")
            total_eliminadas = sum(info['filas_eliminadas'] for info in self.reporte['nulos_procesados'].values())
            print(f"   - Total de filas eliminadas por nulos/invalidos: {total_eliminadas:,}")
        
        if self.reporte['columnas_agregadas']:
            print(f"\nCOLUMNAS DERIVADAS AGREGADAS:")
            for col in self.reporte['columnas_agregadas']:
                print(f"   - {col}")
        
        print("\nCOLUMNAS FINALES:")
        if self.df_limpio is not None:
            for col in self.df_limpio.columns:
                print(f"   - {col}")
        
        print("\n" + "=" * 70)
    
    def guardar_dataset_limpio(self, ruta: str) -> None:
        """
        Guarda el dataset limpio en un archivo CSV.
        
        Args:
            ruta: Ruta donde guardar el archivo CSV
        """
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
        self.df_limpio.to_csv(ruta, index=False, encoding='utf-8')
        print(f"\nDataset limpio guardado en: {ruta}")
        print(f"   - {len(self.df_limpio):,} filas x {len(self.df_limpio.columns)} columnas")


def limpiar_dataset(df: pd.DataFrame, guardar_en: str = None) -> pd.DataFrame:
    """
    Función principal para limpiar el dataset.
    
    Args:
        df: DataFrame original
        guardar_en: Ruta donde guardar el dataset limpio (opcional)
    
    Returns:
        DataFrame limpio y enriquecido
    """
    print("\n" + "=" * 70)
    print("LIMPIEZA DE DATOS - PROYECTO INTEGRADOR 5")
    print("=" * 70)
    
    print("\nVariables del analisis:")
    print("   - gender, city, state, lat, long, city_pop")
    print("   - merchant, category, merch_lat, merch_long")
    print("   - amt, trans_date_trans_time")
    print("   - Derivadas: state_name, anio, mes, dia, hora")
    
    # Crear instancia del limpiador
    limpiador = LimpiadorDatos(df)
    
    # Ejecutar pipeline de limpieza
    limpiador \
        .seleccionar_columnas() \
        .eliminar_duplicados() \
        .limpiar_gender() \
        .limpiar_ubicacion() \
        .enriquecer_estado_nombre() \
        .limpiar_comercio() \
        .limpiar_monto() \
        .enriquecer_fechas()
    
    # Generar e imprimir reporte
    limpiador.generar_reporte()
    limpiador.imprimir_reporte()
    
    # Guardar si se especifica ruta
    if guardar_en:
        limpiador.guardar_dataset_limpio(guardar_en)
    
    print("\n" + "=" * 70)
    print("LIMPIEZA COMPLETADA")
    print("=" * 70 + "\n")
    
    return limpiador.obtener_dataframe_limpio()


def main():
    """
    Función principal para ejecutar desde línea de comandos.
    Busca el archivo descargado de Kaggle y ejecuta la limpieza.
    """
    import os
    import sys
    
    print("\n" + "=" * 70)
    print("LIMPIEZA DE DATOS - PROYECTO INTEGRADOR 5")
    print("=" * 70)
    
    # Determinar la ruta del proyecto
    project_root = Path(__file__).parent.parent.parent
    
    # Buscar el archivo CSV de entrada
    print("\nBuscando archivo CSV de entrada...")
    
    csv_file = None
    
    # 1. Intentar cargar desde csv/export.csv (Prioridad solicitada)
    export_csv = project_root / 'csv' / 'export.csv'
    
    if export_csv.exists():
        csv_file = export_csv
        print(f"   - Archivo encontrado (exportado): {csv_file}")
    else:
        # 2. Buscar en Kaggle cache si no existe el exportado
        print("   - 'csv/export.csv' no encontrado. Buscando en cache de Kaggle...")
        kaggle_cache = Path.home() / '.cache' / 'kagglehub' / 'datasets' / 'priyamchoksi' / 'credit-card-transactions-dataset' / 'versions' / '1'
        
        if kaggle_cache.exists() and kaggle_cache.is_dir():
            archivos_csv = list(kaggle_cache.glob('*.csv'))
            if archivos_csv:
                csv_file = archivos_csv[0]
                print(f"   - Archivo encontrado (Kaggle cache): {csv_file}")
    
    if csv_file is None:
        print("\nERROR: No se encontro ningun archivo CSV de entrada valido.")
        print("   - Se busco en: csv/export.csv")
        print("   - Se busco en: cache de Kaggle")
        return 1
    

    
    # Cargar el dataset
    print(f"\nCargando dataset...")
    try:
        df_original = pd.read_csv(csv_file, low_memory=False)
        print(f"   - Dataset cargado:")
        print(f"      Filas: {len(df_original):,}")
        print(f"      Columnas: {len(df_original.columns)}")
    except Exception as e:
        print(f"\nERROR al cargar el archivo: {e}")
        return 1
    
    # Ejecutar limpieza
    print(f"\nEjecutando limpieza...")
    try:
        ruta_salida = project_root / 'data' / 'dataset_enriquecido.csv'
        df_limpio = limpiar_dataset(
            df=df_original,
            guardar_en=str(ruta_salida)
        )
        
        print("\n" + "=" * 70)
        print("PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 70)
        
        print(f"\nArchivo generado:")
        print(f"   - {ruta_salida}")
        
        print(f"\nResumen:")
        print(f"   - Filas originales: {len(df_original):,}")
        print(f"   - Filas finales: {len(df_limpio):,}")
        print(f"   - Columnas finales: {len(df_limpio.columns)}")
        
        print("\n" + "=" * 70 + "\n")
        return 0
        
    except Exception as e:
        print(f"\nERROR durante la limpieza: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nADVERTENCIA: Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
