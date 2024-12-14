import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Model va label encoderlarni yuklash
model_path = "samolyot_model.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Parametrlar bo'yicha label encoderlar
encoders = {
    "Model": ["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A350", "Cessna 172"],
    "Aircraft brand": ["Boeing", "Airbus", "Cessna"]
}

# Streamlit ilovasi
st.title("Samolyot narxini bashorat qilish")

# Foydalanuvchi kiritishlari
model_input = st.selectbox("Modelni tanlang", encoders["Model"])
o_rindiqlar = st.slider("O‘rindiqlar soni", min_value=4, max_value=400, step=1)
parvoz_masofasi = st.slider("Parvoz masofasi (km)", min_value=500, max_value=15000, step=100)
yonilgi_sarfi = st.number_input("Yonilg‘i sarfi (litr/soat)", min_value=50.0, max_value=5000.0, step=50.0)
ishlab_chiqarilgan_yil = st.slider("Ishlab chiqarilgan yil", min_value=1980, max_value=2023, step=1)
brendi = st.selectbox("Samolyot brendi", encoders["Aircraft brand"])
xom_ashyo_cost = st.number_input("Xom ashyo narxi ($)", min_value=10000.0, max_value=500000.0, step=1000.0)
valyuta_kursi = st.number_input("Valyuta kursi", min_value=1.0, max_value=1.2, step=0.01)

# Label kodlash
model_encoded = encoders["Model"].index(model_input)
brendi_encoded = encoders["Aircraft brand"].index(brendi)

# Ma'lumotni birlashtirish
input_data = pd.DataFrame({
    "Model": [model_encoded],
    "Number of seats": [o_rindiqlar],
    "Flight distance (km)": [parvoz_masofasi],
    "Fuel consumption (liter/hour)": [yonilgi_sarfi],
    "Year of manufacture": [ishlab_chiqarilgan_yil],
    "Aircraft brand": [brendi_encoded],
    "raw material cost": [xom_ashyo_cost],
    "Exchange rate": [valyuta_kursi]
})

# Ma'lumotlarni modelga moslashtirish
input_data = input_data[["Model", "Number of seats", "Flight distance (km)", "Fuel consumption (liter/hour)", 
                         "Year of manufacture", "Aircraft brand", "raw material cost", "Exchange rate"]]

# Bashorat qilish
if st.button("Narxni bashorat qilish"):
    prediction = model.predict(input_data.values)[0]
    st.success(f"Bashorat qilingan narx: ${prediction:,.2f} mln")
