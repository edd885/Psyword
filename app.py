import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import datetime
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

# Descargar recursos necesarios de NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Configuración inicial de la página
st.set_page_config(
    page_title="Espacio de Introspección",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados mejorados
st.markdown("""
    <style>
    /* Estilo base para el contenedor principal */
    .main {
        color: #111827;
        background-color: #f5f5f5;
        padding: 2rem;
    }

    /* Estilo para campos de texto pequeños (inputs) */
    .stTextInput > div > div > input {
        background-color: white;
        color: #111827;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 0.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2ecc71;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
        outline: none;
    }

    /* Estilo mejorado para el área de texto principal */
    .stTextArea > div > div > textarea {
        background-color: white;
        color: #111827;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.1rem;
        line-height: 1.6;
        caret-color: #2ecc71;
        transition: all 0.3s ease;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #2ecc71;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
        outline: none;
    }

    /* Estilo para el selector de contexto */
    .context-selector {
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        background-color: white;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }

    .context-selector:hover {
        border-color: #2ecc71;
        transform: translateY(-1px);
    }

    /* Estilo mejorado para botones */
    .stButton > button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1rem 0;
        transition: all 0.3s ease;
        width: auto;
        min-width: 200px;
    }

    .stButton > button:hover {
        background-color: #27ae60;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.2);
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Estilo para los expanders */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        border-color: #2ecc71;
        background-color: rgba(46, 204, 113, 0.05);
    }

    /* Estilo para las métricas */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Ajustes adicionales para mejorar la legibilidad */
    div[data-baseweb="select"] {
        margin-bottom: 1rem;
    }

    .stMarkdown {
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_sentiment(text):
    """Analiza el sentimiento del texto y retorna los porcentajes."""
    blob = TextBlob(text)
    # Obtener polaridad y subjetividad
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Normalizar los valores para obtener porcentajes
    positive = max(0, polarity) * 100
    negative = abs(min(0, polarity)) * 100
    neutral = (1 - abs(polarity)) * 50
    
    return {
        "Positivo": positive,
        "Negativo": negative,
        "Neutral": neutral,
        "Subjetividad": subjectivity * 100
    }

def create_sentiment_chart(sentiments):
    """Crea un gráfico de barras para los sentimientos."""
    fig = go.Figure(data=[
        go.Bar(
            x=list(sentiments.keys()),
            y=list(sentiments.values()),
            marker_color=['#2ecc71', '#e74c3c', '#95a5a6', '#3498db']
        )
    ])
    
    fig.update_layout(
        title="Análisis de Sentimientos",
        yaxis_title="Porcentaje",
        xaxis_title="Tipo de Sentimiento",
        height=400,
        margin=dict(t=30, l=60, r=30, b=30)
    )
    
    return fig

def analyze_text_metrics(text):
    """Analiza métricas básicas del texto."""
    words = nltk.word_tokenize(text)
    return {
        "Palabras totales": len(words),
        "Palabras únicas": len(set(words)),
        "Oraciones": len(nltk.sent_tokenize(text))
    }

def main():
    # Selector de contexto
    context = st.selectbox(
        "Selecciona el contexto",
        ["Personal", "Empresarial", "Psicología", "Académico"],
        key="context"
    )
    
    # Título y descripción
    st.title("Espacio de Introspección")
    st.markdown("""
        <p style='font-size: 1.1em; color: #111827;'>
        Un espacio para explorar y analizar pensamientos y sentimientos.
        Mientras más completo sea tu escrito, mejor será el análisis.
        </p>
    """, unsafe_allow_html=True)
    
    # Información del usuario
    with st.expander("Datos de Usuario", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", key="nombre")
        with col2:
            fecha = st.date_input("Fecha", datetime.datetime.now())
    
    # Área principal para escribir
    st.markdown("### Introspección actual")
    texto_usuario = st.text_area(
        "",
        height=200,
        placeholder="Escribe libremente sobre tus pensamientos, sentimientos o reflexiones...",
        key="texto_principal"
    )
    
    # Botón de análisis claramente visible
    if st.button("Analizar texto", key="boton_analisis", type="primary"):
        if texto_usuario:
            with st.spinner('Analizando tu texto...'):
                # Análisis de sentimientos
                sentimientos = analyze_sentiment(texto_usuario)
                
                # Crear visualizaciones
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_sentimientos = create_sentiment_chart(sentimientos)
                    st.plotly_chart(fig_sentimientos, use_container_width=True)
                
                with col2:
                    # Word Cloud
                    stop_words = set(stopwords.words('spanish'))
                    wordcloud = WordCloud(
                        width=800,
                        height=400,
                        background_color='white',
                        stopwords=stop_words,
                        colormap='viridis'
                    ).generate(texto_usuario)
                    
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    st.pyplot(plt)
                
                # Métricas del texto
                st.markdown("### Métricas del texto")
                metricas = analyze_text_metrics(texto_usuario)
                cols = st.columns(len(metricas))
                for col, (metrica, valor) in zip(cols, metricas.items()):
                    col.metric(metrica, valor)
        else:
            st.warning('Por favor, escribe algo antes de iniciar el análisis.')
    
    # Pie de página
    st.markdown("""
        <div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 10px; text-align: center; font-size: 0.8em; color: #666;'>
        Tu privacidad es importante. Toda la información compartida aquí está protegida y es confidencial.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
