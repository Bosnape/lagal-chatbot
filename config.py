"""
Configuración central del chatbot.

Edita este archivo cuando definas el tema exacto y tengas el documento fuente.
No deberías necesitar tocar app.py para eso.
"""

# Tema exacto de derecho colombiano que el chatbot puede cubrir.
# TODO: reemplazar con el tema real (ej. "derecho de arrendamiento urbano en Colombia").
TEMA = "un tema de derecho colombiano (pendiente de definir)"

# Nombre visible de la app en la interfaz.
NOMBRE_APP = "Asistente Legal"

# Archivo con el material fuente (leyes, doctrina, resúmenes, jurisprudencia, etc.).
# Todo su contenido se inyecta en el prompt del sistema como base de conocimiento.
CONTEXTO_PATH = "context.md"

# Modelo de Claude a usar (alias sin fecha = siempre la versión estable más reciente).
MODEL = "claude-sonnet-5"

# Mensaje que ve el usuario al abrir el chat.
MENSAJE_BIENVENIDA = (
    f"¡Hola! Soy un asistente que responde preguntas sobre {TEMA}. "
    "Solo puedo ayudarte dentro de ese alcance — para otros temas no voy a poder responder."
)
