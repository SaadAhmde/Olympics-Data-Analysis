from unittest import result

import streamlit as st
import pandas as pd
import  plotly.express as px
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Olympics Analysis",
    page_icon="🏅",
    layout="wide"
)


# ---------------- Load datasets ----------------

# @st.cache_data
def load_data():
    dataframe = pd.read_csv(
        r"C:\Users\HAJI LAPTOP g55\Desktop\Un\athlete_events.csv"
    )
    region_dataframe = pd.read_csv(
        r"C:\Users\HAJI LAPTOP g55\Desktop\Un\noc_regions.csv"
    )
    return preprocessor.preprocess(dataframe, region_dataframe)


dataframe = load_data()


# ---------------- Title ----------------

st.sidebar.title("🏟️ Olympics Analysis")
st.title("🏅 Olympics Data Analysis")


# ---------------- Sidebar ----------------

user_menu = st.sidebar.radio(
    "Choose an option",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete-wise Analysis"
    )
)


# ---------------- Medal Tally ----------------

if user_menu == "Medal Tally":

    st.sidebar.header("🏅 Medal Tally")

    year, country = helper.country_year_list(dataframe)

    selected_year = st.sidebar.selectbox(
        "Select Year",
        year
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        country
    )

    medal_tally = helper.fetch_medal_tally(
        dataframe,
        selected_year,
        selected_country
    )

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("📊 Overall Analysis")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title(f"🏅 Medal Tally in - {selected_year} Olympics")
    elif selected_year == "Overall" and selected_country != "Overall":
        st.title(f"🌍 {selected_country} - Overall Performance")
    elif selected_year != "Overall" and selected_country != "Overall":
        st.title(f"🏆 {selected_country} - {selected_year} Overall Performance")

    st.dataframe(
        medal_tally,
        use_container_width=True
    )

    # Year-by-year breakdown, only when a specific country is selected
    if selected_country != "Overall":
        st.subheader(f"📆 {selected_country} — Medal Count by Year")
        year_wise_df = helper.year_wise_medal_tally(dataframe, selected_country)
        st.dataframe(year_wise_df, use_container_width=True)


# ---------------- Overall Analysis ----------------

