import streamlit as st

st.title("Mi primer chatbot")

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
    # Mostrar el mensaje del usuario en el contenedor del chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simular una respuesta del asistente
    with st.chat_message("assistant"):
        response = f"¡Hola! Has dicho: {prompt}"
        st.markdown(response)
    # Añadir la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": response})