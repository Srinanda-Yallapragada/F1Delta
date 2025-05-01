import streamlit as st
from data_processing import *

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

