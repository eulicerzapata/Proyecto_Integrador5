# Proyecto Integrado 5 – Análisis de Transacciones con Tarjetas de Crédito 💳

## � Resumen (Abstract)

El presente proyecto surge de la necesidad de comprender cómo se comportan los usuarios de tarjetas de crédito a partir de la información disponible en registros reales de transacciones. Este tipo de análisis es útil para comercios y analistas que requieren identificar zonas de mayor actividad, identificación de género, y características del uso cotidiano de los servicios financieros. 

Para este estudio se utilizó el **Credit Card Transactions Dataset**, obtenido de la plataforma pública Kaggle y descargado en noviembre de 2025. El conjunto de datos incluye información sobre el monto de cada transacción, la fecha en que fue realizada, la categoría del comercio, el nombre del establecimiento, la ubicación geográfica, género y otros datos asociados a cada operación, suficientes para realizar un análisis descriptivo del comportamiento transaccional.

El propósito del proyecto es analizar estas transacciones para identificar los lugares donde compran los usuarios, los tipos de comercios que frecuentan, los montos que suelen gastar y el género que mayor gasta. El estudio del dataset se realizará mediante un análisis exploratorio, empleando técnicas descriptivas y visualizaciones que permiten identificar patrones y posibles anomalías presentes en el conjunto de datos.

Los resultados permitirán una mejor comprensión del uso de tarjetas de crédito en diferentes contextos de consumo, ofreciendo información relevante para la toma de decisiones y el entendimiento del comportamiento financiero de los usuarios.

**Palabras clave:** transacciones, Kaggle, tarjetas de crédito, análisis exploratorio, comercios, género, ubicación geográfica.

---

## 🎯 Objetivos

### Objetivo General
Analizar las transacciones bancarias en función del género y la ubicación geográfica de los titulares.

### Objetivos Específicos
1. Seleccionar y comprender el dataset utilizado, incluyendo la fuente de datos de Kaggle.
2. Identificar y describir las variables relevantes del conjunto de datos.
3. Diseñar y construir una base de datos en SQLite que permita almacenar y consultar las transacciones.
4. Realizar el flujo del dataset → SQLite → CSV mediante procesos de carga y exportación.
5. Documentar el proceso y elaborar el documento en formato APA.

---

## 📘 1. Definición del problema / Caso de uso

El uso de tarjetas de crédito genera diariamente un gran volumen de transacciones que contienen información clave sobre el comportamiento de compra de los usuarios. Sin embargo, muchas instituciones, comercios y analistas carecen de una comprensión clara sobre cómo, dónde y en qué categorías de comercio se realizan estas transacciones, lo que dificulta realizar un análisis de género y ubicación geográfica, así como identificar zonas de mayor actividad comercial. Esta falta de conocimiento limita la capacidad de tomar decisiones informadas relacionadas con estrategias comerciales, segmentación de clientes y tendencias relevantes en el consumo.

El presente proyecto aborda esta necesidad mediante el análisis del **Credit Card Transactions Dataset**, un conjunto de datos público obtenido de la plataforma Kaggle y descargado en noviembre de 2025. Este dataset contiene información sobre montos transaccionados, fechas de las operaciones, categorías de comercio, nombres de establecimientos, datos de ubicación geográfica y género asociados a cada registro. Estos atributos permiten realizar un análisis descriptivo del comportamiento transaccional sin necesidad de técnicas predictivas o modelos avanzados.

El caso de uso se centra en examinar:
-  Cómo se distribuyen las transacciones según ubicación y tipo de comercio
-  Diferencias de comportamiento por género
-  Zonas geográficas de mayor actividad comercial

Con ello se busca generar una comprensión clara y fundamentada del consumo mediante tarjetas de crédito, útil para diferentes actores interesados en el análisis de datos financieros.

---

## 📊 2. Dataset utilizado

