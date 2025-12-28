import os
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Apartment Recommender",
    page_icon="🏢",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # /app/website
DATA_DIR = os.path.join(BASE_DIR, "dataset")

# --------------------------------------------------
# --------------------------------------------------
# LOAD DATA (DOCKER & AWS SAFE)
# --------------------------------------------------

location_df = pickle.load(
    open(os.path.join(DATA_DIR, "distance_location.pkl"), "rb")
)

url_df = pickle.load(
    open(os.path.join(DATA_DIR, "url.pkl"), "rb")
)

# Property → URL mapping
url_dict = url_df.set_index("PropertyName")["Link"].to_dict()

cosine_sim1 = pickle.load(
    open(os.path.join(DATA_DIR, "Top_facilities.pkl"), "rb")
)

cosine_sim2 = pickle.load(
    open(os.path.join(DATA_DIR, "price_based.pkl"), "rb")
)

cosine_sim3 = pickle.load(
    open(os.path.join(DATA_DIR, "location_based.pkl"), "rb")
)

# --------------------------------------------------
# RECOMMENDER FUNCTION
# --------------------------------------------------
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores,
        'Link': [url_dict.get(p, "") for p in top_properties]
    })

    return recommendations_df

# --------------------------------------------------
# CENTERED PAGE LAYOUT (full width, no side margin)
# --------------------------------------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

st.title("📍 Apartment Recommender")
st.markdown("### Find nearby apartments and recommend similar properties")
st.divider()

# --------------------------------------------------
# UI: Location + Radius
# --------------------------------------------------
st.subheader("Search Nearby Apartments")
selected_location = st.selectbox('Select Location', sorted(location_df.columns.to_list()))
radius = st.number_input('Radius in KM', min_value=0.5, step=0.5)

# Initialize session state
if "nearby_searched" not in st.session_state:
    st.session_state.nearby_searched = False
    st.session_state.nearby_results = []

# Nearby search button
if st.button('Search Nearby'):
    # Filter apartments within radius
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()
    st.session_state.nearby_results = list(result_ser.index)
    st.session_state.nearby_searched = True

# Show nearby apartments
if st.session_state.nearby_searched:
    if st.session_state.nearby_results:
        st.write("### Nearby Apartments:")
        for name in st.session_state.nearby_results:
            st.text(f"• {name}")
    else:
        st.warning("No apartments found in this radius 😕")

st.divider()

# --------------------------------------------------
# UI: Recommendations (enable only after search)
# --------------------------------------------------
if st.session_state.nearby_searched:
    st.subheader("Recommend Similar Apartments")
    # Full apartment list for selection
    selected_apartment = st.selectbox('Select an apartment for recommendations', sorted(location_df.index.to_list()))

    if "recommend_clicked" not in st.session_state:
        st.session_state.recommend_clicked = False

    if st.button('Recommend'):
        st.session_state.recommend_clicked = True
        st.session_state.recommend_apartment = selected_apartment

    if st.session_state.recommend_clicked:
        recommendation_df = recommend_properties_with_scores(st.session_state.recommend_apartment)

        # Build Markdown table with clickable links
        table_md = "| Property Name | Similarity Score | Link |\n|---|---|---|\n"
        for _, row in recommendation_df.iterrows():
            name = row['PropertyName']
            score = round(row['SimilarityScore'], 3)
            link = row['Link']
            link_md = f"[View Property]({link})" if link else "-"
            table_md += f"| {name} | {score} | {link_md} |\n"

        st.markdown("### 🔍 Recommended Apartments")
        st.markdown(table_md, unsafe_allow_html=True)
else:
    st.info("Search nearby apartments first to enable recommendations 🧭")

st.markdown("</div>", unsafe_allow_html=True)
