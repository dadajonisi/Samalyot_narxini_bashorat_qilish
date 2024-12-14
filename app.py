import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Model va label encoderlarni yuklash
model_path = "samolyot_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Parametrlar bo'yicha label encoderlar
categorical_columns = ["Model", "Turi", "Samolyot brendi"]
encoders = {
    "Model": ["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A350", "Cessna 172"],
    "Turi": ["Yo'lovchi", "Yuk tashish"],
    "Samolyot brendi": ["Boeing", "Airbus", "Cessna"]
}

# Streamlit ilovasi
st.title("Samolyot narxini bashorat qilish")

# Foydalanuvchi kiritishlari
model_input = st.selectbox("Modelni tanlang", encoders["Model"])
o_rindiqlar = st.slider("O‘rindiqlar soni", min_value=4, max_value=400, step=1)
parvoz_masofasi = st.slider("Parvoz masofasi (km)", min_value=500, max_value=15000, step=100)
yonilgi_sarfi = st.number_input("Yonilg‘i sarfi (litr/soat)", min_value=50.0, max_value=5000.0, step=50.0)
ishlab_chiqarilgan_yil = st.slider("Ishlab chiqarilgan yil", min_value=1980, max_value=2023, step=1)
brendi = st.selectbox("Samolyot brendi", encoders["Samolyot brendi"])
texnik_xizmat = st.number_input("Texnik xizmat xarajatlari ($)", min_value=50000.0, max_value=2000000.0, step=10000.0)
valyuta_kursi = st.number_input("Valyuta kursi", min_value=1.0, max_value=1.2, step=0.01)

# Label kodlash
model_encoded = encoders["Model"].index(model_input)
brendi_encoded = encoders["Samolyot brendi"].index(brendi)

# Ma'lumotni birlashtirish
input_data = pd.DataFrame({
    "Model": [model_encoded],
    "O‘rindiqlar soni": [o_rindiqlar],
    "Parvoz masofasi (km)": [parvoz_masofasi],
    "Yonilg‘i sarfi (litr/soat)": [yonilgi_sarfi],
    "Ishlab chiqarilgan yil": [ishlab_chiqarilgan_yil],
    "Samolyot brendi": [brendi_encoded],
    "Texnik xizmat ko‘rsatish xarajatlari": [texnik_xizmat],
    "Valyuta kursi": [valyuta_kursi]
})

# Bashorat qilish
if st.button("Narxni bashorat qilish"):
    prediction = model.predict(input_data)[0]
    st.success(f"Bashorat qilingan narx: ${prediction:,.2f} mln")
