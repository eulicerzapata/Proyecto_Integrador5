"""
Dashboard de Análisis de Transacciones por Género y Lugar
==========================================================

Dashboard interactivo con Streamlit para analizar el comportamiento
de transacciones de tarjetas de crédito con respecto al género y lugar,
con énfasis en el análisis temporal.

Historia que cuenta el tablero:
1. ¿Quién gasta más? Distribución general por género
2. ¿Cuánto gastan? Montos comparativos por género
3. ¿Cuándo gastan? Evolución temporal (PRIORIDAD)
4. ¿En qué gastan? Categorías de comercio
5. ¿Dónde gastan? Análisis por ubicación

Autor: Proyecto Integrador 5
Fecha: 2025-12-06
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN DE PÁGINA (MODO CLARO)
# =============================================================================
st.set_page_config(
    page_title="Análisis de Transacciones por Género",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores por género (consistentes para toda la aplicación)
COLORS = {
    'M': '#3498db',  # Azul
    'F': '#e74c3c',  # Rojo/Rosa
    'total': '#2ecc71'  # Verde
}

GENDER_LABELS = {
    'M': 'Masculino',
    'F': 'Femenino'
}

# Nombres de meses en español
MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Traducciones de categorías al español
CATEGORIAS = {
    'misc_net': 'Compras Online Varias',
    'grocery_pos': 'Supermercado',
    'entertainment': 'Entretenimiento',
    'gas_transport': 'Gasolina y Transporte',
    'misc_pos': 'Compras Varias',
    'grocery_net': 'Supermercado Online',
    'shopping_net': 'Compras Online',
    'shopping_pos': 'Compras en Tienda',
    'food_dining': 'Restaurantes',
    'personal_care': 'Cuidado Personal',
    'health_fitness': 'Salud y Fitness',
    'travel': 'Viajes',
    'kids_pets': 'Niños y Mascotas',
    'home': 'Hogar'
}

# =============================================================================
# ESTILOS CSS PERSONALIZADOS (MODO CLARO)
# =============================================================================
st.markdown("""
<style>
    /* Estilo general - Modo Claro */
    .main {
        padding: 1rem;
        background-color: #ffffff;
    }
    
    /* Cards de métricas */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Títulos */
    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    h2, h3 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #2c3e50;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
    }
    
    /* Secciones de historia */
    .story-section {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 10px 15px;
        margin-bottom: 20px;
        border-radius: 0 5px 5px 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CARGA DE DATOS
# =============================================================================
@st.cache_data
def cargar_datos():
    """Carga el dataset enriquecido con caché para mejor rendimiento."""
    rutas_posibles = [
        Path(__file__).parent.parent / 'data' / 'dataset_enriquecido.csv',
        Path('data/dataset_enriquecido.csv'),
        Path('../data/dataset_enriquecido.csv'),
    ]
    
    for ruta in rutas_posibles:
        if ruta.exists():
            df = pd.read_csv(ruta, low_memory=False)
            # Convertir fecha a datetime
            df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
            # Crear columnas adicionales para análisis temporal
            df['dia_semana'] = df['trans_date_trans_time'].dt.day_name()
            df['dia_semana_num'] = df['trans_date_trans_time'].dt.dayofweek
            df['hora_num'] = df['trans_date_trans_time'].dt.hour
            df['mes_nombre'] = df['mes'].map(MESES)
            df['periodo'] = df['trans_date_trans_time'].dt.to_period('M').astype(str)
            return df
    
    st.error("No se encontró el archivo dataset_enriquecido.csv")
    return None


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN - ANÁLISIS TEMPORAL (PRIORIDAD)
# =============================================================================

def grafico_evolucion_gasto_genero_anio(df_filtrado):
    """Gráfico de Barras: Evolución del Gasto Total por Género y Año."""
    df_anual = df_filtrado.groupby(['anio', 'gender']).agg(
        gasto_total=('amt', 'sum')
    ).reset_index()
    
    fig = px.bar(
        df_anual,
        x='anio',
        y='gasto_total',
        color='gender',
        color_discrete_map=COLORS,
        barmode='group',
        labels={
            'anio': 'Año',
            'gasto_total': 'Gasto Total ($)',
            'gender': 'Género'
        },
        title='📊 Comparativa de Gasto Total: Por Género y Año'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickformat='$,.0f'
    )
    
    # Añadir etiquetas en las barras
    fig.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
    fig.for_each_trace(lambda t: t.update(name=GENDER_LABELS.get(t.name, t.name)))
    
    return fig


def grafico_tendencia_mensual(df_filtrado):
    """Gráfico de Líneas: Tendencia mensual de transacciones por género."""
    df_mensual = df_filtrado.groupby(['anio', 'mes', 'gender']).agg(
        cantidad=('trans_num', 'count'),
        monto_total=('amt', 'sum'),
        monto_promedio=('amt', 'mean')
    ).reset_index()
    
    df_mensual['fecha'] = pd.to_datetime(
        df_mensual['anio'].astype(str) + '-' + df_mensual['mes'].astype(str) + '-01'
    )
    
    fig = px.line(
        df_mensual,
        x='fecha',
        y='cantidad',
        color='gender',
        color_discrete_map=COLORS,
        markers=True,
        labels={
            'fecha': 'Fecha',
            'cantidad': 'Cantidad de Transacciones',
            'gender': 'Género'
        },
        title='📈 Evolución Mensual: Cantidad de Transacciones por Género'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.for_each_trace(lambda t: t.update(name=GENDER_LABELS.get(t.name, t.name)))
    
    return fig


def grafico_monto_mensual(df_filtrado):
    """Gráfico de Líneas: Monto promedio mensual por género."""
    df_mensual = df_filtrado.groupby(['anio', 'mes', 'gender']).agg(
        monto_promedio=('amt', 'mean')
    ).reset_index()
    
    df_mensual['fecha'] = pd.to_datetime(
        df_mensual['anio'].astype(str) + '-' + df_mensual['mes'].astype(str) + '-01'
    )
    
    fig = px.line(
        df_mensual,
        x='fecha',
        y='monto_promedio',
        color='gender',
        color_discrete_map=COLORS,
        markers=True,
        labels={
            'fecha': 'Fecha',
            'monto_promedio': 'Monto Promedio ($)',
            'gender': 'Género'
        },
        title='💵 Evolución Mensual: Monto Promedio por Género'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickformat='$,.2f'
    )
    
    fig.for_each_trace(lambda t: t.update(name=GENDER_LABELS.get(t.name, t.name)))
    
    return fig


def grafico_gasto_mensual_genero(df_filtrado):
    """Gráfico de líneas: Gasto total mensual por género."""
    df_mensual = df_filtrado.groupby(['anio', 'mes', 'gender']).agg(
        gasto_total=('amt', 'sum')
    ).reset_index()
    
    df_mensual['fecha'] = pd.to_datetime(
        df_mensual['anio'].astype(str) + '-' + df_mensual['mes'].astype(str) + '-01'
    )
    
    fig = px.line(
        df_mensual,
        x='fecha',
        y='gasto_total',
        color='gender',
        color_discrete_map=COLORS,
        markers=True,
        labels={
            'fecha': 'Fecha',
            'gasto_total': 'Gasto Total ($)',
            'gender': 'Género'
        },
        title='💰 Evolución Mensual: Gasto Total por Género'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickformat='$,.0f'
    )
    
    fig.for_each_trace(lambda t: t.update(name=GENDER_LABELS.get(t.name, t.name)))
    
    return fig


def grafico_distribucion_hora(df_filtrado):
    """Gráfico de barras: Distribución de transacciones por hora del día."""
    df_hora = df_filtrado.groupby(['hora_num', 'gender']).size().reset_index(name='cantidad')
    
    # Crear etiquetas más claras para las horas
    horas_labels = {
        0: '12 AM', 1: '1 AM', 2: '2 AM', 3: '3 AM', 4: '4 AM', 5: '5 AM',
        6: '6 AM', 7: '7 AM', 8: '8 AM', 9: '9 AM', 10: '10 AM', 11: '11 AM',
        12: '12 PM', 13: '1 PM', 14: '2 PM', 15: '3 PM', 16: '4 PM', 17: '5 PM',
        18: '6 PM', 19: '7 PM', 20: '8 PM', 21: '9 PM', 22: '10 PM', 23: '11 PM'
    }
    
    # Colores con transparencia en formato rgba
    colors_fill = {
        'M': 'rgba(52, 152, 219, 0.3)',  # Azul con transparencia
        'F': 'rgba(231, 76, 60, 0.3)'     # Rojo con transparencia
    }
    
    df_hora['hora_label'] = df_hora['hora_num'].map(horas_labels)
    
    # Usar gráfico de área para mejor visualización
    fig = go.Figure()
    
    for gender in df_hora['gender'].unique():
        df_g = df_hora[df_hora['gender'] == gender].sort_values('hora_num')
        fig.add_trace(go.Scatter(
            x=df_g['hora_label'],
            y=df_g['cantidad'],
            name=GENDER_LABELS.get(gender, gender),
            mode='lines+markers',
            line=dict(color=COLORS.get(gender), width=2),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor=colors_fill.get(gender, 'rgba(128,128,128,0.3)'),
        ))
    
    fig.update_layout(
        template='plotly_white',
        title='🕐 Patrón Horario: ¿A qué hora realizan transacciones?',
        xaxis_title='Hora del Día',
        yaxis_title='Cantidad de Transacciones',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            tickangle=45,
            categoryorder='array',
            categoryarray=[horas_labels[i] for i in range(24)]
        ),
        hovermode='x unified'
    )
    
    return fig


def grafico_heatmap_temporal(df_filtrado):
    """Heatmap: Transacciones por día de la semana y hora."""
    df_heat = df_filtrado.groupby(['dia_semana_num', 'hora_num']).size().reset_index(name='cantidad')
    
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    # Crear un DataFrame completo con todos los días y horas
    from itertools import product
    all_combinations = pd.DataFrame(
        list(product(range(7), range(24))),
        columns=['dia_semana_num', 'hora_num']
    )
    
    # Merge para asegurar que tenemos todas las combinaciones
    df_heat = all_combinations.merge(df_heat, on=['dia_semana_num', 'hora_num'], how='left').fillna(0)
    
    df_pivot = df_heat.pivot(index='dia_semana_num', columns='hora_num', values='cantidad').fillna(0)
    
    # Asegurar que el índice tenga los 7 días ordenados
    df_pivot = df_pivot.reindex(range(7)).fillna(0)
    
    fig = px.imshow(
        df_pivot.values,
        labels=dict(x="Hora del Día", y="Día de la Semana", color="Transacciones"),
        x=[f"{h}:00" for h in range(24)],
        y=dias,
        color_continuous_scale='Blues',
        title='🗓️ Mapa de Calor: Intensidad de Transacciones por Día y Hora'
    )
    
    fig.update_layout(
        template='plotly_white',
        xaxis=dict(tickangle=45)
    )
    
    return fig


def grafico_evolucion_categoria_temporal(df_filtrado):
    """Gráfico de líneas: Evolución temporal por categoría con traducciones."""
    
    # Crear copia y traducir categorías
    df_temp = df_filtrado.copy()
    df_temp['categoria_es'] = df_temp['category'].map(CATEGORIAS).fillna(df_temp['category'])
    
    # Top 5 categorías
    top_cats = df_temp.groupby('categoria_es').size().nlargest(5).index.tolist()
    df_cat = df_temp[df_temp['categoria_es'].isin(top_cats)]
    
    df_temporal = df_cat.groupby(['anio', 'mes', 'categoria_es']).agg(
        cantidad=('trans_num', 'count')
    ).reset_index()
    
    df_temporal['fecha'] = pd.to_datetime(
        df_temporal['anio'].astype(str) + '-' + df_temporal['mes'].astype(str) + '-01'
    )
    
    fig = px.line(
        df_temporal,
        x='fecha',
        y='cantidad',
        color='categoria_es',
        markers=True,
        labels={
            'fecha': 'Fecha',
            'cantidad': 'Cantidad de Transacciones',
            'categoria_es': 'Categoría'
        },
        title='📦 Evolución Temporal: Top 5 Categorías'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    return fig


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN - ANÁLISIS POR GÉNERO
# =============================================================================

def grafico_distribucion_genero(df_filtrado):
    """Gráfico Donut: Distribución de transacciones por género."""
    df_genero = df_filtrado.groupby('gender').agg(
        cantidad=('trans_num', 'count'),
        monto_total=('amt', 'sum')
    ).reset_index()
    
    df_genero['genero_label'] = df_genero['gender'].map(GENDER_LABELS)
    
    fig = px.pie(
        df_genero,
        values='cantidad',
        names='genero_label',
        color='gender',
        color_discrete_map=COLORS,
        title='👥 ¿Quién realiza más transacciones?',
        hole=0.4
    )
    
    fig.update_layout(template='plotly_white')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def grafico_monto_genero(df_filtrado):
    """Gráfico de barras: Monto promedio por género."""
    df_genero = df_filtrado.groupby('gender').agg(
        monto_promedio=('amt', 'mean'),
        monto_total=('amt', 'sum')
    ).reset_index()
    
    df_genero['genero_label'] = df_genero['gender'].map(GENDER_LABELS)
    
    fig = px.bar(
        df_genero,
        x='genero_label',
        y='monto_promedio',
        color='gender',
        color_discrete_map=COLORS,
        text='monto_promedio',
        labels={
            'genero_label': 'Género',
            'monto_promedio': 'Monto Promedio ($)'
        },
        title='� ¿Cuánto gastan en promedio?'
    )
    
    fig.update_layout(template='plotly_white', showlegend=False)
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    
    return fig


def grafico_categorias_genero(df_filtrado, top_n=10):
    """Gráfico de barras horizontales: Top categorías por género con cantidad y monto."""
    
    # Crear copia y traducir categorías
    df_temp = df_filtrado.copy()
    df_temp['categoria_es'] = df_temp['category'].map(CATEGORIAS).fillna(df_temp['category'])
    
    # Agrupar por categoría traducida y género
    df_cat = df_temp.groupby(['categoria_es', 'gender']).agg(
        cantidad=('trans_num', 'count'),
        monto_total=('amt', 'sum'),
        monto_promedio=('amt', 'mean')
    ).reset_index()
    
    # Obtener top categorías por cantidad total
    top_cats = df_temp.groupby('categoria_es').size().nlargest(top_n).index.tolist()
    df_cat = df_cat[df_cat['categoria_es'].isin(top_cats)]
    
    # Ordenar por cantidad total
    orden_cats = df_cat.groupby('categoria_es')['cantidad'].sum().sort_values(ascending=True).index.tolist()
    
    # Crear gráfico
    fig = go.Figure()
    
    for gender in ['F', 'M']:
        df_g = df_cat[df_cat['gender'] == gender]
        # Ordenar según el orden general
        df_g = df_g.set_index('categoria_es').reindex(orden_cats).reset_index()
        
        # Crear etiquetas con cantidad y monto promedio
        text_labels = []
        for _, row in df_g.iterrows():
            cant = row['cantidad']
            monto = row['monto_promedio']
            if cant > 0:
                text_labels.append(f"{cant:,.0f} (${monto:.0f})")
            else:
                text_labels.append("")
        
        fig.add_trace(go.Bar(
            y=df_g['categoria_es'],
            x=df_g['cantidad'],
            name=GENDER_LABELS.get(gender, gender),
            orientation='h',
            marker_color=COLORS.get(gender, '#666666'),
            text=text_labels,
            textposition='inside',
            textfont=dict(color='white', size=16, family='Arial Black'),
            hovertemplate=(
                f"<b>%{{y}}</b><br>"
                f"Género: {GENDER_LABELS.get(gender, gender)}<br>"
                f"Transacciones: %{{x:,}}<br>"
                f"Monto Promedio: $%{{customdata:.2f}}<br>"
                f"<extra></extra>"
            ),
            customdata=df_g['monto_promedio']
        ))
    
    # Calcular altura dinámica - más grande
    altura = max(600, top_n * 65)
    
    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f'🏪 Top {top_n} Categorías: Transacciones (Monto Promedio)',
            font=dict(size=22)
        ),
        barmode='group',
        xaxis=dict(
            title=dict(text='Cantidad de Transacciones', font=dict(size=16)),
            tickfont=dict(size=14)
        ),
        yaxis=dict(title='', tickfont=dict(size=16)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=16)
        ),
        height=altura,
        margin=dict(l=220),
        bargap=0.15,
        bargroupgap=0.1
    )
    
    return fig


