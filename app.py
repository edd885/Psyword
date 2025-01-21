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

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: grey;
    }
    .stTextArea > div > div > textarea {
        background-color: white;
        caret-color: #333;  /* Color del cursor */
    }
    .context-selector {
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_sentiment(text):
    """Analiza el sentimiento del texto y retorna los porcentajes."""
    blob = TextBlob(text)
    # Obtener polaridad y subjetividad
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Categorizar sentimientos
    if polarity > 0:
        sentiment = "Positivo"
        score = polarity
    elif polarity < 0:
        sentiment = "Negativo"
        score = abs(polarity)
    else:
        sentiment = "Neutral"
        score = 0.5
        
    return {
        "Positivo": max(0, polarity) * 100,
        "Negativo": abs(min(0, polarity)) * 100,
        "Neutral": (1 - abs(polarity)) * 50,
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
        height=400
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
        <p style='font-size: 1.1em; color: #555;'>
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
    
    # Procesamiento y visualización
    if texto_usuario:
        col1, col2 = st.columns(2)
        
        with col1:
            # Análisis de sentimientos
            sentimientos = analyze_sentiment(texto_usuario)
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
    
    # Pie de página
    st.markdown("""
        <div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 10px; text-align: center; font-size: 0.8em; color: #666;'>
        Tu privacidad es importante. Toda la información compartida aquí está protegida y es confidencial.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
