import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import fastf1
import pandas as pd
from datetime import datetime


# make sure that the folder 'fastf1_cache' exsits
fastf1.Cache.enable_cache("fastf1_cache")

st.set_page_config(page_title="F1 Delta")

st.sidebar.title("F1 Delta")
st.sidebar.text(
    "  The goal of this project is to explore how driving styles have changed given that 2025 had a lot of driver changes. We can explore this data based on throttle application, driving line taken and more "
)
st.sidebar.header("Select Driver and Session")


# Function to get completed events only from 2025
@st.cache_data
def get_completed_events_2025():
    # Get the full schedule for 2025
    schedule = fastf1.get_event_schedule(2025)
    current_date = datetime.now().date()

    completed_events = []
    for _, event in schedule.iterrows():
        if (
            pd.notna(event["Session5Date"])
            and event["Session5Date"].date() < current_date
        ):
            completed_events.append(event["EventName"])
    return completed_events


# Function to get completed events from 2024
@st.cache_data
def get_completed_events_2024():
    schedule = fastf1.get_event_schedule(2024)

    completed_events = []
    for _, event in schedule.iterrows():
        # Assuming all 2024 races are completed for comparison
        completed_events.append(event["EventName"])
    return completed_events


events_2025 = get_completed_events_2025()
events_2024 = get_completed_events_2024()


# This was done by hand using https://www.statsf1.com/ #TODO update these
driver_stats = [
    {
        "number": 1,
        "name": "Max Verstappen",
        "abbreviation": "VER",
        "wins": 64,
        "poles": 41,
        "podiums": 114,
        "championships": 4,
    },
    {
        "number": 4,
        "name": "Lando Norris",
        "abbreviation": "NOR",
        "wins": 5,
        "poles": 10,
        "podiums": 29,
        "championships": 0,
    },
    {
        "number": 10,
        "name": "Pierre Gasly",
        "abbreviation": "GAS",
        "wins": 1,
        "poles": 0,
        "podiums": 5,
        "championships": 0,
    },
    {
        "number": 14,
        "name": "Fernando Alonso",
        "abbreviation": "ALO",
        "wins": 32,
        "poles": 22,
        "podiums": 106,
        "championships": 2,
    },
    {
        "number": 16,
        "name": "Charles Leclerc",
        "abbreviation": "LEC",
        "wins": 8,
        "poles": 26,
        "podiums": 43,
        "championships": 0,
    },
    {
        "number": 18,
        "name": "Lance Stroll",
        "abbreviation": "STR",
        "wins": 0,
        "poles": 1,
        "podiums": 3,
        "championships": 0,
    },
    {
        "number": 22,
        "name": "Yuki Tsunoda",
        "abbreviation": "TSU",
        "wins": 0,
        "poles": 0,
        "podiums": 0,
        "championships": 0,
    },
    {
        "number": 23,
        "name": "Alexander Albon",
        "abbreviation": "ALB",
        "wins": 0,
        "poles": 0,
        "podiums": 2,
        "championships": 0,
    },
    {
        "number": 27,
        "name": "Nico Hülkenberg",
        "abbreviation": "HUL",
        "wins": 0,
        "poles": 1,
        "podiums": 0,
        "championships": 0,
    },
    {
        "number": 31,
        "name": "Esteban Ocon",
        "abbreviation": "OCO",
        "wins": 1,
        "poles": 0,
        "podiums": 4,
        "championships": 0,
    },
    {
        "number": 44,
        "name": "Lewis Hamilton",
        "abbreviation": "HAM",
        "wins": 105,
        "poles": 104,
        "podiums": 202,
        "championships": 7,
    },
    {
        "number": 55,
        "name": "Carlos Sainz",
        "abbreviation": "SAI",
        "wins": 4,
        "poles": 6,
        "podiums": 27,
        "championships": 0,
    },
    {
        "number": 63,
        "name": "George Russell",
        "abbreviation": "RUS",
        "wins": 3,
        "poles": 5,
        "podiums": 17,
        "championships": 0,
    },
    {
        "number": 81,
        "name": "Oscar Piastri",
        "abbreviation": "PIA",
        "wins": 3,
        "poles": 2,
        "podiums": 12,
        "championships": 0,
    },
]
# Extract just the names for the selectbox
driver_names = [driver["name"] for driver in driver_stats]

# Default values (optional, but good practice)
if "track" not in st.session_state:
    st.session_state["track"] = events_2025[0]
if "driver" not in st.session_state:
    st.session_state["driver"] = driver_names[0]


def get_driver_abbreviation_by_name(name):
    for driver in driver_stats:
        if driver["name"] == name:
            return driver["abbreviation"]


def position_comparision_view(track, driver, abbreviation):
    st.subheader(f"Race Finishing Position Comparison: {driver} at {track}")
    race_session_2025 = fastf1.get_session(2025, track, "R")
    race_session_2025.load()
    race_results_2025 = race_session_2025.results
    driver_result_2025 = race_results_2025[
        race_results_2025["Abbreviation"] == abbreviation
    ].iloc[0]
    team_color_2025 = "#" + driver_result_2025["TeamColor"]
    pos_2025 = int(driver_result_2025["Position"])

    race_session_2024 = fastf1.get_session(2024, track, "R")
    race_session_2024.load()
    race_results_2024 = race_session_2024.results
    driver_result_2024 = race_results_2024[
        race_results_2024["Abbreviation"] == abbreviation
    ].iloc[0]
    team_color_2024 = "#" + driver_result_2024["TeamColor"]
    pos_2024 = int(driver_result_2024["Position"])

    if pos_2024 < pos_2025:
        color_2024 = (
            f'<span style="font-size:20px; color:{team_color_2024}">{pos_2024}</span>'
        )
        color_2025 = f'<span style="font-size:20px;">{pos_2025}</span>'
        comparison_sign = "<"
        performance_text = (
            f"{driver} performed better in {track} in 2024 compared to 2025."
        )
    elif pos_2024 > pos_2025:
        color_2024 = f'<span style="font-size:20px;">{pos_2024}</span>'
        color_2025 = (
            f'<span style="font-size:20px; color:{team_color_2025}">{pos_2025}</span>'
        )
        comparison_sign = ">"
        performance_text = (
            f"{driver} performed better in {track} in 2025 compared to 2024."
        )
    else:
        color_2024 = (
            f'<span style="font-size:20px; color:{team_color_2024}">{pos_2024}</span>'
        )
        color_2025 = (
            f'<span style="font-size:20px; color:{team_color_2025}">{pos_2025}</span>'
        )
        comparison_sign = "="
        performance_text = f"{driver}'s finishing position in {track} was the same in both 2024 and 2025."

    st.markdown(
        f"In 2024, {driver} finished {color_2024}. In 2025, they finished {color_2025}. "
        f"Overall, the comparison is: {color_2024} {comparison_sign} {color_2025}.",
        unsafe_allow_html=True,
    )
    st.write(performance_text)


def refresh_views():
    track = st.session_state.get("track")
    driver = st.session_state.get("driver")
    abbreviation = get_driver_abbreviation_by_name(driver)

    print(f"Selected Track in refresh_views: {track}")
    print(f"Selected Driver in refresh_views: {driver} ({abbreviation})")

    position_comparision_view(track,driver,abbreviation)

# on change watchers
selected_track_name = st.sidebar.selectbox(
    "Select Track", events_2025, key="track", on_change=refresh_views
)

# Add driver selector to sidebar
selected_driver_name = st.sidebar.selectbox(
    "Select Driver", driver_names, key="driver", on_change=refresh_views
)
