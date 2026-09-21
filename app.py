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
ruta_contexto = Path(__file__).parent / config.CONTEXTO_PATH
if not ruta_contexto.exists():
    st.error(f"No se encontró la base de conocimiento ({config.CONTEXTO_PATH}).")
    st.stop()

CONTEXTO = ruta_contexto.read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""Eres un asistente conversacional especializado en {config.TEMA}, \
en el contexto del derecho colombiano.

Reglas estrictas:
1. Solo puedes responder preguntas relacionadas con {config.TEMA}. Si te preguntan \
sobre cualquier otro tema (incluyendo otras áreas del derecho no cubiertas aquí), \
responde amablemente que no puedes ayudar con eso porque está fuera de tu alcance, \
y no intentes responderlo de todas formas.
2. Responde ÚNICAMENTE con lo que esté en la "BASE DE CONOCIMIENTO" de abajo. No uses \
conocimiento externo ni cites artículos, plazos, cifras, teléfonos o entidades que no \
aparezcan allí. Si la pregunta cae dentro de tu alcance pero la base no cubre el dato, \
dilo explícitamente y sugiere consultar a un abogado o a la SIC, en vez de inventar.
3. Cuando la base lo permita, indica la norma en la que te apoyas (por ejemplo, \
art. 51 de la Ley 1480) y distingue lo que dice la ley de lo que es una recomendación práctica.
4. Si la respuesta depende de datos que el usuario no dio (medio de pago, si el vendedor \
está en Colombia, fecha de la compra), pregúntalos antes de concluir.
5. No eres un abogado y esto no reemplaza una asesoría legal profesional. Si la \
conversación se acerca a una decisión legal concreta e importante, recuérdalo.
6. Responde siempre en español, de forma clara y conversacional, sin relleno innecesario.

BASE DE CONOCIMIENTO:
---
{CONTEXTO}
---
"""

PREGUNTAS_RAPIDAS = [
    "El producto que compré nunca llegó",
    "Recibí un producto diferente al que compré",
    "Quiero cancelar una compra que ya hice",
    "Creo que fui víctima de un fraude",
    "¿Puedo recuperar mi dinero?",
    "No logro contactar al vendedor",
]

st.title(f"⚖️ {config.NOMBRE_APP}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(config.MENSAJE_BIENVENIDA)

# Los botones solo aparecen antes de la primera pregunta del usuario.
botones = st.empty()
if not st.session_state.messages:
    with botones.container():
        st.caption("Ejemplos de preguntas frecuentes:")
        columnas = st.columns(2)
        for i, texto in enumerate(PREGUNTAS_RAPIDAS):
            if columnas[i % 2].button(texto, use_container_width=True, key=f"rapida_{i}"):
                st.session_state.pregunta_rapida = texto

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pregunta = st.chat_input("Escribe tu pregunta...") or st.session_state.pop(
    "pregunta_rapida", None
)

if pregunta:
    botones.empty()
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):

        def generar_respuesta():
            with client.messages.stream(
                model=config.MODEL,
                max_tokens=2048,
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