- **Fuente:** Kaggle
- **Nombre:** Credit Card Transactions Dataset
- **Autor:** @priyamchoksi
- **Enlace:** [https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset](https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset)
- **Archivo principal:** CSV con transacciones
- **Licencia:** Según Kaggle (normalmente CC BY 4.0)
- **Fecha de descarga:** Noviembre de 2025

El dataset contiene información detallada sobre transacciones de tarjetas de crédito, incluyendo datos de ubicación, monto, tipo de comercio y más.

---

## 🧩 3. Variables relevantes

| Variable | Descripción | Utilidad |
|----------|-------------|----------|
| `trans_num` | Número único de transacción | Identificador único, evita duplicados |
| `trans_date_trans_time` | Fecha y hora de la transacción | Permite análisis temporal y patrones horarios |
| `cc_num` | Número de tarjeta de crédito | Permite agrupar por tarjeta/usuario |
| `merchant` | Nombre del comercio | Identifica establecimientos frecuentes |
| `category` | Categoría del comercio | Segmenta por tipo de gasto (alimentos, gasolina, etc.) |
| `amt` | Monto de la transacción | Variable objetivo para análisis de gastos |
| `gender` | Género del titular | Análisis de comportamiento por género |
| `city` / `state` | Ciudad y estado | Permite análisis geográfico |
| `lat` / `long` | Coordenadas geográficas | Facilita visualización en mapas |
| `city_pop` | Población de la ciudad | Contexto demográfico |
| `job` | Ocupación del titular | Segmentación por perfil laboral |
| `dob` | Fecha de nacimiento | Permite calcular edad y segmentar por generación |
| `merch_lat` / `merch_long` | Ubicación del comercio | Análisis de distancia y distribución geográfica |

---

## 🧠 4. Justificación del análisis

El mercado de transacciones financieras genera grandes volúmenes de datos que requieren análisis descriptivo para extraer información valiosa y fundamentar decisiones basadas en evidencia.

---

## 🧱 5. Flujo de datos implementado

El proyecto cumple con el flujo **Dataset → SQLite → CSV** exigido:

```
┌─────────────────┐
│  Kaggle Dataset │
│   (CSV files)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  1. INGESTIÓN       │
│  (Ingestar.py)      │
│  - Descarga         │
│  - Extracción       │
│  - Validación       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. CARGA A SQLite  │
│  (load_to_sqlite.py)│
│  - Crear DB         │
│  - Insertar datos   │
│  - Validar esquema  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. EXPORTACIÓN CSV │
│  (export_to_csv.py) │
│  - Consulta SQL     │
│  - Generación CSV   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. ANÁLISIS        │
│  (Jupyter Notebook) │
│  - Exploración      │
│  - Visualización    │
│  - Insights         │
└─────────────────────┘
```

---

## 📁 6. Estructura del proyecto

```
piv_2025_2_2/
│
├── README.md                    # Este archivo
├── setup.py                     # Configuración del paquete Python
│
├── src/
│   └── proyecto_integrador/
│       ├── ingestar.py         # Clase para descarga y procesamiento desde Kaggle
│       ├── load_to_sqlite.py   # Script de carga a base de datos SQLite
│       └── export_to_csv.py    # Script de exportación desde SQLite a CSV
│
├── notebooks/
│   └── proyecto_integrador.ipynb  # Notebook con análisis exploratorio
│
├── db/
│   └── proyecto.db             # Base de datos SQLite (generada)
│
├── csv/
│   └── export.csv              # Archivo CSV exportado (generado)
│
└── data/                        # Datos descargados de Kaggle (generado)
```

---

## 🚀 7. Instalación y configuración

### Requisitos previos

