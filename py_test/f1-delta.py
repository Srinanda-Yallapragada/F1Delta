import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt, mpld3  # use st.pyplot for interactivity
from mpld3 import fig_to_html, plugins
import fastf1
import fastf1.plotting
import pandas as pd
from datetime import datetime
import numpy as np


# for interactive plots
fastf1.plotting.setup_mpl(
    mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme=None
)


# make sure that the folder 'fastf1_cache' exsits
fastf1.Cache.enable_cache("fastf1_cache")

st.set_page_config(page_title="F1 Delta", layout="wide")

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
    # {
    #     "number": 1,
    #     "name": "Max Verstappen",
    #     "abbreviation": "VER",
    #     "wins": 64,
    #     "poles": 41,
    #     "podiums": 114,
    #     "championships": 4,
    # },
    # {
    #     "number": 4,
    #     "name": "Lando Norris",
    #     "abbreviation": "NOR",
    #     "wins": 5,
    #     "poles": 10,
    #     "podiums": 29,
    #     "championships": 0,
    # },
    {
        "number": 10,
        "name": "Pierre Gasly",
        "abbreviation": "GAS",
        "wins": 1,
        "poles": 0,
        "podiums": 5,
        "championships": 0,
    },
    # {
    #     "number": 14,
    #     "name": "Fernando Alonso",
    #     "abbreviation": "ALO",
    #     "wins": 32,
    #     "poles": 22,
    #     "podiums": 106,
    #     "championships": 2,
    # },
    # {
    #     "number": 16,
    #     "name": "Charles Leclerc",
    #     "abbreviation": "LEC",
    #     "wins": 8,
    #     "poles": 26,
    #     "podiums": 43,
    #     "championships": 0,
    # },
    # {
    #     "number": 18,
    #     "name": "Lance Stroll",
    #     "abbreviation": "STR",
    #     "wins": 0,
    #     "poles": 1,
    #     "podiums": 3,
    #     "championships": 0,
    # },
    {
        "number": 22,
        "name": "Yuki Tsunoda",
        "abbreviation": "TSU",
        "wins": 0,
        "poles": 0,
        "podiums": 0,
        "championships": 0,
    },
    # {
    #     "number": 23,
    #     "name": "Alexander Albon",
    #     "abbreviation": "ALB",
    #     "wins": 0,
    #     "poles": 0,
    #     "podiums": 2,
    #     "championships": 0,
    # },
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
    # {
    #     "number": 63,
    #     "name": "George Russell",
    #     "abbreviation": "RUS",
    #     "wins": 3,
    #     "poles": 5,
    #     "podiums": 17,
    #     "championships": 0,
    # },
    # {
    #     "number": 81,
    #     "name": "Oscar Piastri",
    #     "abbreviation": "PIA",
    #     "wins": 3,
    #     "poles": 2,
    #     "podiums": 12,
    #     "championships": 0,
    # },
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


def format_timedelta(delta):
    if pd.isna(delta):
        return "-"
    minutes = int(delta.total_seconds() // 60)
    seconds = delta.total_seconds() % 60
    return f"{minutes}:{seconds:.3f}"


# TODO fix bugs in comparision logic
def get_driver_qualifying_info(year, track, abbreviation):

    qual_session = fastf1.get_session(year, track, "Q")
    qual_session.load()
    qual_results = qual_session.results
    driver_qual = qual_results[qual_results["Abbreviation"] == abbreviation].iloc[0]
    position = int(driver_qual["Position"])
    lap_time = (
        format_timedelta(driver_qual["Q3"])
        if pd.notna(driver_qual["Q3"])
        else (
            format_timedelta(driver_qual["Q2"])
            if pd.notna(driver_qual["Q2"])
            else format_timedelta(driver_qual["Q1"])
        )
    )
    return (
        position,
        lap_time,
        "#" + driver_qual["TeamColor"],
        driver_qual["TeamName"],
    )


def get_driver_result_info(year, track, abbreviation):
    race_session = fastf1.get_session(year, track, "R")
    race_session.load()
    race_results = race_session.results
    driver_result = race_results[race_results["Abbreviation"] == abbreviation].iloc[0]
    return (
        int(driver_result["Position"]),
        "#" + driver_result["TeamColor"],
        driver_result["TeamName"],
    )


def display_driver_overview(track, driver, abbreviation):
    _, team_color_2024, _ = get_driver_result_info(2024, track, abbreviation)
    _, team_color_2025, _ = get_driver_result_info(2025, track, abbreviation)

    year_title_24 = f"<span class='header' style='color:{team_color_2024};'>2024</span>"
    year_title_25 = f"<span class='header' style='color:{team_color_2025};'>2025</span>"

    st.markdown(
        f"<span class='header'>{year_title_24} vs {year_title_25}: {driver} at the {track}</span>",
        unsafe_allow_html=True,
    )

    # TODO load driver image, install them from f1 avif files and load them from the f1-circuits folder i guess
    st.markdown(
        f"<span class ='large'>Overall Stats</span>",
        unsafe_allow_html=True,
    )
    selected_driver_data = next((d for d in driver_stats if d["name"] == driver), None)
    if selected_driver_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"<span class='stat-value'>{selected_driver_data['wins']}</span><br><span class='stat-label'>Wins</span>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"<span class='stat-value'>{selected_driver_data['poles']}</span><br><span class='stat-label'>Poles</span>",
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"<span class='stat-value'>{selected_driver_data['podiums']}</span><br><span class='stat-label'>Podiums</span>",
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"<span class='stat-value'>{selected_driver_data['championships']}</span><br><span class='stat-label'>Championships</span>",
                unsafe_allow_html=True,
            )


