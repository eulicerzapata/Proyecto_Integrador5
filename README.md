# Proyecto Integrado 5 – Análisis de Transacciones con Tarjetas de Crédito 💳

---
## 🔗 Links

Diagrama de Gantt: https://docs.google.com/spreadsheets/d/1I1Phu9ODemJZHmGOwFeAwHl1w4TL-Qs5J2ONIuQouhg/edit?usp=sharing

Documentación: https://docs.google.com/document/d/1dQ46rt1UL1tuB6v6KXs-eRTLkAm-UciMZAHUypAvRkg/edit?usp=sharing

---


## 🎯 Objetivos

### Objetivo General
Analizar las transacciones bancarias en función del género y la ubicación geográfica de los titulares.
---

## 📘 1. Definición del problema / Caso de uso

El caso de uso se centra en examinar:
-  Cómo se distribuyen las transacciones según ubicación y tipo de comercio
-  Diferencias de comportamiento por género
-  Zonas geográficas de mayor actividad comercial

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

El proyecto cumple con el flujo **Dataset → Limpieza → SQLite → CSV** exigido:

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
┌─────────────────────────────┐
│  2. LIMPIEZA Y ENRIQUECIMIENTO   
│  (limpiar_enriquecer.py)    │
│  - Eliminar duplicados      │
│  - Manejar nulos            │
│  - Normalizar columnas      │
│  - Enriquecer con fechas    │
│  - Guardar CSV enriquecido  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────┐
│  3. CARGA A SQLite  │
│  (load_to_sqlite.py)│
│  - Crear DB         │
│  - Insertar datos   │
│  - Validar esquema  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. EXPORTACIÓN CSV │
│  (export_to_csv.py) │
│  - Consulta SQL     │
│  - Generación CSV   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  5. ANÁLISIS        │
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
├── README.md                    # Documentación del proyecto
├── setup.py                     # Configuración del paquete
├── requirements.txt             # Dependencias del proyecto
│
├── dashboard/
│   └── app.py                   # Código fuente del dashboard (Streamlit)
│
├── src/
│   └── proyecto_integrador/
│       ├── limpiar_datos.py      # Limpieza y generación de Parquet
│       ├── ingestar.py           # Descarga de datos
│       ├── load_to_sqlite.py     # Carga a base de datos
│       └── export_to_csv.py      # Exportación
│
├── data/
│   └── dataset_enriquecido.parquet  # Dataset optimizado para el dashboard
│
├── db/
│   └── proyecto.db              # Base de datos SQLite
│
├── notebooks/                   # Notebooks de análisis y pruebas
└── docs/                        # Documentación y gráficos generados
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
# 1. Descargar, limpiar datos 
python src/proyecto_integrador/limpiar_datos.py

# O ejecutar paso a paso:

# 1a.  descargar y cargar datos a SQLite 
python src/proyecto_integrador/load_to_sqlite.py

# 2. Exportar desde SQLite a CSV
python src/proyecto_integrador/export_to_csv.py
```

### Opción 3: Ejecución desde Jupyter Notebook

#### Notebook de Limpieza y Enriquecimiento

```powershell
# Abrir notebook de limpieza
jupyter notebook notebooks/limpieza_enriquecimiento.ipynb
```

Este notebook incluye:
- ✅ Descarga automática del dataset
- ✅ Análisis antes y después de la limpieza
- ✅ Eliminación de duplicados
- ✅ Manejo de valores nulos
- ✅ Normalización de columnas
- ✅ Enriquecimiento con columnas temporales (año, mes, día, etc.)
- ✅ Carga a SQLite
- ✅ Estadísticas descriptivas

#### Notebook de Análisis Exploratorio

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
4. **Carpeta de Gráficos** (`docs/graficos/`) con visualizaciones clave
 
---

## 🔍 10. Validaciones y comprobaciones

El proyecto incluye validaciones automáticas en el notebook:

✅ **Listar tablas disponibles** en SQLite  
✅ **Conteo de filas** por tabla  
✅ **Inspección de primeras filas** de cada tabla  
✅ **Análisis de valores nulos** por columna  
✅ **Detección de duplicados** basado en `trans_num`

---

## 📊 11. Dashboard Interactivo

El proyecto cuenta con un dashboard interactivo desplegado en Streamlit Cloud que permite explorar los datos de manera visual.

**🔗 Link del Dashboard:** [https://proyectointegrador5git-p93mwqqeqjdqwvujfgevf3.streamlit.app/](https://proyectointegrador5git-p93mwqqeqjdqwvujfgevf3.streamlit.app/)

### Instrucciones para usar el dashboard:
1.  **Ingresa al link** proporcionado arriba.
2.  **Navega por las pestañas** para ver diferentes análisis (Temporal, Género, Ubicación).
3.  **Usa los filtros** en la barra lateral para segmentar por año, estado o género.
4.  **Interactúa con los gráficos**: puedes hacer zoom, descargar imágenes y ver detalles al pasar el mouse.

---

## 👥 12. Autores

- **Eulicer Zapata Orrego** - [eulicer.zapata@iudigital.edu.co](mailto:eulicer.zapata@iudigital.edu.co)
- **Dawin Salazar**- [dawin.salazar@iudigital.edu.co](mailto:dawin.salazar@iudigital.edu.co)

---

## 📄 13. Licencia

Este proyecto es de uso académico para el **Proyecto Integrado 5** de la Institución Universitaria Digital.

---
