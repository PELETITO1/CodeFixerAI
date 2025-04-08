import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="CodeFixerAI", layout="centered")
st.title("CodeFixerAI – Tu Revisor de Código Inteligente")
st.markdown("Corrige, mejora y aprende de tu código en Python gracias a la IA.")

def mostrar_como_funciona():
    with st.expander("¿Cómo funciona CodeFixerAI?"):
        st.markdown("""
        **Características clave:**
        - Corrige errores de código Python automáticamente.
        - Devuelve una versión optimizada del código.
        - Ofrece una explicación breve de los cambios realizados.

        **Cómo usarlo:**
        1. Pega el código en el área de texto.
        2. Haz clic en **\"Revisar Código\"**.
        3. Observa el resultado y aprende de los cambios sugeridos.

        **Recomendaciones:**
        - Usa fragmentos de hasta 50 líneas.
        """)

mostrar_como_funciona()

codigo_entrada = st.text_area("Ingresa tu código en Python aquí:", height=300)

PROMPT_BASE = '''Eres un experto en programación en Python. Revisa el siguiente fragmento de código y realiza lo siguiente:
1. Corrige errores de sintaxis y lógica si existen.
2. Mejora la legibilidad del código si es posible.
3. Devuelve el código corregido.
4. Explica brevemente los cambios realizados (en un texto aparte, no en los comentarios del código).

Código a revisar:
"""
{codigo_usuario}
"""
'''

def obtener_respuesta_ia(codigo):
    prompt = PROMPT_BASE.format(codigo_usuario=codigo)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

if st.button("Revisar Código"):
    if not codigo_entrada.strip():
        st.warning("Por favor, ingresa algún código.")
    else:
        with st.spinner("Analizando tu código con IA..."):
            respuesta = obtener_respuesta_ia(codigo_entrada)

        partes = respuesta.split("```python")
        if len(partes) > 1:
            codigo_corregido = partes[1].split("```", 1)[0]
            explicacion = respuesta.replace(f"```python{codigo_corregido}```", "").strip()
            st.subheader("✅ Código Corregido")
            st.code(codigo_corregido, language="python")
            st.subheader("🧠 Explicación de Cambios")
            st.markdown(explicacion)
        else:
            st.info("Respuesta de la IA:")
            st.markdown(respuesta)