elif user_menu == "Overall Analysis":

    st.header("📊 Overall Analysis")

    # ---------------- Statistics ----------------

    editions = dataframe["Year"].nunique()
    cities = dataframe["City"].nunique()
    sports = dataframe["Sport"].nunique()
    athletes = dataframe["Name"].nunique()
    nations = dataframe["region"].nunique()
    events = dataframe["Event"].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athletes)


    # ==================================================
    # Participating Nations Over Time
    # ==================================================

    st.title("🌍 Participating Nations Over the Years")

    nation_over_time = helper.nation_over_time(dataframe)

    import plotly.express as px

    fig1 = px.line(
        nation_over_time,
        x="Year",
        y="Nations",
        markers=True,
        # title="🌍 Participating Nations Over the Years"
    )

    fig1.update_layout(
        xaxis_title="Olympic Year",
        yaxis_title="Number of Nations",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # ==================================================
    # Events Over Time
    # ==================================================


    st.title("🏅 Number of Olympic Events Over the Years")

    events_over_time = (
        dataframe
        .drop_duplicates(["Year", "Event"])
        ["Year"]
        .value_counts()
        .reset_index(name="Events")
        .sort_values("Year")
    )

    fig2 = px.line(
        events_over_time,
        x="Year",
        y="Events",
        markers=True,
        # title=" Number of Olympic Events Over the Years"
    )

    fig2.update_layout(
        xaxis_title="Olympic Year",
        yaxis_title="Number of Events",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )
    # ==================================================
    # Athlete Over Time
    # ==================================================

    st.title("🏃 Number of Athletes Over the Years")

    athlete_over_time = (
        dataframe
        .drop_duplicates(["Year", "Name"])
        ["Year"]
        .value_counts()
        .reset_index(name="Athletes")
        .sort_values("Year")
    )

    fig3 = px.line(
        athlete_over_time,
        x="Year",
        y="Athletes",
        markers=True,
        # title=" Number of Athletes Over the Years"
    )

    fig3.update_layout(
        xaxis_title="Olympic Year",
        yaxis_title="Number of Athletes",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
#=====================================
    # Number of Events Over Time — Every Sport
#=============================================
    st.title("🏅 Number of Events Over Time — Every Sport")

    x = dataframe.drop_duplicates(
        ["Year", "Sport", "Event"]
    )

    heatmap_data = (
        x.pivot_table(
            index="Sport",
            columns="Year",
            values="Event",
            aggfunc="count"
        )
        .fillna(0)
        .astype(int)
    )

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        # title="Number of Events by Sport and Olympic Year",
        labels={
            "x": "Olympic Year",
            "y": "Sport",
            "color": "Number of Events"
        }
    )

    fig.update_layout(
        height=900,
        xaxis_title="Olympic Year",
        yaxis_title="Sport"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.title("🏆 Most Successful Athletes")

    sport_list = dataframe["Sport"].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox(
        "Select a Sport",
        sport_list
    )

    result = helper.most_success(
        dataframe,
        selected_sport
    )

    st.dataframe(
        result,
        use_container_width=True
    )

# ---------------- Country-wise Analysis ----------------

elif user_menu == "Country-wise Analysis":

    st.header("🌍 Country-wise Analysis")
    country_list = dataframe["region"].dropna().unique().tolist()

    selected_country = st.sidebar.selectbox(
        "Select Country",
        country_list
    )

    result = helper.country_medal_tally(
        dataframe,
        selected_country
    )

    st.dataframe(result)
    # heap map
    st.title(f"Best Performance for {selected_country}")

    fig = helper.country_wise_event_tally(
        dataframe,
        selected_country
    )

    st.pyplot(fig)

    # Top 10 athelets
    st.title(f"Top 10 Successful Athletes from {selected_country}")

    result = helper.top_10_success_athletes(
        dataframe,
        selected_country
    )

    st.table(result)


# ---------------- Athlete-wise Analysis ----------------

elif user_menu == "Athlete-wise Analysis":

    st.header("🏃 Athlete-wise Analysis")
    # data frame
    athlete_dataframe = dataframe.drop_duplicates(subset=["Name", "region"])

    # Create a copy of the dataframe
    df = athlete_dataframe.copy()

    # Overall athletes
    overall = df[["Age"]].dropna().assign(Category="Overall Age")

    # Gold medalists
    gold = df[df["Medal"] == "Gold"][["Age"]].dropna().assign(
        Category="Gold Medalist"
    )

    # Silver medalists
    silver = df[df["Medal"] == "Silver"][["Age"]].dropna().assign(
        Category="Silver Medalist"
    )

    # Bronze medalists
    bronze = df[df["Medal"] == "Bronze"][["Age"]].dropna().assign(
        Category="Bronze Medalist"
    )

    # Combine all data
    age_data = pd.concat([overall, gold, silver, bronze])

    # Create histogram
    fig = px.histogram(
        age_data,
        x="Age",
        color="Category",
        marginal="rug",
        barmode="overlay",
        nbins=30,
        title="Age Distribution of Athletes and Medalists"
    )

    st.plotly_chart(fig)

    medal_df = athlete_dataframe.dropna(subset=["Age", "Medal"]).copy()

    # Create age groups
    medal_df["Age Group"] = pd.cut(
        medal_df["Age"],
        bins=[0, 15, 20, 25, 30, 35, 40, 100],
        labels=[
            "Under 16",
            "16-20",
            "21-25",
            "26-30",
            "31-35",
            "36-40",
            "41+"
        ]
    )

    # Count medals in each age group
    age_group_counts = (
        medal_df["Age Group"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_group_counts.columns = ["Age Group", "Medals"]

    # Plot
    fig1 = px.bar(
        age_group_counts,
        x="Age Group",
        y="Medals",
        title="Medal Records by Age Group",
        text="Medals"
    )

    st.plotly_chart(fig1)

    sport_age = (
        athlete_dataframe
        .dropna(subset=["Age", "Sport"])
        .groupby("Sport")["Age"]
        .agg(["mean", "min", "max", "count"])
        .reset_index()
    )

    sport_age.columns = [
        "Sport",
        "Average Age",
        "Youngest Age",
        "Oldest Age",
        "Athlete Records"
    ]

    # Show sports with at least 100 athlete records
    sport_age = sport_age[sport_age["Athlete Records"] >= 100]

    sport_age = sport_age.sort_values(
        "Average Age",
        ascending=False
    )

    fig2 = px.bar(
        sport_age,
        x="Average Age",
        y="Sport",
        orientation="h",
        title="Average Athlete Age by Sport",
        hover_data=[
            "Youngest Age",
            "Oldest Age",
            "Athlete Records"
        ]
    )

    st.plotly_chart(fig2)

    overall = athlete_dataframe[["Age"]].dropna().copy()
    overall["Category"] = "Overall Athletes"

    medalists = athlete_dataframe[
        athlete_dataframe["Medal"].notna()
    ][["Age"]].dropna().copy()

    medalists["Category"] = "Medalists"

    age_comparison = pd.concat([overall, medalists])

    fig3 = px.box(
        age_comparison,
        x="Category",
        y="Age",
        color="Category",
        points=False,
        title="Age Comparison: Overall Athletes vs Medalists"
    )

    st.plotly_chart(fig3)

    import plotly.express as px

    average_age, age_groups = helper.age_analysis(dataframe)

    st.subheader("Average Age by Medal")

    fig1 = px.bar(
        average_age,
        x="Medal",
        y="Age",
        color="Medal",
        title="Average Age of Medalists"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Medals by Age Group")

    fig2 = px.bar(
        age_groups,
        x="Age Group",
        y="Medals",
        title="Medal Records by Age Group"
    )

    st.plotly_chart(fig2, use_container_width=True)