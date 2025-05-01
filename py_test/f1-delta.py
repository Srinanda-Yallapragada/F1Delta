import streamlit as st
import fastf1
import fastf1.plotting #this is needed
import pandas as pd


from quali import *
from race import *
from overview import *


# for interactive plots
fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme="None"
)


# make sure that the folder 'fastf1_cache' exsits
fastf1.Cache.enable_cache("fastf1_cache")

st.set_page_config(page_title="F1 Delta", layout="wide")


# markdown style description for the classes and font sizes

st.markdown(
    """
    <style>
    .stat-value { font-size: 40px; font-weight: bold; display: block; text-align: center;}
    .stat-label { font-size: 30px; color: grey; display: block; text-align: center;}
    .regular { font-size: 25px; }
    .medium { font-size: 30px; }
    .large { font-size: 40px; }
    .header { font-size: 50px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title("F1 Delta")
st.sidebar.markdown(
    "<span class='regular'>The goal of this project is to explore how driving styles have changed given that 2025 had a lot of driver changes. We can explore this data based on throttle application, driving line taken and more</span>",
    unsafe_allow_html=True,
)
st.sidebar.header("Select Driver and Session")


events_2025 = get_completed_events_2025()
events_2024 = get_completed_events_2024()


# Default values
if "track" not in st.session_state:
    st.session_state["track"] = events_2025[0]
if "driver" not in st.session_state:
    st.session_state["driver"] = driver_names[0]


def simple_plot():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    fig = px.scatter(
        df,
        x="x",
        y="y",
        labels={"x": "Simple X Axis", "y": "Simple Y Axis"},
        title="Simple Plot with Hover",
    )
    return fig


def refresh_views():
    track = st.session_state.get("track")
    driver = st.session_state.get("driver")
    abbreviation = get_driver_abbreviation_by_name(driver)

    print(f"Selected Track in refresh_views: {track}")
    print(f"Selected Driver in refresh_views: {driver} ({abbreviation})")

    # # simple_plot()
    # st.plotly_chart(simple_plot())

    display_driver_overview(track, driver, abbreviation)
    qualifying_comparision_view(track, driver, abbreviation)
    rpm_vs_distance_fastest_lap_view(track, driver, abbreviation)
    fastest_qualifying_lap_speed_view(track, driver, abbreviation)
    position_comparision_view(track, driver, abbreviation)


# on change watchers
selected_track_name = st.sidebar.selectbox(
    "Select Track", events_2025, key="track", on_change=refresh_views
)

# Add driver selector to sidebar
selected_driver_name = st.sidebar.selectbox(
    "Select Driver", driver_names, key="driver", on_change=refresh_views
)
