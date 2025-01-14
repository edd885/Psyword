import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import datetime

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
    Retorna un color y un mensaje apropiado.
    """
    if num_palabras < 150:
        return "orange", "Continúa escribiendo para obtener una mejor visualización"
    elif num_palabras <= 300:
        return "green", "¡Longitud ideal para el análisis!"
    else:
        return "blue", "Has superado la longitud recomendada, pero puedes continuar si lo deseas"

def main():
    # Configuración inicial de la página
    st.set_page_config(
        page_title="Notas Pre-Consulta",
        page_icon="🧠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Estilo personalizado con indicadores visuales
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 2rem;
        }
        .palabra-contador {
            font-size: 1.2em;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .tiempo-estimado {
            font-style: italic;
            color: #666;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Título y descripción
    st.title("Espacio de Reflexión Pre-Consulta")
    st.markdown("""
        Este es un espacio seguro para expresar tus pensamientos y sentimientos 
        antes de tu sesión. La longitud ideal es entre 150 y 300 palabras 
        (aproximadamente 5-15 minutos de escritura).
    """)
    
    # Información del paciente
    with st.expander("Información Personal", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", key="nombre")
        with col2:
            fecha = st.date_input("Fecha", datetime.datetime.now())
    
    # Área principal para escribir
    st.markdown("### ¿Cómo te sientes hoy?")
    texto_paciente = st.text_area(
        "",
        height=200,
        placeholder="Escribe libremente sobre tus pensamientos, sentimientos o preocupaciones...",
        key="texto_principal"
    )
    
    # Contador de palabras y retroalimentación visual
    num_palabras = contar_palabras(texto_paciente)
    color_barra, mensaje = obtener_color_progreso(num_palabras)
    
    # Mostrar progreso
    col1, col2 = st.columns([2, 1])
    with col1:
        st.progress(min(num_palabras / 300, 1.0), text=f"{num_palabras} palabras")
    with col2:
        tiempo_estimado = max(1, int(num_palabras / 30))  # Estimación aproximada
        st.info(f"≈ {tiempo_estimado} min")
    
    st.markdown(f"<div style='color: {color_barra};'>{mensaje}</div>", unsafe_allow_html=True)
    
    # Botón para procesar el texto
    if st.button("Generar Visualización", type="primary", disabled=num_palabras < 50):
        if texto_paciente:
            try:
                # Configurar stop words en español
                nltk.download('stopwords', quiet=True)
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
                    st.success("Información guardada exitosamente")
            
            except Exception as e:
                st.error(f"Hubo un error al procesar el texto: {str(e)}")
        else:
            st.warning("Por favor, escribe algo antes de generar la visualización.")
    
    # Pie de página
    st.markdown("""
        <div style='margin-top: 2rem; padding: 10px; text-align: center; font-size: 0.8em; color: #666;'>
        Tu privacidad es importante. Toda la información compartida aquí está protegida y es confidencial.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
