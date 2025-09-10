import streamlit as st
from nltk.chat.util import Chat, reflections
import nltk
import os

# --- CONFIGURACIÓN Y DESCARGA DE DATOS NLTK ---
NLTK_DATA_DIR = "nltk_data"
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DATA_DIR)

# Función para descargar datos de NLTK de forma segura
@st.cache_resource
def download_and_init_nltk():
    st.info("Intentando descargar/inicializar datos de NLTK y chatbot...")
    try:
        nltk.download('punkt', download_dir=NLTK_DATA_DIR, quiet=True)
        # --- PARES DE PATRONES Y RESPUESTAS PARA NLTK (MOVIDOS DENTRO DE ESTA FUNCIÓN) ---
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
        
        chatbot = Chat(pares, reflections)
        st.success("Chatbot NLTK inicializado correctamente.")
        return chatbot
    except Exception as e:
        st.error(f"Error crítico al inicializar el Chatbot: {e}")
        st.stop() # Detiene la ejecución de la app si hay un error fatal

# Asigna el chatbot inicializado a una variable global para la sesión
chatbot_nltk = download_and_init_nltk()

# --- TÍTULO DE LA APLICACIÓN ---
st.title("Mi Chatbot Inteligente con NLTK")

# --- RESTO DEL CÓDIGO ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = "Lo siento, el chatbot no pudo responder." # Default en caso de problemas
        if chatbot_nltk:
            st.info(f"Procesando prompt: '{prompt}'") # Mensaje de depuración
            try:
                response = chatbot_nltk.respond(prompt)
                if response is None:
                    response = "Disculpa, no pude encontrar una respuesta específica para eso."
                st.info(f"Respuesta de NLTK: '{response}'") # Mensaje de depuración
            except Exception as e:
                response = f"Ocurrió un error al procesar tu pregunta: {e}"
                st.error(f"Error en chatbot_nltk.respond(): {e}") # Mensaje de depuración para errores
        else:
            response = "Lo siento, el chatbot no está disponible en este momento debido a un error de inicialización."
        
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})