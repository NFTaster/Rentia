import streamlit as st
import openai
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Tu DB inicial (agrega Airtable después)
properties_df = pd.DataFrame([
    {"id": 1, "title": "Monoambiente Rioja 2513 ⭐", "barrio": "Centro", "precio": 420000, "personas": 4, "fechas": "15-20 Feb", "amenities": "BTC, renovado", "fotos": "https://via.placeholder.com/300x200?text=Rioja+2513", "desc": "Perfecto para familia, centro Rosario"},
    {"id": 2, "title": "Hotel Puerto Norte 20 rooms", "barrio": "Puerto Norte", "precio": 480000, "personas": 4, "fechas": "Disponible ya", "amenities": "Pileta, desayuno", "fotos": "https://via.placeholder.com/300x200?text=Hotel+PN", "desc": "Full amenities, vistas río"},
    # Agrega más: tus propiedades
])

# Función búsqueda IA
@st.cache_data
def search_properties(query: str, min_price: int, max_price: int, barrio: str):
    prompt = f"Query: '{query}'. Filtros precio {min_price}-{max_price}k, barrio {barrio}. Props: {properties_df.to_dict('records')}. Devuelve TOP 5 ordenados por match % descending. JSON: [['id','title','precio','score']] español."
    try:
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        # Simula resultados (parse real después)
        results = properties_df[(properties_df['precio'] >= min_price) & (properties_df['precio'] <= max_price)]
        results = results.assign(score=pd.Series([95, 88, 92], index=results.index).fillna(80))
        return results.sort_values('score', ascending=False).head(5)
    except:
        return properties_df.head(5)  # Fallback

st.set_page_config(layout="wide")
st.title("🏠 Matching Rosario IA - Como Airbnb")
col1, col2 = st.columns(2)
with col1:
    query = st.text_input("📍 Busca: destino, fechas, huéspedes", "Centro Rosario, 4 personas, febrero")
    min_p, max_p = st.slider("💰 Precio ARS", 200000, 800000, (300000, 500000))
with col2:
    barrio = st.selectbox("Barrio", ["Todos", "Centro", "Puerto Norte", "Pichincha"])
    amenities = st.multiselect("Extras", ["Pileta", "BTC", "Desayuno"])

if st.button("🔍 Buscar Propiedades", type="primary"):
    results = search_properties(query, min_p, max_p, barrio)
    for _, prop in results.iterrows():
        colA, colB, colC = st.columns([3,1,1])
        with colA:
            st.markdown(f"**{prop['title']}** ⭐ {prop.get('score', 90):.0f}%")
            st.caption(f"{prop['barrio']} | ${prop['precio']/1000:.0f}k | {prop['personas']}p | {prop['amenities']}")
        with colB:
            st.image(prop['fotos'], width=150)
        with colC:
            st.button(f"Reservar ID{prop['id']}", key=prop['id'])

st.sidebar.info("🚀 MVP deploy Streamlit. Agrega tu OpenAI key en secrets.")