- Python 3.8 o superior
- Cuenta de Kaggle con API key configurada
- Pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/eulicerzapata/Proyecto_Integrador5.git
cd piv_2025_2_2
```

### Paso 2: Instalar dependencias

```bash
pip install -e .
```

Esto instalará las siguientes dependencias:
- `pandas` - Manipulación de datos
- `openpyxl` - Lectura de archivos Excel
- `kagglehub` - Descarga de datasets de Kaggle
- `matplotlib` / `seaborn` - Visualización
- `requests` / `beautifulsoup4` - Web scraping (opcional)
- `pyarrow` - Optimización de lectura de datos

### Paso 3: Configurar Kaggle API

1. Descarga tu archivo `kaggle.json` desde tu cuenta de Kaggle:
   - Ve a [https://www.kaggle.com/settings](https://www.kaggle.com/settings)
   - En la sección "API", haz clic en "Create New API Token"

2. Coloca el archivo en la ubicación correcta:
   - **Windows:** `C:\Users\<tu-usuario>\.kaggle\kaggle.json`
   - **Linux/Mac:** `~/.kaggle/kaggle.json`

3. Asegúrate de que el archivo tenga los permisos adecuados:
   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   ```

---

## ▶️ 8. Ejecución del proyecto

### Opción 1: GitHub Actions (Automático) ⭐ RECOMENDADO

El proyecto incluye un workflow de GitHub Actions que ejecuta todo el pipeline automáticamente.

**Configuración inicial** (solo una vez):

1. Obtén tus credenciales de Kaggle desde [https://www.kaggle.com/settings](https://www.kaggle.com/settings)
2. En tu repositorio de GitHub: **Settings** → **Secrets and variables** → **Actions**
3. Crea dos secrets:
   - `KAGGLE_USERNAME`: tu usuario de Kaggle
   - `KAGGLE_KEY`: tu API key de Kaggle

**El workflow se ejecuta automáticamente**:
- ✅ Cada vez que haces push a `main`
- ✅ Manualmente desde la pestaña "Actions" en GitHub

📖 **Guía completa**: Ver [.github/ACTIONS_SETUP.md](.github/ACTIONS_SETUP.md)

### Opción 2: Ejecución paso a paso (scripts individuales)

```powershell
# 1. Descargar y cargar datos a SQLite
python src/proyecto_integrador/load_to_sqlite.py

# 2. Exportar desde SQLite a CSV
python src/proyecto_integrador/export_to_csv.py
```

### Opción 3: Ejecución desde Jupyter Notebook

```powershell
# Iniciar Jupyter Notebook
jupyter notebook notebooks/proyecto_integrador.ipynb
```

Luego ejecuta las celdas secuencialmente para:
1. Descargar el dataset
2. Cargar a SQLite
3. Exportar a CSV
4. Realizar análisis exploratorio

---

## 📈 9. Resultados esperados

Al finalizar la ejecución, tendrás:

1. **Base de datos SQLite** (`db/proyecto.db`) con la tabla `transacciones`
2. **Archivo CSV** (`csv/export.csv`) con los datos exportados
3. **Notebook con análisis exploratorio** que incluye:
   - Estadísticas descriptivas generales
   - Análisis de transacciones por género
   - Análisis geográfico (ciudad, estado, coordenadas)
   - Distribución de transacciones por categoría de comercio
   - Identificación de establecimientos más frecuentados
   - Análisis de montos de gasto por perfil demográfico
   - Patrones temporales de transacciones
   - Detección de valores nulos y datos inconsistentes
   - Identificación de posibles anomalías en el conjunto de datos

---

## 🔍 10. Validaciones y comprobaciones

El proyecto incluye validaciones automáticas en el notebook:

✅ **Listar tablas disponibles** en SQLite  
✅ **Conteo de filas** por tabla  
✅ **Inspección de primeras filas** de cada tabla  
✅ **Análisis de valores nulos** por columna  
✅ **Detección de duplicados** basado en `trans_num`

---

## 👥 11. Autores

- **Eulicer Zapata Orrego** - [eulicer.zapata@iudigital.edu.co](mailto:eulicer.zapata@iudigital.edu.co)
- **Dawin Salazar**- [dawin.salazar@iudigital.edu.co](mailto:dawin.salazar@iudigital.edu.co)

---

## 📄 12. Licencia

Este proyecto es de uso académico para el **Proyecto Integrado 5** de la Institución Universitaria Digital.

---