# =============================================================================
# FUNCIONES DE VISUALIZACIÓN - ANÁLISIS POR LUGAR
# =============================================================================

def grafico_proporcion_gasto_estados(df_filtrado, ordenar_por='F', top_n=10):
    """Gráfico de barras apiladas 100%: Proporción de gasto por género ordenado por monto."""
    
    # Calcular gasto total por estado y género (TODOS los estados primero)
    pivot_sum = df_filtrado.pivot_table(
        index='state_name', 
        columns='gender', 
        values='amt', 
        aggfunc='sum'
    ).fillna(0)
    
    # Calcular porcentaje (proporción)
    pivot_pct = pivot_sum.div(pivot_sum.sum(axis=1), axis=0)
    
    # Ordenar por el MONTO en dólares del género seleccionado (no porcentaje)
    if ordenar_por in pivot_sum.columns:
        # Ordenar de mayor a menor MONTO del género seleccionado
        pivot_sum_sorted = pivot_sum.sort_values(ordenar_por, ascending=False).head(top_n)
        # Invertir para que el mayor quede arriba en el gráfico horizontal
        pivot_sum_sorted = pivot_sum_sorted.iloc[::-1]
        # Alinear la tabla de porcentajes
        pivot_pct = pivot_pct.reindex(pivot_sum_sorted.index)
        pivot_sum = pivot_sum_sorted
    else:
        pivot_sum = pivot_sum.head(top_n).iloc[::-1]
        pivot_pct = pivot_pct.reindex(pivot_sum.index)
    
    # Crear figura con Plotly
    fig = go.Figure()
    
    # Orden de géneros para que F aparezca primero (izquierda) y M después
    generos_orden = ['F', 'M'] if 'F' in pivot_pct.columns else list(pivot_pct.columns)
    
    for gender in generos_orden:
        if gender not in pivot_pct.columns:
            continue
            
        pct_values = pivot_pct[gender].values
        sum_values = pivot_sum[gender].values
        
        # Crear etiquetas con porcentaje y monto
        text_labels = []
        for pct, amt in zip(pct_values, sum_values):
            if pct > 0.08:  # Solo mostrar si es mayor a 8%
                if amt >= 1_000_000:
                    amt_str = f"${amt/1_000_000:.1f}M"
                else:
                    amt_str = f"${amt/1_000:.0f}K"
                text_labels.append(f"{pct:.0%}<br>({amt_str})")
            else:
                text_labels.append("")
        
        fig.add_trace(go.Bar(
            y=pivot_pct.index,
            x=pct_values,
            name=GENDER_LABELS.get(gender, gender),
            orientation='h',
            marker_color=COLORS.get(gender, '#666666'),
            text=text_labels,
            textposition='inside',
            textfont=dict(color='white', size=14, family='Arial Black'),
            hovertemplate=(
                f"<b>%{{y}}</b><br>"
                f"Género: {GENDER_LABELS.get(gender, gender)}<br>"
                f"Proporción: %{{x:.1%}}<br>"
                f"Monto: $%{{customdata:,.2f}}<extra></extra>"
            ),
            customdata=sum_values
        ))
    
    # Calcular altura dinámica basada en cantidad de estados - más grande
    altura = max(550, top_n * 55)
    
    fig.update_layout(
        template='plotly_white',
        title=dict(
            text=f'📊 Top {top_n} Estados con Mayor Gasto {GENDER_LABELS.get(ordenar_por, ordenar_por)}',
            font=dict(size=20)
        ),
        barmode='stack',
        xaxis=dict(
            title=dict(text='Proporción del Gasto Total', font=dict(size=14)),
            tickformat='.0%',
            tickfont=dict(size=12),
            range=[0, 1]
        ),
        yaxis=dict(title='', tickfont=dict(size=14)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        height=altura,
        margin=dict(l=180)
    )
    
    return fig


def mapa_concentracion_transacciones(df_filtrado, max_cities=300):
    """Mapa de densidad: Concentración geográfica de transacciones por género."""
    
    # Agrupar por ciudad y género para calcular métricas
    df_cities = df_filtrado.groupby(['city', 'state_name', 'lat', 'long', 'gender']).agg(
        cantidad=('trans_num', 'count'),
        monto_total=('amt', 'sum'),
        monto_promedio=('amt', 'mean'),
        poblacion=('city_pop', 'first')
    ).reset_index()
    
    # Calcular totales por ciudad para el hover
    df_totals = df_filtrado.groupby(['city', 'state_name']).agg(
        cantidad_total=('trans_num', 'count'),
        monto_ciudad=('amt', 'sum')
    ).reset_index()
    
    # Calcular métricas por género para el hover
    df_gender = df_filtrado.groupby(['city', 'state_name', 'gender']).agg(
        cant_g=('trans_num', 'count'),
        monto_g=('amt', 'sum')
    ).reset_index()
    
    df_gender_pivot = df_gender.pivot_table(
        index=['city', 'state_name'],
        columns='gender',
        values=['cant_g', 'monto_g'],
        fill_value=0
    )
    df_gender_pivot.columns = ['_'.join(col).strip() for col in df_gender_pivot.columns]
    df_gender_pivot = df_gender_pivot.reset_index()
    
    # Unir todo
    df_cities = df_cities.merge(df_totals, on=['city', 'state_name'], how='left')
    df_cities = df_cities.merge(df_gender_pivot, on=['city', 'state_name'], how='left')
    
    # Tomar las ciudades con más transacciones por género
    df_cities = df_cities.groupby('gender').apply(
        lambda x: x.nlargest(max_cities, 'cantidad')
    ).reset_index(drop=True)
    
    # Crear el mapa
    fig = go.Figure()
    
    for gender in df_cities['gender'].unique():
        df_g = df_cities[df_cities['gender'] == gender]
        
        # Crear hover con información de ambos géneros
        hover_texts = []
        for _, row in df_g.iterrows():
            cant_f = row.get('cant_g_F', 0)
            cant_m = row.get('cant_g_M', 0)
            monto_f = row.get('monto_g_F', 0)
            monto_m = row.get('monto_g_M', 0)
            
            text = (
                f"<b>{row['city']}, {row['state_name']}</b><br>"
                f"<b>Total ciudad:</b> {row['cantidad_total']:,.0f} trans | ${row['monto_ciudad']:,.0f}<br>"
                f"─────────────────<br>"
                f"<span style='color:#e74c3c'>♀ Femenino:</span> {cant_f:,.0f} trans | ${monto_f:,.0f}<br>"
                f"<span style='color:#3498db'>♂ Masculino:</span> {cant_m:,.0f} trans | ${monto_m:,.0f}<br>"
                f"─────────────────<br>"
                f"Población: {row['poblacion']:,.0f}"
            )
            hover_texts.append(text)
        
        fig.add_trace(go.Scattermapbox(
            lat=df_g['lat'],
            lon=df_g['long'],
            mode='markers',
            marker=dict(
                size=df_g['cantidad'] / df_g['cantidad'].max() * 25 + 8,
                color=COLORS.get(gender, '#666666'),
                opacity=0.7
            ),
            text=hover_texts,
            hoverinfo='text',
            name=GENDER_LABELS.get(gender, gender)
        ))
    
    fig.update_layout(
        title='🗺️ Mapa de Concentración de Transacciones en Estados Unidos',
        mapbox=dict(
            style="carto-positron",
            center={"lat": 39.8283, "lon": -98.5795},
            zoom=3.2
        ),
        height=650,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)"
        ),
        showlegend=True
    )
    
    return fig


