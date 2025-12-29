print("🔥 PREDICTOR FILE LOADED")


import os
import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

import streamlit as st
import pandas as pd
import numpy as np
import joblib


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Price Prediction",
    page_icon="💰",
    layout="wide"
)

# --------------------------------------------------
# CENTERED PAGE CONTAINER
# --------------------------------------------------
st.title("💰 Property Price Predictor", anchor=None)
st.caption("ML-based price estimation for Gurgaon properties")
st.divider()

# --------------------------------------------------
# LOAD MODEL & DATA

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # /app/website
DATA_DIR = os.path.join(BASE_DIR, "dataset")

# --------------------------------------------------
df = joblib.load(
    os.path.join(DATA_DIR, "df.pkl")
)

pipeline = joblib.load(
    os.path.join(DATA_DIR, "price_prediction.pkl")
)


# --------------------------------------------------
# INPUT SECTION: 4 ROWS × 3 COLUMNS (centered)
# --------------------------------------------------
st.subheader("Enter Property Details")

with st.container():
    # Row 1
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        property_type = st.selectbox('Property Type', ['flat', 'house'])
    with r1c2:
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
    with r1c3:
        bedrooms = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))

    # Row 2
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        bathroom = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
    with r2c2:
        balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
    with r2c3:
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

    # Row 3
    r3c1, r3c2, r3c3 = st.columns(3)
    with r3c1:
        built_up_area = float(st.number_input('Built Up Area'))
    with r3c2:
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
    with r3c3:
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

    # Row 4
    r4c1, r4c2, r4c3 = st.columns(3)
    with r4c1:
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    with r4c2:
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    with r4c3:
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

st.divider()

# --------------------------------------------------
# PREDICT BUTTON
# --------------------------------------------------
predict = st.button("Predict Price 💸", type="primary", use_container_width=True)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
if predict:
    data = [[property_type, sector, bedrooms, bathroom, balcony,
             property_age, built_up_area, servant_room, store_room,
             furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    input_df = pd.DataFrame(data, columns=columns)

    base_price = np.expm1(pipeline.predict(input_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    st.success("Prediction generated successfully 🚀")

    # Metrics centered
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Minimum Price", f"₹ {low:.2f} Cr")
    with c2:
        st.metric("Estimated Price", f"₹ {base_price:.2f} Cr")
    with c3:
        st.metric("Maximum Price", f"₹ {high:.2f} Cr")
