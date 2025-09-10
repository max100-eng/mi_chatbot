import streamlit as st
from nltk.chat.util import Chat, reflections
import nltk
import os # Para gestionar la descarga de datos NLTK

# --- CONFIGURACIÓN Y DESCARGA DE DATOS NLTK ---
# Define una ruta para los datos de NLTK dentro del directorio de la app
NLTK_DATA_DIR = "nltk_data"
# Asegúrate de que el directorio exista
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
# Añade esta ruta a la lista de paths donde NLTK buscará sus datos
nltk.data.path.append(NLTK_DATA_DIR)

# Función para descargar datos de NLTK de forma segura
@st.cache_resource # Usa st.cache_resource para descargar una sola vez por sesión
def download_nltk_data():
    try:
        # Descarga solo 'punkt' que es esencial para nltk.chat
        nltk.download('punkt', download_dir=NLTK_DATA_DIR, quiet=True)
        # Puedes añadir otros si los necesitas para futuras expansiones:
        # nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_DIR, quiet=True)
        # nltk.download('wordnet', download_dir=NLTK_DATA_DIR, quiet=True)
        # nltk.download('omw-1.4', download_dir=NLTK_DATA_DIR, quiet=True)
        st.success("Datos de NLTK descargados o ya presentes.")
    except Exception as e:
        st.error(f"Error al descargar datos de NLTK: {e}")
        st.info("Por favor, verifica tu conexión a internet o los permisos de escritura.")

download_nltk_data() # Ejecuta la descarga al inicio de la app

# --- TÍTULO DE LA APLICACIÓN ---
st.title("Mi Chatbot Inteligente con NLTK")

# --- PARES DE PATRONES Y RESPUESTAS PARA NLTK ---
# Ampliado con más ejemplos y una mejor gestión de lo que no entiende
pares = [
    # Saludos
    [
        r"hola|hey|buenas|que tal|saludos|buenos dias|buenas tardes|buenas noches",
        ["¡Hola!", "Qué tal", "¿En qué puedo ayudarte hoy?", "Hola, un placer saludarte."]
    ],
    # Nombre del bot
    [
        r"cual es tu nombre\?|como te llamas\?|quien eres\?",
        ["Mi nombre es Chatbot. Fui creado para conversar contigo.", "Soy un asistente virtual, puedes llamarme Chatbot."]
    ],
    # Estado del bot
    [
        r"como estas\?|que tal estas\?|estas bien\?",
        ["Estoy bien, gracias por preguntar. ¿Y tú cómo estás?", "Funcionando perfectamente. ¿Hay algo en lo que pueda ayudarte?"]
    ],
    # Preguntas sobre el usuario
    [
        r"mi nombre es (.*)|me llamo (.*)",
        ["¡Hola %1, qué gusto conocerte! ¿Cómo te puedo ayudar hoy?", "Encantado, %1. ¿Qué necesitas?"]
    ],
    [
        r"tengo una pregunta|quiero preguntar algo|puedes ayudarme\?",
        ["Claro, dime tu pregunta.", "¿En qué puedo ayudarte?", "Haré lo posible por asistirte."]
    ],
    # Despedidas
    [
        r"adios|chao|hasta luego|me voy|nos vemos",
        ["¡Adiós! Que tengas un excelente día.", "Hasta la próxima.", "Fue un placer ayudarte. ¡Vuelve pronto!"]
    ],
    # Agradecimientos
    [
        r"gracias|muchas gracias|te lo agradezco",
        ["De nada. Siempre a tu servicio.", "Con gusto.", "Para eso estoy."]
    ],
    # Creación del bot
    [
        r"(.*) (creo|creó|creaste|crearon) (.*)",
        ["Fui creado por un programador.", "Soy el resultado del trabajo de un desarrollador."]
    ],
    # Funcionalidad del bot
    [
        r"que haces\?|para que sirves\?",
        ["Estoy diseñado para conversar contigo y responder preguntas generales.", "Mi propósito es ayudarte a encontrar información y mantener una conversación."]
    ],
    # Clima (ejemplo para un tema específico que podría necesitar una API)
    [
        r"(.*) (clima|tiempo) (.*)",
        ["Lo siento, no tengo acceso a información en tiempo real sobre el clima.", "No puedo darte el pronóstico del tiempo en este momento."]
    ],
    # Preguntas sobre la existencia
    [
        r"eres real\?|existes\?",
        ["Soy un programa de software, no tengo una existencia física.", "Existo en el mundo digital."]
    ],
    # Comodín (última regla si ninguna de las anteriores coincide)
    [
        r"(.*)", # Atrapa cualquier entrada
        ["No estoy seguro de haber entendido bien. ¿Podrías reformular tu pregunta?",
         "Lo siento, parece que no tengo una respuesta para eso. ¿Podrías ser más específico?",
         "Hmm, no tengo esa información. ¿Hay algo más que te interese?",
         "Mi conocimiento es limitado para esa consulta. Prueba con otra pregunta."
        ]
    ]
]

# --- INICIALIZACIÓN DEL CHATBOT NLTK ---
# reflections es un diccionario de NLTK que permite sustituir pronombres
# (ej. "yo estoy" -> "tú estás") para hacer las respuestas más naturales.
chatbot_nltk = Chat(pares, reflections)

# --- INICIALIZACIÓN DEL HISTORIAL DE CHAT DE STREAMLIT ---
# 'st.session_state' es crucial para que el historial persista entre interacciones
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MOSTRAR MENSAJES DEL HISTORIAL ---
# Recorre los mensajes guardados y los muestra en la interfaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ENTRADA DEL USUARIO Y GENERACIÓN DE RESPUESTA ---
# st.chat_input crea el cuadro de texto para el usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    # Añadir el mensaje del usuario al historial y mostrarlo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta del chatbot NLTK
    with st.chat_message("assistant"):
        response = chatbot_nltk