def position_comparision_view(track, driver, abbreviation):

    driver_pos_24, team_color_2024, team_name_2024 = get_driver_result_info(
        2024, track, abbreviation
    )
    driver_pos_25, team_color_2025, team_name_2025 = get_driver_result_info(
        2025, track, abbreviation
    )

    st.markdown(
        f"<span class ='large'>Race</span>",
        unsafe_allow_html=True,
    )

    formatted_pos_24 = f'<span class="medium" style="color:{team_color_2024}">{driver_pos_24} with {team_name_2024}</span>'
    formatted_pos_25 = f'<span class="medium" style="color:{team_color_2025}">{driver_pos_25} with {team_name_2025}</span>'

    if driver_pos_24 < driver_pos_25:
        performance_text = f"{driver} performed <span class='medium'>BETTER</span> in {track} in 2024 compared to 2025."
    elif driver_pos_24 > driver_pos_25:
        performance_text = f"{driver} performed <span class='medium'>WORSE</span> in {track} in 2025 compared to 2024."
    else:
        performance_text = f"{driver}'s finishing position in {track} was the <span class='medium'>SAME</span> in both 2024 and 2025."

    st.markdown(
        f"<span class='regular'>In 2024, {driver} finished in position {formatted_pos_24}. In 2025, he finished in position {formatted_pos_25}.</span>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<span class='regular'>{performance_text}</span>", unsafe_allow_html=True
    )


def qualifying_comparision_view(track, driver, abbreviation):
    qual_pos_24, qual_lap_24, team_color_2024, team_name_2024 = (
        get_driver_qualifying_info(2024, track, abbreviation)
    )
    qual_pos_25, qual_lap_25, team_color_2025, team_name_2025 = (
        get_driver_qualifying_info(2025, track, abbreviation)
    )
    st.markdown(
        f"<span class='large'>Qualifying</span>",
        unsafe_allow_html=True,
    )

    if qual_pos_24 is not None and qual_pos_25 is not None:

        formatted_pos_24 = f"<span class='medium' style='color:{team_color_2024}'>{qual_pos_24} ({qual_lap_24}) with {team_name_2024}</span>"
        formatted_pos_25 = f"<span class='medium' style='color:{team_color_2025}'>{qual_pos_25} ({qual_lap_25}) with {team_name_2025}</span>"

        if qual_pos_24 < qual_pos_25:
            performance_text = f"{driver} qualified <span class='medium'>BETTER</span> at {track} in 2024 compared to 2025."
        elif qual_pos_24 > qual_pos_25:
            performance_text = f"{driver} qualified <span class='medium'>WORSE</span> at {track} in 2025 compared to 2024."
        else:
            performance_text = f"{driver}'s qualifying position at {track} was the <span class='medium'>SAME</span> in both 2024 and 2025."

        st.markdown(
            f"<span class='regular'>In 2024 qualifying, {driver} finished in position {formatted_pos_24}. "
            f"In 2025 qualifying, he finished in position {formatted_pos_25}.</span>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<span class='regular'>{performance_text}</span>", unsafe_allow_html=True
        )
    else:
        st.warning(
            f"<span class='regular'> Qualifying data not available for {driver} at {track} in one or both years.</span?"
        )


