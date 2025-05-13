import streamlit as st
import fastf1
import pandas as pd
from datetime import datetime

import json
import os


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
    # {
    #     "number": 10,
    #     "name": "Pierre Gasly",
    #     "abbreviation": "GAS",
    #     "wins": 1,
    #     "poles": 0,
    #     "podiums": 5,
    #     "championships": 0,
    # },
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



def get_track_id(track_name):
    # Load the locations JSON file
    with open('public/f1-circuits/f1-locations.json', 'r') as f:
        locations = json.load(f)
    
    # Map of Grand Prix names to circuit names
    track_name_mapping = {
        "Australian Grand Prix": "Albert Park Circuit",
        "Bahrain Grand Prix": "Bahrain International Circuit",
        "Saudi Arabian Grand Prix": "Jeddah Corniche Circuit",
        "Japanese Grand Prix": "Suzuka International Racing Course",
        "Chinese Grand Prix": "Shanghai International Circuit",
        "Miami Grand Prix": "Miami International Autodrome",
        "Emilia Romagna Grand Prix": "Autodromo Enzo e Dino Ferrari",
        "Monaco Grand Prix": "Circuit de Monaco",
        "Canadian Grand Prix": "Circuit Gilles-Villeneuve",
        "Spanish Grand Prix": "Circuit de Barcelona-Catalunya",
        "Austrian Grand Prix": "Red Bull Ring",
        "British Grand Prix": "Silverstone Circuit",
        "Hungarian Grand Prix": "Hungaroring",
        "Belgian Grand Prix": "Circuit de Spa-Francorchamps",
        "Dutch Grand Prix": "Circuit Zandvoort",
        "Italian Grand Prix": "Autodromo Nazionale Monza",
        "Singapore Grand Prix": "Marina Bay Street Circuit",
        "United States Grand Prix": "Circuit of the Americas",
        "Mexican Grand Prix": "Autódromo Hermanos Rodríguez",
        "Brazilian Grand Prix": "Autódromo José Carlos Pace - Interlagos",
        "Las Vegas Grand Prix": "Las Vegas Street Circuit",
        "Qatar Grand Prix": "Losail International Circuit",
        "Abu Dhabi Grand Prix": "Yas Marina Circuit"
    }
    
    # Convert Grand Prix name to circuit name if it exists in mapping
    circuit_name = track_name_mapping.get(track_name, track_name)
    
    # Find the track by name
    for location in locations:
        if location['name'] == circuit_name:
            return location['id']
    return None

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
def get_driver_race_info(year, track, abbreviation):

    race_session = fastf1.get_session(year, track, "R")
    race_session.load()
    race_results = race_session.results
    driver_race = race_results[race_results["Abbreviation"] == abbreviation].iloc[0]
    position = int(driver_race["Position"])
    team_color = "#" + driver_race["TeamColor"]

    return (position, team_color)
def get_teammate_info(year, track, abbreviation):
    race_session = fastf1.get_session(year, track, "R")
    race_session.load()
    race_results = race_session.results
    
    driver_race = race_results[race_results["Abbreviation"] == abbreviation].iloc[0]
    team_name = driver_race["TeamName"]
    
    team_drivers = race_results[race_results["TeamName"] == team_name]

    team_mate = team_drivers[team_drivers["Abbreviation"] != abbreviation].iloc[0]
    return team_mate
    

@st.cache_data
def get_fastest_qualifying_lap_telemetry(year, track, abbreviation):
    session = fastf1.get_session(year, track, "Q")
    session.load()
    driver_laps = session.laps.pick_drivers(abbreviation)
    fastest_lap = driver_laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry().add_distance()
    # print(telemetry)
    return telemetry


# crap code TODO
@st.cache_data
def get_circuit_info(year, track):
    try:
        session = fastf1.get_session(
            year, track, "Q"
        )  # Using Qualifying to get circuit info
        session.load()
        circuit_info = session.get_circuit_info()
        return circuit_info.corners
    except Exception as e:
        print(f"Error fetching circuit info for {year}, {track}: {e}")
        return None


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


@st.cache_data
def get_fastest_qualifying_lap_telemetry(year, track, abbreviation):
    session = fastf1.get_session(year, track, "Q")
    session.load()
    driver_laps = session.laps.pick_drivers(abbreviation)
    fastest_lap = driver_laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry().add_distance()
    # print(telemetry)
    return telemetry


@st.cache_data
def get_race_telemetry(year, track, abbreviation):

    race = fastf1.get_session(year, track, "R")
    race.load()
    laps = race.laps.pick_drivers(abbreviation)
    # telemetry = laps.get_telemetry().compute() # may need to change #TODO
    telemetry = laps.get_telemetry().add_distance()
    return telemetry


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
