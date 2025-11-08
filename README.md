# 💳 Proyecto Integrado 5 – Análisis de Transacciones de Tarjetas de Crédito# 💳 Proyecto Integrado 5 – Análisis de Transacciones de Tarjetas de Crédito



## 📘 1. Descripción del proyecto## 📘 1. Descripción del proyecto



El objetivo de este proyecto es **analizar transacciones de tarjetas de crédito** para identificar **patrones de gasto, tendencias de consumo y comportamientos financieros**.El objetivo de este proyecto es **analizar transacciones de tarjetas de crédito** para identificar **patrones de gasto, tendencias de consumo y comportamientos financieros**.



El estudio busca responder preguntas como:El estudio busca responder preguntas como:



> 💰 ¿Cuáles son los patrones de gasto más comunes en las transacciones con tarjeta de crédito?> 💰 ¿Cuáles son los patrones de gasto más comunes en las transacciones con tarjeta de crédito?

> 🛍️ ¿Qué categorías de productos generan más transacciones?> 🛍️ ¿Qué categorías de productos generan más transacciones?

> 📊 ¿Cómo varían los montos de transacción según diferentes variables?> 📊 ¿Cómo varían los montos de transacción según diferentes variables?



Este análisis permite ofrecer información útil para:Este análisis permite ofrecer información útil para:

- Instituciones financieras que buscan entender el comportamiento de sus clientes.- Instituciones financieras que buscan entender el comportamiento de sus clientes.

- Comercios que desean optimizar sus estrategias de venta.- Comercios que desean optimizar sus estrategias de venta.

- Analistas de datos que estudian patrones de consumo.- Analistas de datos que estudian patrones de consumo.



------



## 📊 2. Dataset utilizado## 📊 2. Dataset utilizado



**Fuente:** Kaggle  **Fuente:** Kaggle  

**Nombre:** *Credit Card Transactions Dataset*  **Nombre:** *Credit Card Transactions Dataset*  

