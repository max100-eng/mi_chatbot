import streamlit as st

st.title("Mi primer chatbot inteligente")

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial del chat al volver a ejecutar la app
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar la entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    # Añadir el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Lógica de respuesta mejorada
    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()
        if "hola" in prompt_lower or "saludo" in prompt_lower:
            response = "¡Hola! ¿En qué puedo ayudarte?"
        elif "nombre" in prompt_lower:
            response = "Soy un chatbot de ejemplo creado con Streamlit."
        elif "adios" in prompt_lower or "chao" in prompt_lower:
            response = "¡Hasta la próxima! 😊"
        elif "clima" in prompt_lower:
            response = "No tengo información del clima, pero puedo ayudarte con otras cosas."
        else:
            response = "No entiendo lo que dices. ¿Puedes ser más específico?"
        
        st.markdown(response)
    
    # Añadir la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": response})