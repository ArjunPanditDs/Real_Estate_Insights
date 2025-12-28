import streamlit as st

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏙️",
    layout="wide"
)

# ----------------------------------
# HERO SECTION
# ----------------------------------
st.title("🏙️ Gurgaon Real Estate Analytics")
st.caption("Data-driven insights • Machine Learning • Smart Recommendations")

st.markdown("""
This application provides **end-to-end real estate intelligence for Gurgaon** using  
**data analysis, machine learning models, and recommender systems**.
""")

st.divider()

# ----------------------------------
# KEY FEATURES
# ----------------------------------
st.subheader("🚀 What can you do with this app?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 💰 Price Prediction")
    st.markdown("""
    Predict property prices using  
    trained **ML regression models**  
    based on location & features.
    """)

with col2:
    st.markdown("### 📊 Analytics Insights")
    st.markdown("""
    Explore **sector-wise pricing**,  
    floor & area trends, amenities,  
    correlations & distributions.
    """)

with col3:
    st.markdown("### 🏘️ Property Recommender")
    st.markdown("""
    Get **similar apartment suggestions**  
    using content-based recommendation  
    techniques.
    """)

with col4:
    st.markdown("### 🧠 ML Powered")
    st.markdown("""
    Uses **feature engineering**,  
    regression models & similarity  
    metrics for intelligent outputs.
    """)

st.divider()

# ----------------------------------
# DATA & MODEL HIGHLIGHTS
# ----------------------------------
st.subheader("📌 Project Highlights")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Properties Analyzed", "3,142+")

with c2:
    st.metric("Avg Property Price", "₹0.95 Cr", "+5.2%")

with c3:
    st.metric("Avg Price / Sq Ft", "₹11,250", "+2.4%")

st.markdown("""
**Dataset Includes:**
- Property type, sector, price, area
- BHK, floor, age & furnishing
- Amenities & luxury score
- Latitude–longitude (geo analysis)
""")

st.divider()

# ----------------------------------
# HOW TO USE
# ----------------------------------
st.subheader("🧭 How to use this application")

st.markdown("""
1️⃣ **Price Prediction**  
→ Enter property details to estimate market price  

2️⃣ **Analytics Insights**  
→ Visualize trends, correlations & distributions  

3️⃣ **Recommender System**  
→ Find similar properties based on features  

Use the **sidebar** to switch between modules.
""")

st.info("👈 Use the sidebar to navigate between pages")

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.caption("📍 Project built for learning, analytics & ML demonstration")
