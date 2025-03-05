import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sub-division_population_of_pakistan.csv")
    return df

df = load_data()

# Ensure numeric data types for relevant columns
numeric_columns = [
    "ALL SEXES (RURAL)", "ALL SEXES (URBAN)", "MALE (RURAL)", "FEMALE (RURAL)",
    "MALE (URBAN)", "FEMALE (URBAN)", "ANNUAL GROWTH RATE (RURAL)", "TRANSGENDER (RURAL)", "AVG HOUSEHOLD SIZE (RURAL)"
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# Sidebar for navigation
st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #F2FAF1;
            padding: 20px;
            border-right: 2px solid #D4ECDD;
        }
        [data-testid="stSidebar"] h1 {
            color: #1D4D4F;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #2C3E50;
            font-size: 16px;
            font-weight: 500;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 12px;
            border-radius: 10px;
            background: #E6F4EA;
            color: #145A32;
            margin-bottom: 5px;
            font-weight: bold;
            transition: background 0.3s ease-in-out, transform 0.2s;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: #C8E6C9;
            transform: scale(1.02);
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
            background: #81C784;
            color: white;
            font-weight: bold;
        }
        [data-testid="stSidebar"] hr {
            border: 1px solid #A5D6A7;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.image("flag.png", width=200)
st.sidebar.title("📊 Pakistan Population Analysis")
st.sidebar.markdown("🌍 **Explore Census Insights with Interactive Charts!**")

page = st.sidebar.radio(
    "📌 **Select Page**",  # ✅ Proper label
    [
        "🏠 Home", "📈 Population Distribution", "👥 Gender Ratio Analysis",
        "🏙️ Division-wise Gender Ratio Analysis", "📊 Growth Rate Analysis", 
        "🌆 Urban vs Rural Comparison", "🌈 Transgender Population Analysis",
        "🏡 Division-wise Household Size Analysis", "🏠 Household Size Analysis",
        "📍 District-wise Insights", "📌 Division-wise Insights", "🗺️ Province-wise Insights"
    ],
    label_visibility="visible"  # ✅ Ensures label is displayed
)


st.sidebar.markdown("---")

# Global Chart Selection (Move Inside the Sidebar)
st.sidebar.markdown("📊 **Choose Chart Type**")
chart_type = st.sidebar.radio(
    "📊 **Choose Chart Type**", ["📊 Bar Chart", "🥧 Pie Chart"], index=0
)


# 🔹 Function to Display Charts
def display_chart(data, x_column, y_column, title, x_label, y_label, chart_type):
    if chart_type == "📊 Bar Chart":
        fig = px.bar(data, x=x_column, y=y_column, title=title, labels={x_column: x_label, y_column: y_label},
                     color_discrete_sequence=["#66BB6A"])  # Green
    elif chart_type == "🥧 Pie Chart":
        fig = px.pie(data, names=x_column, values=y_column, title=title,
                     color_discrete_sequence=px.colors.qualitative.Set3)
    elif chart_type == "📈 Line Chart":
        fig = px.line(data, x=x_column, y=y_column, title=title, labels={x_column: x_label, y_column: y_label},
                      color_discrete_sequence=["#FFA07A"])  # Light Salmon
    else:
        fig = px.scatter(data, x=x_column, y=y_column, title=title, labels={x_column: x_label, y_column: y_label},
                         color_discrete_sequence=["#FF7043"])  # Soft Orange
    st.plotly_chart(fig)
# Home Page
if page ==  "🏠 Home":
    st.title("📊 Welcome to the Pakistan Population Analysis")
    
    st.write("""
    Explore the 2017 Pakistan Population Census data, covering provinces, divisions, districts, 
    and sub-divisions. This dashboard provides insights into urban & rural populations, 
    gender distribution, growth rates, and more.
    """)

    # Calculate Total Population
    total_rural = df["ALL SEXES (RURAL)"].sum()
    total_urban = df["ALL SEXES (URBAN)"].sum()
    total_population = total_rural + total_urban

    # Display total population statistics
    st.markdown(f"""
    ### 🏡 Total Rural Population: **{total_rural:,.0f}**  
    ### 🏙️ Total Urban Population: **{total_urban:,.0f}**
    ### 🌍 Total Population: **{total_population:,.0f}**
    """)

    # Add a new section for Province-wise Total Population Pie Chart
    st.subheader("🌍 Province-wise Total Population Distribution")
    province_population = (
        df.groupby("PROVINCE")[["ALL SEXES (RURAL)", "ALL SEXES (URBAN)"]]
        .sum()
        .reset_index()
        .copy()  # ✅ Ensure a full copy
    )
    province_population.loc[:, "TOTAL POPULATION"] = (
        province_population["ALL SEXES (RURAL)"] + province_population["ALL SEXES (URBAN)"]
    )

    fig_province = px.pie(
        province_population,
        names="PROVINCE",
        values="TOTAL POPULATION",
        color_discrete_sequence=["green", "#4682B4", "#3CB371", "#FFA500", "#9370DB"],
        title="Total Population by Province"
    )
    st.plotly_chart(fig_province)

    # Create two columns to display pie charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌿 Rural Population Distribution")
        rural_population = df.groupby("PROVINCE")["ALL SEXES (RURAL)"].sum().reset_index().copy()
        fig_rural = px.pie(
            rural_population, 
            names="PROVINCE", 
            values="ALL SEXES (RURAL)", 
            color_discrete_sequence=["green", "#87CEFA", "#98FB98", "#FFDAB9", "#E6E6FA"],
            title="Rural Population by Province"
        )
        st.plotly_chart(fig_rural)

    with col2:
        st.subheader("🏢 Urban Population Distribution")
        urban_population = df.groupby("PROVINCE")["ALL SEXES (URBAN)"].sum().reset_index().copy()
        fig_urban = px.pie(
            urban_population, 
            names="PROVINCE", 
            values="ALL SEXES (URBAN)", 
            color_discrete_sequence=["green", "#87CEFA", "#98FB98", "#FFDAB9", "#E6E6FA"],
            title="Urban Population by Province"
        )
        st.plotly_chart(fig_urban)

# Population Distribution Page
elif page == "📈 Population Distribution":
    st.title("📈 Population Distribution")
    
    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="population_distribution_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Calculate total population (Rural + Urban) safely
    filtered_df.loc[:, "TOTAL POPULATION"] = filtered_df["ALL SEXES (RURAL)"] + filtered_df["ALL SEXES (URBAN)"]

    # ✅ Update chart to show TOTAL POPULATION instead of only RURAL
    display_chart(filtered_df, "DISTRICT", "TOTAL POPULATION", 
                  f"Population Distribution in {province}", 
                  "District", "Total Population", chart_type)

    # Calculate and display total population of the province
    total_population = filtered_df["TOTAL POPULATION"].sum()
    st.markdown(f"### 🌍 Total Population of {province}: **{total_population:,}**")

 
# Gender Ratio Analysis
elif page == "👥 Gender Ratio Analysis":
    st.title("Gender Ratio Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="gender_ratio_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # User selects Rural or Urban Population with a unique key
    area_type = st.selectbox("🏡 Select Area Type", ["Rural", "Urban"], index=0, key="gender_ratio_area")

    # User selects Gender Type with a unique key
    gender_option = st.selectbox("🧑‍🤝‍🧑 Select Gender", ["Male", "Female", "Comparison"], index=0, key="gender_ratio_gender")

    # Set column names based on selection
    if gender_option == "Male":
        gender_column = f"MALE ({area_type.upper()})"
        display_chart(filtered_df, "DISTRICT", gender_column, f"{area_type} Male Population in {province}",
                      "District", "Population", chart_type)
    
    elif gender_option == "Female":
        gender_column = f"FEMALE ({area_type.upper()})"
        display_chart(filtered_df, "DISTRICT", gender_column, f"{area_type} Female Population in {province}",
                      "District", "Population", chart_type)
    
    else:  # Comparison of Male and Female
        st.subheader(f"{area_type} Male vs Female Population in {province}")
        st.write("Comparison of Male and Female population side by side.")
        
        # Two charts: One for Male and one for Female
        col1, col2 = st.columns(2)
        with col1:
            display_chart(filtered_df, "DISTRICT", f"MALE ({area_type.upper()})",
                          f"{area_type} Male Population in {province}", "District", "Male Population", chart_type)
        with col2:
            display_chart(filtered_df, "DISTRICT", f"FEMALE ({area_type.upper()})",
                          f"{area_type} Female Population in {province}", "District", "Female Population", chart_type)

elif page == "🏙️ Division-wise Gender Ratio Analysis":
    st.title("Division-wise Gender Ratio Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="gender_ratio_province")

    # Filter dataset based on selected province
    province_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Select Division (filtered based on selected Province) with a unique key
    division = st.selectbox("🏙️ Select Division", province_df["DIVISION"].unique(), key="gender_ratio_division")

    # Filter dataset based on selected division
    division_df = province_df[province_df["DIVISION"] == division].copy()  # ✅ Create a new copy to avoid warnings

    # User selects Rural or Urban Population with a unique key
    area_type = st.selectbox("🏡 Select Area Type", ["Rural", "Urban"], index=0, key="gender_ratio_area")

    # User selects Gender Type with a unique key
    gender_option = st.selectbox("🧑‍🤝‍🧑 Select Gender", ["Male", "Female", "Comparison"], index=0, key="gender_ratio_gender")

    if gender_option == "Male":
        gender_column = f"MALE ({area_type.upper()})"
        display_chart(division_df, "DISTRICT", gender_column, f"{area_type} Male Population in {division}", "District", "Male Population", chart_type)

    elif gender_option == "Female":
        gender_column = f"FEMALE ({area_type.upper()})"
        display_chart(division_df, "DISTRICT", gender_column, f"{area_type} Female Population in {division}", "District", "Female Population", chart_type)

    else:  # Single Graph for Comparison
        st.subheader(f"{area_type} Male vs Female Population in {division}")

        # Create a new DataFrame for comparison
        comparison_df = division_df[["DISTRICT", f"MALE ({area_type.upper()})", f"FEMALE ({area_type.upper()})"]]
        comparison_df = comparison_df.melt(id_vars="DISTRICT", var_name="Gender", value_name="Population")

        # Create a grouped bar chart with a new color combination
        fig = px.bar(
            comparison_df,
            x="DISTRICT",
            y="Population",
            color="Gender",
            title=f"{area_type} Male vs Female Population in {division}",
            labels={"DISTRICT": "District", "Population": "Population"},
            barmode="group",  # Ensures bars for Male & Female are side by side
            color_discrete_map={
                "MALE (RURAL)": "#1f77b4",   # Deep Blue
                "FEMALE (RURAL)": "#ff7f0e", # Orange
                "MALE (URBAN)": "#2ca02c",   # Green
                "FEMALE (URBAN)": "#d62728"  # Red
            }  # Custom color scheme
        )

        st.plotly_chart(fig)


# Growth Rate Analysis Page
elif page == "📊 Growth Rate Analysis":
    st.title("Growth Rate Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="growth_rate_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # User selects whether to view Rural or Urban Growth Rate
    growth_type = st.radio("📈 Select Growth Rate Type", ["Rural", "Urban"], index=0)

    # Set column name based on selection
    growth_column = "ANNUAL GROWTH RATE (RURAL)" if growth_type == "Rural" else "ANNUAL GROWTH RATE (URBAN)"

    # Display graph with corrected function call
    display_chart(filtered_df, "DISTRICT", growth_column, 
                  f"{growth_type} Annual Growth Rate in {province}", "District", "Growth Rate (%)", chart_type)

# Urban vs Rural Comparison Page
elif page == "🌆 Urban vs Rural Comparison":
    st.title("Urban vs Rural Population Comparison")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="urban_rural_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Urban Population Graph (Top)
    st.subheader("Urban Population")
    display_chart(filtered_df, "DISTRICT", "ALL SEXES (URBAN)", 
                  f"Urban Population in {province}", "District", "Population", chart_type)

    # Rural Population Graph (Below)
    st.subheader("Rural Population")
    display_chart(filtered_df, "DISTRICT", "ALL SEXES (RURAL)", 
                  f"Rural Population in {province}", "District", "Population", chart_type)


# Transgender Population Analysis Page
elif page == "🌈 Transgender Population Analysis":
    st.title("Transgender Population Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="transgender_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Display Transgender Population Chart (Rural)
    display_chart(filtered_df, "DISTRICT", "TRANSGENDER (RURAL)", 
                  f"Transgender Population in {province} (Rural)", "District", "Population", chart_type)

    # Display Transgender Population Chart (Urban)
    display_chart(filtered_df, "DISTRICT", "TRANSGENDER (URBAN)", 
                  f"Transgender Population in {province} (Urban)", "District", "Population", chart_type)

# Household Size Analysis Page
elif page == "🏡 Division-wise Household Size Analysis":
    st.title("Division-wise Household Size Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="household_division_province")

    # Filter dataset based on selected province
    province_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Select Division (filtered based on Province) with a unique key
    division = st.selectbox("🏙️ Select Division", province_df["DIVISION"].unique(), key="household_division_selection")

    # Filter dataset based on selected division
    division_df = province_df[province_df["DIVISION"] == division].copy()  # ✅ Create a new copy to avoid warnings

    # Check if filtered data is empty
    if division_df.empty:
        st.warning("No data available for the selected division.")
    else:
        # Create two columns to display graphs side by side
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Rural Household Size")
            display_chart(division_df, "DISTRICT", "AVG HOUSEHOLD SIZE (RURAL)", 
                          f"Rural Household Size in {division}", "District", "Household Size", chart_type)

        with col2:
            st.subheader("Urban Household Size")
            display_chart(division_df, "DISTRICT", "AVG HOUSEHOLD SIZE (URBAN)", 
                          f"Urban Household Size in {division}", "District", "Household Size", chart_type)

elif page == "🏠 Household Size Analysis":
    st.title("Average Household Size Analysis")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="household_size_province")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy to avoid warnings

    # Create two columns to display graphs side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rural Household Size")
        display_chart(filtered_df, "DISTRICT", "AVG HOUSEHOLD SIZE (RURAL)", 
                      f"Rural Household Size in {province}", "District", "Household Size", chart_type)

    with col2:
        st.subheader("Urban Household Size")
        display_chart(filtered_df, "DISTRICT", "AVG HOUSEHOLD SIZE (URBAN)", 
                      f"Urban Household Size in {province}", "District", "Household Size", chart_type)

# District-wise Insights Page
elif page == "📍 District-wise Insights":
    st.title("District-wise Insights")

    # First, select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="district_insights_province")

    # Filter divisions based on selected province
    divisions = df[df["PROVINCE"] == province]["DIVISION"].unique()
    division = st.selectbox("📍 Select Division", divisions, key="district_insights_division")  # ✅ Unique key

    # Filter districts based on selected division
    districts = df[(df["PROVINCE"] == province) & (df["DIVISION"] == division)]["DISTRICT"].unique()
    district = st.selectbox("🏙️ Select District", districts, key="district_insights_district")  # ✅ Unique key

    # Filter data for selected district
    filtered_df = df[(df["PROVINCE"] == province) & (df["DIVISION"] == division) & (df["DISTRICT"] == district)].copy()  # ✅ Create a new copy

    # Creating a new column for total population (Rural + Urban) safely
    filtered_df.loc[:, "TOTAL POPULATION"] = filtered_df["ALL SEXES (RURAL)"] + filtered_df["ALL SEXES (URBAN)"]

    # Pass chart_type to display_chart function
    display_chart(filtered_df, "SUB DIVISION", "TOTAL POPULATION", 
                  f"Total Population in {district}, {division}, {province}", 
                  "Sub Division", "Total Population", chart_type)


# division wise
elif page == "📌 Division-wise Insights":
    st.title("Division-wise Insights")

    # First, select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="province_1")

    # Filter divisions based on selected province
    divisions = df[df["PROVINCE"] == province]["DIVISION"].unique()
    division = st.selectbox("📍 Select Division", divisions, key="division_insights")  # ✅ Unique key

    # Filter data for selected division
    filtered_df = df[(df["PROVINCE"] == province) & (df["DIVISION"] == division)].copy()  # ✅ Create a new copy

    # Creating a new column for total population (Rural + Urban) safely
    filtered_df.loc[:, "TOTAL POPULATION"] = filtered_df["ALL SEXES (RURAL)"] + filtered_df["ALL SEXES (URBAN)"]

    # Pass `chart_type` as an argument to display_chart()
    display_chart(filtered_df, "DISTRICT", "TOTAL POPULATION", f"Total Population in {division}, {province}", 
                  "District", "Total Population", chart_type)


# Province-wise Insights Page
elif page == "🗺️ Province-wise Insights":
    st.title("Province-wise Insights")

    # Select Province with a unique key to avoid duplicate widget warnings
    province = st.selectbox("🌍 Select Province", df["PROVINCE"].unique(), key="province_insights")

    # Filter dataset based on selected province
    filtered_df = df[df["PROVINCE"] == province].copy()  # ✅ Create a new copy

    # Creating a new column for total population (Rural + Urban) safely
    filtered_df.loc[:, "TOTAL POPULATION"] = filtered_df["ALL SEXES (RURAL)"] + filtered_df["ALL SEXES (URBAN)"]

    # Pass chart_type as an argument
    display_chart(filtered_df, "DIVISION", "TOTAL POPULATION", f"Total Population in {province}", 
                  "Division", "Total Population", chart_type)

