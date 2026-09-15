import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuración de la página
st.set_page_config(page_title="Géminis Betting Analyst Pro", page_icon="⚽", layout="wide")

# --- EL PROMPT DE ROL QUE DEFINISTE ---
ROL_PROMPT = """
Actúa como un analista probabilístico de apuestas deportivas especializado principalmente en fútbol y baloncesto.
Tu objetivo es determinar:
1. Qué resultado es más probable.
2. Mercados con respaldo estadístico.
3. Si la cuota compensa el riesgo.
4. Cuándo no apostar.

PRINCIPIO FUNDAMENTAL: Nunca inventes datos. Diferencia entre información confirmada y suposiciones.
METODOLOGÍA: Analiza Contexto Competitivo, Estado de Plantillas, Rendimiento Estadístico (xG, tiros, etc.), Calidad de la muestra, H2H, Probabilidad y Valor.
FORMATO DE RESPUESTA: Sigue estrictamente el formato: Partido, Competición, Lectura, Contexto, Datos, Señales a favor/en contra, Pick Principal, Decisión Final y Stake (0-5).
"""

# Configuración de la API (Tu clave ya está aquí)
API_KEY = "AQ.Ab8RN6IkkxTWqIVSz-bU5-0lDBZBDvhXwuVAHlD1AXwho0bzqQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("🎯 Analizador de Apuestas Pro")
st.write("Sube la captura de tu partido y Géminis hará el análisis con tu metodología.")

archivo_subido = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    imagen = Image.open(archivo_subido)
    st.image(imagen, caption='Captura del partido', width=400)
    
    if st.button("🚀 ANALIZAR AHORA"):
        with st.spinner('Analizando datos y cuotas...'):
            try:
                # Convertir imagen para enviar
                img_byte_arr = io.BytesIO()
                imagen.save(img_byte_arr, format='PNG')
                
                # Llamada a la IA
                res = model.generate_content([
                    ROL_PROMPT,
                    {"mime_type": "image/png", "data": img_byte_arr.getvalue()}
                ])
                
                st.markdown("---")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("### Configuración Activa")
st.sidebar.info("Modelo: Gemini 1.5 Pro\nRol: Analista Probabilístico")
