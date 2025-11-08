# Proyecto Integrado 5 – Análisis de Transacciones con Tarjetas de Crédito 💳

## 📘 1. Descripción del proyecto

El objetivo de este proyecto es analizar un conjunto de datos de transacciones realizadas con tarjetas de crédito para identificar patrones de comportamiento, detección de anomalías y tendencias en el uso de tarjetas de crédito.

El estudio busca responder preguntas como:

💳 **¿Cuáles son los patrones de uso más comunes en las transacciones con tarjetas de crédito?**

Este análisis permite ofrecer información útil para:

- **Instituciones financieras** que buscan mejorar la seguridad y detección de fraude.
- **Comercios** que desean entender mejor el comportamiento de sus clientes.
- **Analistas de datos** que buscan identificar tendencias y patrones en transacciones financieras.

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
| `city` / `state` | Ciudad y estado | Permite análisis geográfico |
| `lat` / `long` | Coordenadas geográficas | Facilita visualización en mapas |
| `city_pop` | Población de la ciudad | Contexto demográfico |
| `job` | Ocupación del titular | Segmentación por perfil laboral |
| `dob` | Fecha de nacimiento | Permite calcular edad y segmentar por generación |
| `merch_lat` / `merch_long` | Ubicación del comercio | Análisis de distancia y distribución geográfica |

---

## 🧠 4. Caso de uso y justificación

El análisis de transacciones con tarjetas de crédito es fundamental para:

- **Detección de fraude:** Identificar patrones anómalos en transacciones.
- **Análisis de comportamiento del consumidor:** Entender hábitos de gasto por categoría, ubicación y horario.
- **Optimización de servicios financieros:** Diseñar productos y servicios adaptados a las necesidades de los clientes.
- **Seguridad bancaria:** Mejorar sistemas de alerta temprana ante actividades sospechosas.

El mercado de transacciones financieras genera grandes volúmenes de datos que requieren análisis avanzado para extraer valor.

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

### Opción 1: Ejecución paso a paso (scripts individuales)

```powershell
# 1. Descargar y cargar datos a SQLite
python src/proyecto_integrador/load_to_sqlite.py

# 2. Exportar desde SQLite a CSV
python src/proyecto_integrador/export_to_csv.py
```

### Opción 2: Ejecución desde Jupyter Notebook

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
3. **Notebook con análisis** que incluye:
   - Estadísticas descriptivas
   - Detección de valores nulos
   - Distribución de transacciones por categoría
   - Patrones temporales
   - Análisis geográfico
   - Detección de anomalías

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
- **Dawin Salazar**

---

## 📄 12. Licencia

Este proyecto es de uso académico para el **Proyecto Integrado 5** de la Institución Universitaria Digital.

---

## 🤝 13. Contribuciones

Si deseas contribuir a este proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 14. Contacto y soporte

Para preguntas o soporte:
- **Repositorio:** [https://github.com/eulicerzapata/Proyecto_Integrador5](https://github.com/eulicerzapata/Proyecto_Integrador5)