@st.cache_data
def get_fastest_qualifying_lap_telemetry_with_rpm(year, track, abbreviation):
    session = fastf1.get_session(year, track, "Q")
    session.load()
    driver_laps = session.laps.pick_drivers(abbreviation)
    fastest_lap = driver_laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry().add_distance()
    return telemetry


def interactive_overlaid_rpm_trace(
    telemetry_2024, color_2024, telemetry_2025, color_2025, driver_name
):
    fig, ax = plt.subplots()
    line1, = ax.plot(
        telemetry_2024["Distance"],
        telemetry_2024["RPM"],
        color=color_2024,
        label="2024"
    )
    line2, = ax.plot(
        telemetry_2025["Distance"],
        telemetry_2025["RPM"],
        color=color_2025,
        label="2025"
    )

    ax.set_xlabel("Distance in m")
    ax.set_ylabel("RPM")
    ax.set_title(f"{driver_name} Fastest Qualifying Lap RPM Comparison")
    ax.legend()

    labels_2024 = [
        f"Year: 2024<br>Distance: {dist:.1f}m<br>RPM: {rpm:.0f}"
        for dist, rpm in zip(telemetry_2024["Distance"], telemetry_2024["RPM"])
    ]
    labels_2025 = [
        f"Year: 2025<br>Distance: {dist:.1f}m<br>RPM: {rpm:.0f}"
        for dist, rpm in zip(telemetry_2025["Distance"], telemetry_2025["RPM"])
    ]

    plugins.connect(fig, plugins.PointLabelTooltip(line1, labels=labels_2024))
    plugins.connect(fig, plugins.PointLabelTooltip(line2, labels=labels_2025))

    html = mpld3.fig_to_html(fig)
    return html


def fastest_qualifying_lap_overlaid_rpm_view(track, driver, abbreviation):
    st.markdown(
        f"<span class='large'>Fastest Qualifying Lap Overlaid RPM Comparison</span>",
        unsafe_allow_html=True,
    )

    _, team_color_2024, _ = get_driver_result_info(2024, track, abbreviation)
    telemetry_2024 = get_fastest_qualifying_lap_telemetry_with_rpm(
        2024, track, abbreviation
    )

    _, team_color_2025, _ = get_driver_result_info(2025, track, abbreviation)
    telemetry_2025 = get_fastest_qualifying_lap_telemetry_with_rpm(
        2025, track, abbreviation
    )

    html = interactive_overlaid_rpm_trace(telemetry_2024, team_color_2024, telemetry_2025, team_color_2025, driver)
    st.components.v1.html(html, height=600)

    st.markdown(
        "<span class='regular'>The plot above shows the overlaid engine RPM of the driver during their fastest qualifying lap in 2024 and 2025. Hover over each line to see the RPM at different points in the lap for the respective year.</span>",
        unsafe_allow_html=True,
    )


def simple_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6], marker="o", linestyle="-")
    ax.set_xlabel("Simple X Axis")
    ax.set_ylabel("Simple Y Axis")
    ax.set_title("Simple Plot")
    return fig




def refresh_views():
    track = st.session_state.get("track")
    driver = st.session_state.get("driver")
    abbreviation = get_driver_abbreviation_by_name(driver)

    print(f"Selected Track in refresh_views: {track}")
    print(f"Selected Driver in refresh_views: {driver} ({abbreviation})")

    # # simple_plot()
    # st.pyplot(simple_plot())

    # display_driver_overview(track, driver, abbreviation)
    # qualifying_comparision_view(track, driver, abbreviation)
    print(fastest_qualifying_lap_overlaid_rpm_view(track, driver, abbreviation))
    # print(get_fastest_qualifying_lap_object(2025, track, abbreviation))

    # position_comparision_view(track, driver, abbreviation)


# on change watchers
selected_track_name = st.sidebar.selectbox(
    "Select Track", events_2025, key="track", on_change=refresh_views
)

# Add driver selector to sidebar
selected_driver_name = st.sidebar.selectbox(
    "Select Driver", driver_names, key="driver", on_change=refresh_views
)
