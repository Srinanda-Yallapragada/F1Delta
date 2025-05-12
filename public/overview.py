import streamlit as st
import os
from data_processing import *
import base64


def display_driver_overview(track, driver, abbreviation):
    _, team_color_2024, _ = get_driver_result_info(2024, track, abbreviation)
    _, team_color_2025, _ = get_driver_result_info(2025, track, abbreviation)
    year_title_24 = f"<span class='header' style='color:{team_color_2024};'>2024</span>"
    year_title_25 = f"<span class='header' style='color:{team_color_2025};'>2025</span>"
    st.markdown(
        f"<span class='header'>{year_title_24} vs {year_title_25}: {driver} at the {track}</span>",
        unsafe_allow_html=True,
    )

    # Create a container for the stats, driver image, and more stats
    stats_col1, image_col, stats_col2 = st.columns([1, 1, 1])

    selected_driver_data = next((d for d in driver_stats if d["name"] == driver), None)

    if selected_driver_data:
        with stats_col1:
            col1, col2 = st.columns(2)
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

        with image_col:
            driver_image = f"driver_images/{driver}.png"
            encoded = base64.b64encode(open(driver_image, 'rb').read()).decode()
            st.markdown(
                f"""
                <div style='display: flex; justify-content: center; align-items: center; height: 100%;'>
                    <img src="data:image/png;base64,{encoded}" 
                        style="width: 200px; max-height: 220px; object-fit: contain; border-radius: 10px;" />
                </div>
                """,
                unsafe_allow_html=True,
            )

        with stats_col2:
            col3, col4 = st.columns(2)
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

    # Add track SVG in its own section, outside of the columns
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Spacer

    # Display the track SVG in a dedicated section
    track_id = get_track_id(track)
    svg_path = f"../public/f1-circuits/svgs/{track_id}.svg"
    if os.path.exists(svg_path):
        with open(svg_path, "r") as f:
            svg_content = f.read()
        svg_content = svg_content.replace(
            'style="width:100%;height:auto;display:block;"', ""
        )
        st.markdown(
            f"""
            <div style='width: 100%; text-align: center; margin: 20px auto;'>
                <div style='display: inline-block; background-color: #1e1e2e; padding: 20px; border-radius: 10px; border: 1px solid #333344;'>
                    <h2 style='color: #ffffff; margin-bottom: 15px;'>{track} Circuit</h2>
                    {svg_content}

            """,
            unsafe_allow_html=True,
        )
