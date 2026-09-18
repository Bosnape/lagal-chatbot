# Asistente legal (chatbot)

Chatbot en Streamlit que responde preguntas sobre un tema puntual de derecho
colombiano, usando la API de Claude. Pensado para desplegarse como una app
web con link, sin que la persona que lo usa tenga que instalar nada.

## Estructura

- `app.py` — la app (interfaz de chat + llamada al modelo).
- `config.py` — tema, nombre de la app, modelo, mensaje de bienvenida.
- `context.md` — la base de conocimiento (hoy tiene contenido de ejemplo).
- `requirements.txt` — dependencias.
- `.streamlit/secrets.toml.example` — plantilla para la API key.

## 1. Probarlo en tu computador (opcional)

```bash
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edita .streamlit/secrets.toml y pega tu API key de Anthropic

streamlit run app.py
```

Se abre en `http://localhost:8501`.

## 2. Desplegarlo como link (recomendado para tu amiga)

Usando **Streamlit Community Cloud** (gratis):

1. Crea un repo en GitHub y sube esta carpeta (el `.gitignore` ya excluye
   `secrets.toml`, así que tu API key nunca se sube).
2. Entra a [share.streamlit.io](https://share.streamlit.io) con tu cuenta
   de GitHub.
3. "New app" → selecciona el repo → main file: `app.py` → Deploy.
4. Antes o después del deploy, ve a **Settings → Secrets** de la app y pega:

   ```toml
   ANTHROPIC_API_KEY = "sk-ant-tu-api-key-real"
   ```

5. Te da un link tipo `https://tu-app.streamlit.app`. Ese es el que le
   mandas a tu amiga — lo abre en el navegador, sin instalar nada.

> El costo por uso de la API corre por tu cuenta de Anthropic (tú pones la
> key). Si esperas mucho uso, vale la pena poner un límite de gasto en tu
> consola de Anthropic.

## 3. Cuando tengas el documento fuente del tema real

1. Reemplaza el contenido de `context.md` con el material real (puedes
   pegarlo tal cual, o resumido — entre más limpio, mejores respuestas).
2. Actualiza `TEMA` en `config.py` con el nombre real del tema (esto ajusta
   automáticamente el mensaje de bienvenida y las instrucciones del modelo).
3. Vuelve a subir los cambios a GitHub — Streamlit Community Cloud
   redespliega solo.

Si el documento es muy largo (varias decenas de páginas), avísame: en ese
caso conviene pasar de "todo el texto en el prompt" a una búsqueda tipo RAG
para no gastar de más ni perder precisión.

## Notas de diseño

- El prompt del sistema (en `app.py`) restringe al chatbot a responder solo
  sobre `config.TEMA`, y le pide decir "no tengo información suficiente" en
  vez de inventar cuando la base de conocimiento no alcanza.
- Incluye un disclaimer de que no reemplaza asesoría legal profesional.
- No hay base de datos ni login: cada quien que abre el link tiene su propia
  conversación en memoria, que se pierde al recargar la página. Si más
  adelante quieres guardar historial entre sesiones, es un paso aparte.
