import streamlit as st
import pandas as pd
import json
import plotly.express as px
import ast
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Gurugram Real Estate Analytics",
    layout="wide"
)

st.title("🏙️ Gurugram  Real Estate Analytics")

# ----------------------------------
# SESSION STATE (WORDCLOUD ONLY)
# ----------------------------------
if "wc_sector" not in st.session_state:
    st.session_state.wc_sector = "All"

# ----------------------------------
# LOAD DATA 
# ----------------------------------
@st.cache_data
def load_data():
    sector_stats = pd.read_csv("dataset/sector_stats.csv")
    properties = pd.read_csv("dataset/gurgaon_properties.csv")
    main_df = pd.read_csv("dataset/new_latlong.csv")

    with open("dataset/gurugram_sectors_clean.geojson", "r") as f:
        geojson = json.load(f)

    return sector_stats, properties, main_df, geojson

sector_stats, feature_df, main_df, clean_geojson = load_data()

# ----------------------------------
# FLOOR RANGE BUCKETING
# ----------------------------------
def floor_bucket(x):
    if x <= 2:
        return "Ground–2"
    elif x <= 5:
        return "3–5"
    elif x <= 10:
        return "6–10"
    elif x <= 15:
        return "11–15"
    elif x <= 20:
        return "16–20"
    else:
        return "21+"

main_df["floor_range"] = main_df["floorNum"].apply(floor_bucket)

floor_order = ["Ground–2", "3–5", "6–10", "11–15", "16–20", "21+"]

floor_stats = (
    main_df
    .groupby("floor_range")
    .agg(
        count=("price", "count"),
        avg_price=("price", "mean")
    )
    .reset_index()
)

floor_stats["floor_range"] = pd.Categorical(
    floor_stats["floor_range"],
    categories=floor_order,
    ordered=True
)

floor_stats = floor_stats.sort_values("floor_range")
floor_stats["avg_price_cr"] = floor_stats["avg_price"].round(2)

# ----------------------------------
# BUILT-UP AREA BUCKETING
# ----------------------------------
def area_bucket(x):
    if x < 500:
        return "<500"
    elif x <= 1000:
        return "500–1000"
    elif x <= 1500:
        return "1000–1500"
    elif x <= 2000:
        return "1500–2000"
    elif x <= 2500:
        return "2000–2500"
    else:
        return "2500+"

main_df["area_range"] = main_df["built_up_area"].apply(area_bucket)

area_order = [
    "<500",
    "500–1000",
    "1000–1500",
    "1500–2000",
    "2000–2500",
    "2500+"
]

area_stats = (
    main_df
    .groupby("area_range")
    .agg(
        count=("price", "count"),
        avg_price=("price", "mean")
    )
    .reset_index()
)

area_stats["area_range"] = pd.Categorical(
    area_stats["area_range"],
    categories=area_order,
    ordered=True
)

area_stats = area_stats.sort_values("area_range")
area_stats["avg_price_cr"] = area_stats["avg_price"].round(2)

# ----------------------------------
# HEATMAP 
# ----------------------------------
# CORRELATION DATA 
# ----------------------------------
exclude_cols = [
    "price_per_sqft",
    "latitude",
    "longitude"
]

numeric_cols = (
    main_df
    .select_dtypes(include=["int64", "float64"])
    .drop(columns=exclude_cols, errors="ignore")
)

corr_matrix = numeric_cols.corr().round(2)

# ----------------------------------
# BHK DISTRIBUTION DATA
# ----------------------------------
bhk_df = (
    main_df["bedRoom"]
    .value_counts()
    .sort_index()
    .reset_index()
)

bhk_df.columns = ["BHK", "Count"]
bhk_df["BHK"] = bhk_df["BHK"].astype(str) + " BHK"

# ----------------------------------
# FURNISHING DISTRIBUTION DATA
# ----------------------------------
furnishing_map = {
    0: "Unfurnished",
    1: "Semi-Furnished",
    2: "Fully Furnished"
}

furn_df = (
    main_df["furnishing_type"]
    .map(furnishing_map)
    .value_counts()
    .reset_index()
)

furn_df.columns = ["Furnishing Type", "Count"]

# ----------------------------------
# AGE / POSSESSION DISTRIBUTION
# ----------------------------------
age_df = (
    main_df["agePossession"]
    .value_counts()
    .reset_index()
)

age_df.columns = ["Age / Possession", "Count"]

