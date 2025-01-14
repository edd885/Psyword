import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Configuración necesaria para Streamlit Cloud
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import datetime
import os

def download_nltk_data():
    """
    Descarga los datos necesarios de NLTK si no están disponibles.
    Esta función es crucial para el funcionamiento en Streamlit Cloud.
    """
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)

def contar_palabras(texto):
    """
    Cuenta el número de palabras en el texto ingresado.
    Ignora espacios en blanco múltiples y líneas vacías.
    """
    if not texto:
        return 0
    palabras = texto.strip().split()
    return len(palabras)

def obtener_color_progreso(num_palabras):
    """
    Determina el color de la barra de progreso basado en el número de palabras.
    Retorna un color y un mensaje apropiado según el rango de palabras.
    """
    if num_palabras < 150:
        return "orange", "Continúa escribiendo para obtener una mejor visualización"
    elif num_palabras <= 300:
        return "green", "¡Longitud ideal para el análisis!"
    else:
        return "blue", "Has superado la longitud recomendada, pero puedes continuar si lo deseas"

def main():
    # Asegurar que los datos de NLTK estén disponibles
    download_nltk_data()
    
    # Configuración inicial de la página
    st.set_page_config(
        page_title="Notas Pre-Consulta",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items=None
    )

    # Estilos personalizados para mejorar la visibilidad y contraste
    st.markdown("""
        <style>
        /* Estilo general de la página */
        .main {
            background-color: #ffffff;
            color: #000000;
            padding: 2rem;
        }
        
        /* Asegurar visibilidad de títulos */
        h1, h2, h3 {
            color: #000000 !important;
            font-weight: bold;
        }
        
        /* Estilos para campos de entrada */
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
        }
        
        .stTextArea > div > div > textarea {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
        }
        
        /* Estilos para contadores y medidores */
        .palabra-contador {
            font-size: 1.2em;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            background-color: #f8f9fa;
        }
        
        .tiempo-estimado {
            font-style: italic;
            color: #666666;
            margin-bottom: 15px;
        }
        
        /* Estilos para mensajes del sistema */
        .stSuccess, .stInfo, .stWarning {
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

    # Título y descripción principal
    st.title("Espacio de Reflexión Pre-Consulta")
    st.markdown("""
        Este es un espacio seguro para expresar tus pensamientos y sentimientos 
        antes de tu sesión. La longitud ideal es entre 150 y 300 palabras 
        (aproximadamente 5-15 minutos de escritura).
    """)
    
    # Sección de información personal
    with st.expander("Información Personal", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", key="nombre")
        with col2:
            fecha = st.date_input("Fecha", datetime.datetime.now())
    
    # Área principal para escritura
    st.markdown("### ¿Cómo te sientes hoy?")
    texto_paciente = st.text_area(
        "",
        height=200,
        placeholder="Escribe libremente sobre tus pensamientos, sentimientos o preocupaciones...",
        key="texto_principal"
    )
    
    # Sistema de retroalimentación visual
    num_palabras = contar_palabras(texto_paciente)
    color_barra, mensaje = obtener_color_progreso(num_palabras)
    
    # Visualización del progreso
    col1, col2 = st.columns([2, 1])
    with col1:
        st.progress(min(num_palabras / 300, 1.0), text=f"{num_palabras} palabras")
    with col2:
        tiempo_estimado = max(1, int(num_palabras / 30))
        st.info(f"≈ {tiempo_estimado} min")
    
    st.markdown(f"<div style='color: {color_barra};'>{mensaje}</div>", unsafe_allow_html=True)
    
    # Procesamiento y visualización
    if st.button("Generar Visualización", type="primary", disabled=num_palabras < 50):
        if texto_paciente:
            try:
                # Configuración de stop words en español
                stop_words = set(stopwords.words('spanish'))
                
                # Crear y configurar el word cloud
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    stopwords=stop_words,
                    colormap='viridis',
                    min_word_length=3
                ).generate(texto_paciente)
                
                # Mostrar el word cloud
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)
                
                if nombre:
                    st.success("Información procesada exitosamente")
            
            except Exception as e:
                st.error(f"Hubo un error al procesar el texto: {str(e)}")
        else:
            st.warning("Por favor, escribe algo antes de generar la visualización.")
    
    # Pie de página con información de privacidad
    st.markdown("""
        <div style='margin-top: 2rem; padding: 10px; text-align: center; 
        font-size: 0.8em; color: #666666; background-color: #f8f9fa; 
        border-radius: 5px;'>
        Tu privacidad es importante. Toda la información compartida aquí está 
        protegida y es confidencial.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