def crear_kpis(df_filtrado):
    """Crea los KPIs principales del dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_trans = len(df_filtrado)
        st.metric(label="📊 Total Transacciones", value=f"{total_trans:,}")
    
    with col2:
        monto_total = df_filtrado['amt'].sum()
        st.metric(label="💰 Monto Total", value=f"${monto_total:,.2f}")
    
    with col3:
        monto_promedio = df_filtrado['amt'].mean()
        st.metric(label="📈 Monto Promedio", value=f"${monto_promedio:,.2f}")
    
    with col4:
        estados_unicos = df_filtrado['state_name'].nunique()
        st.metric(label="🗺️ Estados", value=f"{estados_unicos}")


# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================
def main():
    """Función principal del dashboard."""
    
    # Título principal
    st.markdown("# 📊 Análisis de Transacciones por Género")
    
    # Cargar datos
    df = cargar_datos()
    
    if df is None:
        st.stop()
    
    # ==========================================================================
    # SIDEBAR - FILTROS
    # ==========================================================================
    with st.sidebar:
        st.markdown("## 🎛️ Filtros")
        st.markdown("---")
        
        # Filtro de género
        st.markdown("### 👥 Género")
        generos = st.multiselect(
            "Seleccionar género:",
            options=['M', 'F'],
            default=['M', 'F'],
            format_func=lambda x: GENDER_LABELS.get(x, x)
        )
        
        st.markdown("---")
        
        # Filtro temporal
        st.markdown("### 📅 Período")
        anios = sorted(df['anio'].unique())
        anio_sel = st.select_slider(
            "Año:",
            options=anios,
            value=(min(anios), max(anios))
        )
        
        meses_sel = st.slider("Meses:", min_value=1, max_value=12, value=(1, 12))
        
        st.markdown("---")
        
        # Filtro de estado
        st.markdown("### 🗺️ Ubicación")
        estados = sorted(df['state_name'].unique())
        estados_sel = st.multiselect("Estados:", options=estados, default=[])
        
        st.markdown("---")
        
        # Filtro de categoría
        st.markdown("### 🏪 Categoría")
        categorias = sorted(df['category'].unique())
        categorias_sel = st.multiselect(
            "Categorías:",
            options=categorias,
            default=[],
            format_func=lambda x: CATEGORIAS.get(x, x)
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.markdown(f"**Dataset:** {len(df):,} transacciones")
        st.markdown(f"**Estados:** {df['state_name'].nunique()}")
        st.markdown(f"**Categorías:** {df['category'].nunique()}")
    
    # ==========================================================================
    # APLICAR FILTROS
    # ==========================================================================
    df_filtrado = df.copy()
    
    if generos:
        df_filtrado = df_filtrado[df_filtrado['gender'].isin(generos)]
    
    df_filtrado = df_filtrado[
        (df_filtrado['anio'] >= anio_sel[0]) & (df_filtrado['anio'] <= anio_sel[1])
    ]
    
    df_filtrado = df_filtrado[
        (df_filtrado['mes'] >= meses_sel[0]) & (df_filtrado['mes'] <= meses_sel[1])
    ]
    
    if estados_sel:
        df_filtrado = df_filtrado[df_filtrado['state_name'].isin(estados_sel)]
    
    if categorias_sel:
        df_filtrado = df_filtrado[df_filtrado['category'].isin(categorias_sel)]
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ No hay datos con los filtros seleccionados. Ajusta los filtros.")
        st.stop()
    
    # ==========================================================================
    # KPIs
    # ==========================================================================
    st.markdown("## 📈 Métricas Principales")
    crear_kpis(df_filtrado)
    
    # KPIs por género
    if len(generos) > 1:
        st.markdown("### Por Género")
        cols = st.columns(len(generos))
        for i, g in enumerate(generos):
            df_g = df_filtrado[df_filtrado['gender'] == g]
            with cols[i]:
                st.markdown(f"**{GENDER_LABELS.get(g, g)}**")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Transacciones", f"{len(df_g):,}")
                with col_b:
                    st.metric("Monto Prom.", f"${df_g['amt'].mean():,.2f}")
    
    st.markdown("---")
    
    # ==========================================================================
    # HISTORIA DEL TABLERO - ANÁLISIS TEMPORAL COMO PRIORIDAD
    # ==========================================================================
    
    # --------------------------------------------------------------------------
    # SECCIÓN 1: EVOLUCIÓN TEMPORAL (PRIORIDAD)
    # --------------------------------------------------------------------------
    st.markdown("## 📅 1. ¿Cómo evoluciona el gasto en el tiempo?")
    st.markdown("""
    <div class="story-section">
    Esta sección muestra la evolución temporal de las transacciones, 
    permitiendo identificar tendencias, estacionalidades y patrones de comportamiento por género a lo largo del tiempo.
    </div>
    """, unsafe_allow_html=True)
    
    # Gasto total por año y género
    st.plotly_chart(grafico_evolucion_gasto_genero_anio(df_filtrado), use_container_width=True)
    
    # Evolución mensual
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_tendencia_mensual(df_filtrado), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_gasto_mensual_genero(df_filtrado), use_container_width=True)
    
    # Monto promedio mensual
    st.plotly_chart(grafico_monto_mensual(df_filtrado), use_container_width=True)
    
    # Patrón horario
    st.plotly_chart(grafico_distribucion_hora(df_filtrado), use_container_width=True)
    
    st.markdown("---")
    
    # --------------------------------------------------------------------------
    # SECCIÓN 2: ANÁLISIS POR GÉNERO
    # --------------------------------------------------------------------------
    st.markdown("## 👥 2. ¿Quién gasta más y en qué?")
    st.markdown("""
    <div class="story-section">
    Comparativa del comportamiento de gasto entre géneros: distribución de transacciones, 
    montos promedio y preferencias por categoría de comercio.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grafico_distribucion_genero(df_filtrado), use_container_width=True)
    with col2:
        st.plotly_chart(grafico_monto_genero(df_filtrado), use_container_width=True)
    
    # Categorías por género - con selector
    col_selector, col_espacio = st.columns([1, 4])
    with col_selector:
        top_n_cat = st.selectbox(
            "Mostrar categorías:",
            options=[10, 14],
            index=0,
            format_func=lambda x: f"Top {x}" if x < 14 else "Todas",
            key='top_n_categorias'
        )
    
    st.plotly_chart(grafico_categorias_genero(df_filtrado, top_n_cat), use_container_width=True)
    
    # Evolución temporal por categoría
    st.plotly_chart(grafico_evolucion_categoria_temporal(df_filtrado), use_container_width=True)
    
    st.markdown("---")
    
    # --------------------------------------------------------------------------
    # SECCIÓN 3: ANÁLISIS POR LUGAR
    # --------------------------------------------------------------------------
    st.markdown("## 🗺️ 3. ¿Dónde se concentran las transacciones?")
    st.markdown("""
    <div class="story-section">
    Análisis geográfico de las transacciones: distribución de gasto por género en los principales estados 
    y mapa de concentración que muestra dónde se realizan más transacciones en Estados Unidos.
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de ordenamiento y cantidad
    col_orden, col_cantidad, col_espacio = st.columns([1, 1, 3])
    with col_orden:
        ordenar_por = st.radio(
            "Ordenar por gasto:",
            options=['F', 'M'],
            format_func=lambda x: GENDER_LABELS.get(x, x),
            horizontal=True,
            key='orden_estados'
        )
    with col_cantidad:
        top_n = st.selectbox(
            "Mostrar estados:",
            options=[10, 20, 30, 40, 50],
            index=0,
            key='top_n_estados'
        )
    
    st.plotly_chart(grafico_proporcion_gasto_estados(df_filtrado, ordenar_por, top_n), use_container_width=True)
    
    # Mapa de concentración de transacciones
    st.markdown("### 🗺️ Mapa de Concentración de Transacciones")
    st.markdown("""
    El mapa muestra la distribución geográfica de las transacciones. El **tamaño** de cada punto 
    representa la cantidad de transacciones y el **color** indica el género (🔴 Rojo = Femenino, 🔵 Azul = Masculino).
    Al pasar el cursor sobre cada punto, verá el detalle de transacciones por ambos géneros en esa ciudad.
    Puede hacer zoom y desplazarse por el mapa para explorar las diferentes regiones.
    """)
    
    st.plotly_chart(mapa_concentracion_transacciones(df_filtrado), use_container_width=True)
    
    # ==========================================================================
    # FOOTER
    # ==========================================================================
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666666; padding: 1rem;'>
            📊 Dashboard de Análisis de Transacciones | Proyecto Integrador 5 | 2025
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