# ----------------------------------
# BALCONY DISTRIBUTION
# ----------------------------------
balcony_df = (
    main_df["balcony"]
    .fillna("No Balcony")
    .replace({
        "0": "No Balcony",
        "1": "Balcony",
        0: "No Balcony",
        1: "Balcony"
    })
    .value_counts()
    .reset_index()
)

balcony_df.columns = ["Balcony Status", "Count"]

# ----------------------------------
# WORDCLOUD DATA PREP
# ----------------------------------
feature_sector_df = feature_df.merge(
    main_df[["sector"]],
    left_index=True,
    right_index=True
)[["features", "sector"]]

sector_list = ["All"] + sorted(feature_sector_df["sector"].unique())

st.subheader("🗺️ Sector-wise Price per Sqft Map")

fig = px.choropleth_map(
        sector_stats,
        geojson=clean_geojson,
        locations="sector",
        featureidkey="properties.sector",
        color="avg_price_per_sqft",             
        color_continuous_scale="Viridis",
        map_style="open-street-map",
        zoom=11,
        center={"lat": 28.4595, "lon": 77.0266},
        opacity=0.75,
        hover_name="sector",
        hover_data={
            "avg_price": ':.2f',
            "avg_price_per_sqft": ':.0f',
            "avg_area": ':.0f',
            "listings": True
        },
        title="Gurugram Sector-wise Average Price per Sqft"
    )

fig.update_layout(
        height=700,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

fig.update_traces(marker_line_width=1, marker_line_color="black")
st.plotly_chart(fig, use_container_width=True)
# ----------------------------------
# LAYOUT (TWO COLUMNS)
# ----------------------------------
col1, col2 = st.columns(2)

# ==================================
# LEFT COLUMN → MAP (FIXED METRIC)
# ==================================
with col1:
    st.subheader("🧭 Amenities Availability")

    amenity_cols = [
        "study room",
        "servant room",
        "store room",
        "pooja room",
        "others"
    ]

    amenity_stats = (
        main_df[amenity_cols]
        .mean()
        .mul(100)
        .round(1)
    )

    categories = amenity_stats.index.tolist()
    values = amenity_stats.values.tolist()

    categories += [categories[0]]
    values += [values[0]]

    max_val = max(values)

    fig_radar = go.Figure()

    fig_radar.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line=dict(color="#2E86C1", width=3),
            fillcolor="rgba(46,134,193,0.35)"
        )
    )

    fig_radar.update_layout(
        polar=dict(
            gridshape="linear",
            radialaxis=dict(
                range=[0, max_val * 1.2],
                showticklabels=True
            )
        ),
        height=650,
        margin=dict(t=30, b=30, l=30, r=30),
        showlegend=False
    )

    st.plotly_chart(fig_radar, use_container_width=True)


with col2:
    st.subheader("☁️ Sector-wise Feature WordCloud")

    wc_sector = st.selectbox(
        "Select Sector (WordCloud Only)",
        sector_list,
        index=sector_list.index(st.session_state.wc_sector),
        key="wc_sector_select"
    )

    st.session_state.wc_sector = wc_sector

    if st.session_state.wc_sector == "All":
        wc_df = feature_sector_df
    else:
        wc_df = feature_sector_df[
            feature_sector_df["sector"] == st.session_state.wc_sector
        ]

    words = []
    for item in wc_df["features"].dropna().apply(ast.literal_eval):
        words.extend(item)

    feature_text = " ".join(words)

    if feature_text.strip():
        plt.rcParams["font.family"] = "Arial"

        wordcloud = WordCloud(
            width=800,
            height=650,
            background_color="white",
            stopwords={"s"},
            min_font_size=10
        ).generate(feature_text)

        fig_wc, ax = plt.subplots(figsize=(7,7))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig_wc, use_container_width=True)
    else:
        st.info("No feature data available for this sector.")

st.markdown("---")

col_built, col_floor = st.columns(2)

