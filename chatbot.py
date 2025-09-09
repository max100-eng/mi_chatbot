from nltk.chat.util import Chat, reflections

# Pares de patrones y respuestas
pares = [
    [
        r"mi nombre es (.*)",
        ["Hola %1, ¿cómo estás?",]
    ],
    [
        r"¿cuál es tu nombre?",
        ["Mi nombre es Chatbot.",]
    ],
    [
        r"¿cómo estás?",
        ["Bien, ¿y tú?",]
    ],
    [
        r"hola|hey|buenas",
        ["Hola", "Qué tal",]
    ],
    [
        r"¿qué (.*) quieres?",
        ["Nada gracias.",]
    ],
    [
        r"(.*) creado?",
        ["Fui creado por un programador.",]
    ],
]

# Crear una instancia del chatbot
chatbot = Chat(pares, reflections)

# Iniciar la conversación
def chatear():
    print("Hola, soy un bot. Escribe algo para comenzar.")
    chatbot.converse()

if __name__ == "__main__":
    chatear()