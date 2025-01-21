# Estilos personalizados
st.markdown("""
    <style>
    /* Estilo base para el contenedor principal */
    .main {
        background-color: #f5f5f5;
        padding: 2rem;
        transition: all 0.3s ease;
    }

    /* Estilo para campos de texto pequeños (inputs) */
    .stTextInput > div > div > input {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2ecc71;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
        outline: none;
    }

    /* Estilo para áreas de texto grandes */
    .stTextArea > div > div > textarea {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 1rem;
        caret-color: #333;
        font-size: 1rem;
        line-height: 1.5;
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

    /* Estilo para botones */
    .stButton > button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #27ae60;
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
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
    </style>
    """, unsafe_allow_html=True)