**Autor:** [@priyamchoksi](https://www.kaggle.com/priyamchoksi)  **Autor:** [@priyamchoksi](https://www.kaggle.com/priyamchoksi)  

**Enlace:** [https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset](https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset)  **Enlace:** [https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset](https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset)  

**Licencia:** Licencia abierta (verificar en Kaggle - normalmente *CC0: Public Domain* o *CC BY 4.0*)  **Licencia:** Licencia abierta (verificar en Kaggle - normalmente *CC0: Public Domain* o *CC BY 4.0*)  

**Fecha de descarga:** Noviembre de 2025**Fecha de descarga:** Noviembre de 2025



El dataset contiene información sobre transacciones realizadas con tarjetas de crédito, incluyendo montos, categorías, fechas y otros atributos relevantes.El dataset contiene información sobre transacciones realizadas con tarjetas de crédito, incluyendo montos, categorías, fechas y otros atributos relevantes.



------



## 🧩 3. Variables relevantes## 🧩 3. Variables relevantes



Las variables principales del dataset incluyen (sujeto a confirmación al descargar):Las variables principales del dataset incluyen (sujeto a confirmación al descargar):



| Variable | Descripción | Utilidad || Variable | Descripción | Utilidad |

|-----------|--------------|----------||-----------|--------------|----------|

| `transaction_id` | Identificador único de la transacción | Clave primaria || `transaction_id` | Identificador único de la transacción | Clave primaria |

| `date` | Fecha de la transacción | Análisis temporal || `date` | Fecha de la transacción | Análisis temporal |

| `amount` | Monto de la transacción | Variable objetivo principal || `amount` | Monto de la transacción | Variable objetivo principal |

| `category` | Categoría del producto/servicio | Segmentación de gastos || `category` | Categoría del producto/servicio | Segmentación de gastos |

| `merchant` | Nombre del comercio | Análisis por establecimiento || `merchant` | Nombre del comercio | Análisis por establecimiento |

| `card_type` | Tipo de tarjeta utilizada | Segmentación de clientes || `card_type` | Tipo de tarjeta utilizada | Segmentación de clientes |



**Nota:** La estructura exacta se confirmará al descargar y explorar el dataset.**Nota:** La estructura exacta se confirmará al descargar y explorar el dataset.



------



## 🧠 4. Caso de uso y justificación## 🧠 4. Caso de uso y justificación



El análisis de transacciones con tarjetas de crédito es fundamental para:El análisis de transacciones con tarjetas de crédito es fundamental para:



- Detectar patrones de consumo y tendencias del mercado.- Detectar patrones de consumo y tendencias del mercado.

- Identificar segmentos de clientes por comportamiento de compra.- Identificar segmentos de clientes por comportamiento de compra.

- Optimizar estrategias de marketing y ventas.- Optimizar estrategias de marketing y ventas.

- Apoyar decisiones financieras basadas en datos.- Apoyar decisiones financieras basadas en datos.



------



## 🧱 5. Flujo de datos implementado## 🧱 5. Flujo de datos implementado



El proyecto cumple con el flujo **dataset → SQLite → CSV** exigido:El proyecto cumple con el flujo **dataset → SQLite → CSV** exigido:



```
📥 Kaggle Dataset → 📂 data/ → 🗄️ SQLite (db/proyecto.db) → 📤 CSV (db/export.csv)
```

### Pasos del pipeline:

1. **Descarga del dataset** desde Kaggle usando `kagglehub`.
2. **Carga a SQLite**: Los datos se insertan en la base de datos `db/proyecto.db`.
3. **Exportación a CSV**: Se exportan los datos desde SQLite a `db/export.csv`.

---

## 📁 6. Estructura del repositorio

```
piv_2025_2_2/
│
├── data/                     # Dataset original (o enlace en README si pesa mucho)
│   └── README.md             # Instrucciones para descargar el dataset
│
├── db/                       # Base de datos y exportaciones
│   ├── proyecto.db           # Base de datos SQLite con las transacciones
│   └── export.csv            # Exportación desde la base de datos
│
├── docs/                     # Imágenes y documentación de soporte (opcional)
│
├── src/                      # Código fuente
│   └── proyecto_integrador/
│       ├── ingestar.py       # Clase para descarga y carga de datos
│       ├── load_to_sqlite.py # Script de carga a SQLite
│       └── export_to_csv.py  # Script de exportación a CSV
│
├── notebooks/                # Jupyter notebooks con análisis
│   └── analisis_sql.ipynb    # Notebook con CREATE TABLE, INSERT y consultas
│
├── README.md                 # Este archivo
├── setup.py                  # Configuración del paquete
└── .gitignore                # Archivos a ignorar en git
```

---

## 🚀 7. Instrucciones de uso

### 7.1 Requisitos previos

```bash
pip install pandas numpy kagglehub openpyxl
```

### 7.2 Configurar credenciales de Kaggle

1. Crea una cuenta en [Kaggle](https://www.kaggle.com/)
2. Ve a `Account` → `Create New API Token`
3. Descarga el archivo `kaggle.json`
4. Colócalo en `~/.kaggle/` (Linux/Mac) o `C:\Users\<usuario>\.kaggle\` (Windows)

### 7.3 Ejecutar el pipeline completo

```python
# 1. Cargar datos a SQLite
python src/proyecto_integrador/load_to_sqlite.py

# 2. Exportar desde SQLite a CSV
python src/proyecto_integrador/export_to_csv.py
```

### 7.4 Explorar con el notebook

Abre `notebooks/analisis_sql.ipynb` para ver las sentencias SQL y análisis exploratorio.

---

## 📜 8. Licencia y créditos

- **Dataset:** Credit Card Transactions Dataset por Priyam Choksi (Kaggle)
- **Licencia del dataset:** Verificar en la página de Kaggle
- **Proyecto desarrollado por:** [Tu nombre/equipo]
- **Fecha:** Noviembre 2025

---

## 📧 9. Contacto

Para preguntas o sugerencias sobre este proyecto, contacta a [tu email/contacto].
