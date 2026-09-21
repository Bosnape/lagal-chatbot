from pathlib import Path

import streamlit as st
from anthropic import Anthropic

import config

st.set_page_config(page_title=config.NOMBRE_APP, page_icon="⚖️")

# --- API key ---
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
except FileNotFoundError:  # no existe ningún secrets.toml
    api_key = None
if not api_key:
    st.error(
        "Falta configurar la API key de Anthropic. Agrégala en "
        "Settings → Secrets de esta app (ANTHROPIC_API_KEY)."
    )
    st.stop()

client = Anthropic(api_key=api_key)


# --- Base de conocimiento ---
@st.cache_data
def cargar_contexto() -> str:
    ruta = Path(config.CONTEXTO_PATH)
    return ruta.read_text(encoding="utf-8") if ruta.exists() else ""


CONTEXTO = cargar_contexto()

SYSTEM_PROMPT = f"""Eres un asistente conversacional especializado en {config.TEMA}, \
en el contexto del derecho colombiano.

Reglas estrictas:
1. Solo puedes responder preguntas relacionadas con {config.TEMA}. Si te preguntan \
sobre cualquier otro tema (incluyendo otras áreas del derecho no cubiertas aquí), \
responde amablemente que no puedes ayudar con eso porque está fuera de tu alcance, \
y no intentes responderlo de todas formas.
2. Basa tus respuestas en la información de la sección "BASE DE CONOCIMIENTO" de abajo. \
Si la pregunta cae dentro de tu alcance pero no tienes información suficiente para \
responder con seguridad, dilo explícitamente en vez de inventar una respuesta.
3. No eres un abogado y esto no reemplaza una asesoría legal profesional. Si la \
conversación se acerca a una decisión legal concreta e importante, recuérdalo.
4. Responde siempre en español, de forma clara y conversacional, sin relleno innecesario.

BASE DE CONOCIMIENTO:
---
{CONTEXTO}
---
"""

st.title(f"⚖️ {config.NOMBRE_APP}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(config.MENSAJE_BIENVENIDA)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pregunta = st.chat_input("Escribe tu pregunta...")

if pregunta:
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):

        def generar_respuesta():
            with client.messages.stream(
                model=config.MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            ) as stream:
                yield from stream.text_stream

        try:
            respuesta = st.write_stream(generar_respuesta)
        except Exception as e:
            respuesta = (
                "Tuve un problema para responder (revisa la API key o la conexión). "
                f"Detalle técnico: {e}"
            )
            st.write(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