with col_built:
    st.subheader("📊 Price by Built-up Area Range")

    fig_area = go.Figure()

    # Histogram → COUNT
    fig_area.add_bar(
        x=area_stats["area_range"],
        y=area_stats["count"],
        name="Property Count",
        marker_color="#D6EAF8",
        yaxis="y"
    )

    # Step line → AVG PRICE
    fig_area.add_scatter(
        x=area_stats["area_range"],
        y=area_stats["avg_price_cr"],
        name="Avg Price (Cr)",
        mode="lines+markers+text",
        text=area_stats["avg_price_cr"],
        textposition="top center",
        line=dict(
            color="#1F618D",
            width=3,
            shape="hv"
        ),
        marker=dict(size=8),
        yaxis="y2"
    )

    fig_area.update_layout(
        height=450,
        xaxis_title="Built-up Area Range (sqft)",
        yaxis=dict(title="Property Count", showgrid=False),
        yaxis2=dict(
            title="Average Price (Cr)",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[
                area_stats["avg_price_cr"].min() * 0.9,
                area_stats["avg_price_cr"].max() * 1.1
            ]
        ),
        legend=dict(
            orientation="h",
            y=1.15,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(t=40, b=40, l=40, r=40)
    )

    st.plotly_chart(fig_area, use_container_width=True)

with col_floor:
    st.subheader("📊 Price Analysis by Floor Range")

    fig_floor = go.Figure()

    # Bars → Count
    fig_floor.add_bar(
        x=floor_stats["floor_range"],
        y=floor_stats["count"],
        name="Property Count",
        marker_color="#AED6F1",
        yaxis="y"
    )

    # Line → Avg Price (Cr)
    fig_floor.add_scatter(
    x=floor_stats["floor_range"],
    y=floor_stats["avg_price_cr"],
    name="Avg Price (Cr)",
    mode="lines+markers+text",
    text=floor_stats["avg_price_cr"],
    textposition="top center",
    line=dict(
        color="#CB4335",
        width=3,
        shape="hv"  
    ),
    marker=dict(size=8),
    yaxis="y2"
)


    fig_floor.update_layout(
        height=450,
        xaxis_title="Floor Range",
        yaxis=dict(
            title="Property Count",
            showgrid=False
        ),
        yaxis2=dict(
            title="Average Price (Cr)",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[
                floor_stats["avg_price_cr"].min() * 0.9,
                floor_stats["avg_price_cr"].max() * 1.1
            ]
        ),
        legend=dict(
            orientation="h",
            y=1.15,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(t=40, b=40, l=40, r=40)
    )

    st.plotly_chart(fig_floor, use_container_width=True)

st.markdown("---")

st.subheader("🔥 Feature Correlation Heatmap")

fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1
    )

fig_corr.update_layout(
        height=1000,
        xaxis_title="Features",
        yaxis_title="Features",
        margin=dict(t=40, b=40, l=40, r=40)
    )

st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

col_bhk, col_furn = st.columns(2)
with col_bhk:
    st.subheader("🏠 Property Distribution by BHK")

    fig_bhk = px.pie(
        bhk_df,
        names="BHK",
        values="Count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig_bhk.update_traces(
        textinfo="percent+label",
        textfont_size=14
    )

    fig_bhk.update_layout(
        height=450,
        margin=dict(t=40, b=40, l=40, r=40),
        legend_title_text="Bedroom Type"
    )

    st.plotly_chart(fig_bhk, use_container_width=True)

with col_furn:
    st.subheader("🛋️ Furnishing Type Distribution")

    fig_furn = px.pie(
        furn_df,
        names="Furnishing Type",
        values="Count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_furn.update_traces(
        textinfo="percent+label",
        textfont_size=14
    )

    fig_furn.update_layout(
        height=450,
        margin=dict(t=40, b=40, l=40, r=40),
        legend_title_text="Furnishing Status"
    )

    st.plotly_chart(fig_furn, use_container_width=True)

st.markdown("---")

col_age, col_balcony = st.columns(2)
with col_age:
    st.subheader("⏳ Property Age / Possession")

    fig_age = px.pie(
        age_df,
        names="Age / Possession",
        values="Count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_age.update_traces(
        textinfo="percent+label",
        textfont_size=14
    )

    fig_age.update_layout(
        height=450,
        margin=dict(t=40, b=40, l=40, r=40),
        legend_title_text="Status"
    )

    st.plotly_chart(fig_age, use_container_width=True)

with col_balcony:
    st.subheader("🌤️ Balcony Availability")

    fig_balcony = px.pie(
        balcony_df,
        names="Balcony Status",
        values="Count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel1
    )

    fig_balcony.update_traces(
        textinfo="percent+label",
        textfont_size=14
    )

    fig_balcony.update_layout(
        height=450,
        margin=dict(t=40, b=40, l=40, r=40),
        legend_title_text="Balcony"
    )

    st.plotly_chart(fig_balcony, use_container_width=True)
