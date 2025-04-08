import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="CodeFixerAI", page_icon="🛠️", layout="centered")

st.title("🛠️ CodeFixerAI")
st.subheader("Revisor y Corregidor de Código en Python con Inteligencia Artificial")

st.markdown("""
¿Tenés errores en tu código o simplemente querés mejorarlo?  
Pegá tu código en el área de abajo y dejá que **CodeFixerAI** lo revise y te dé una versión optimizada o corregida.
""")

user_code = st.text_area("📋 Pegá tu código en Python acá:", height=300)

if st.button("🔍 Revisar y Corregir"):
    if user_code.strip() == "":
        st.warning("Por favor, ingresá algo de código primero.")
    else:
        with st.spinner("Analizando tu código con IA..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Actuá como un experto en Python. Tu tarea es analizar y corregir el código que te enviaré. También mejoralo si es posible."},
                        {"role": "user", "content": user_code}
                    ],
                    temperature=0.4,
                    max_tokens=1500
                )
                fixed_code = response.choices[0].message.content
                st.success("✅ Código corregido:")
                st.code(fixed_code, language="python")
            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")