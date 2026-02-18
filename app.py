import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Global Military Power",
    layout="wide"
)

# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------
data = {
    "Country": ["United States", "Russia", "China", "India", "South Korea"],
    "PowerIndex": [0.071, 0.072, 0.073, 0.102, 0.150],
    "MilitaryBudget": [877, 86, 292, 81, 46],
    "GDP": [25.4, 2.2, 17.9, 3.7, 1.8],
    "Personnel": [1400000, 850000, 2000000, 1450000, 555000],
    "Region": ["North America", "Europe", "Asia", "Asia", "Asia"],
    "Continent": ["North America", "Europe", "Asia", "Asia", "Asia"],
    "Alliance": ["NATO", "None", "None", "None", "US Ally"]
}

df = pd.DataFrame(data)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""<style>
.block-container {
    padding-top: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.header-container {
    background-color: #bfbfbf;
    padding: 22px;
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 6px;

}
[data-testid="stSidebar"] {
    background-color: #a6a6a6;
    padding:40px;
}
.kpi-card {
    background-color: #9e9e9e;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    margin: 5px;
    border-radius: 6px;
}
.insights-box {
    background-color: #b3b3b3;
    padding: 35px;
    margin-top: 10px;
    border-radius: 25px;
    text-align: center;
    font-size: 28px;
    font-weight: 800;
}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

page = st.sidebar.radio(
    "",
    ["Quick Stats", "Nation Overview", "Compare Powers", "Coalition Builder"]
)

# ---------------------------------------------------
# QUICK STATS
# ---------------------------------------------------
if page == "Quick Stats":

    st.markdown(
        "<div class='header-container'> <span style='position: relative; top:20px;'> Global Military Power Dashboard </span></div>",
        unsafe_allow_html=True
    )

    # Filters
    f1, f2, f3 = st.columns(3)

    with f1:
        region_filter = st.selectbox("Region", df["Region"].unique())
    with f2:
        continent_filter = st.selectbox("Continent", df["Continent"].unique())
    with f3:
        alliance_filter = st.selectbox("Alliance", df["Alliance"].unique())

    filtered_df = df[
        (df["Region"] == region_filter) &
        (df["Continent"] == continent_filter) &
        (df["Alliance"] == alliance_filter)
    ]

    # KPI ROW
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"<div class='kpi-card'>KPI 1<br>{len(filtered_df)}</div>", unsafe_allow_html=True)
    with k2:
        value = filtered_df["PowerIndex"].mean() if not filtered_df.empty else 0
        st.markdown(f"<div class='kpi-card'>KPI 2<br>{value:.3f}</div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-card'>KPI 3<br>{filtered_df['MilitaryBudget'].sum()}</div>", unsafe_allow_html=True)
    with k4:
        value = filtered_df["GDP"].mean() if not filtered_df.empty else 0
        st.markdown(f"<div class='kpi-card'>KPI 4<br>{value:.2f}</div>", unsafe_allow_html=True)
    with k5:
        st.markdown(f"<div class='kpi-card'>KPI 5<br>{filtered_df['Personnel'].sum()}</div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown("### Military Rank by Country")

        fig_map = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode="country names",
            color="PowerIndex",
            color_continuous_scale="Reds",
            height=400
        )

        # REMOVE POWER INDEX COLOR SCALE
        fig_map.update_layout(
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("<div class='insights-box'>INSIGHTS</div>", unsafe_allow_html=True)

    with right:
        st.markdown("### Top 5 countries by power index")

        top5 = df.nsmallest(5, "PowerIndex")

        fig_bar = px.bar(
            top5,
            x="PowerIndex",
            y="Country",
            orientation="h",
            color_discrete_sequence=["#4d4d4d"],
            height=260
        )

        fig_bar.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(autorange="reversed"),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("### GDP Vs Military Budget")

        fig_bubble = px.scatter(
            filtered_df,
            x="GDP",
            y="MilitaryBudget",
            size="Personnel",
            color="PowerIndex",
            height=200
        )

        fig_bubble.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_bubble, use_container_width=True)

# ---------------------------------------------------
# OTHER PAGES
# ---------------------------------------------------
elif page == "Nation Overview":
    st.markdown("<div class='header-container'>Nation Overview</div>", unsafe_allow_html=True)
    st.write("Content for Nation Overview page.")

elif page == "Compare Powers":
    st.markdown("<div class='header-container'>Compare Powers</div>", unsafe_allow_html=True)
    st.write("Content for Compare Powers page.")

elif page == "Coalition Builder":
    st.markdown("<div class='header-container'>Coalition Builder</div>", unsafe_allow_html=True)
    st.write("Content for Coalition Builder page.")
