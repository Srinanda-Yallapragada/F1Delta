import streamlit as st
import os
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
    
    # Create a container for the stats, driver image, and more stats
    stats_col1, image_col, stats_col2 = st.columns([1, 1, 1])
    
    selected_driver_data = next(
        (d for d in driver_stats if d["name"] == driver), None
    )

    if selected_driver_data:
        with stats_col1:
            st.markdown(
                f"<div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>",
                unsafe_allow_html=True,
            )
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
            st.markdown("</div>", unsafe_allow_html=True)

        with image_col:
            st.markdown(
                f"<div style='text-align: center; padding: 10px;'>",
                unsafe_allow_html=True,
            )
            driver_image = f"driver_images/{driver}.png"
            st.image(driver_image, width=250, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with stats_col2:
            st.markdown(
                f"<div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>",
                unsafe_allow_html=True,
            )
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
            st.markdown("</div>", unsafe_allow_html=True)

    # Add track SVG in its own section, outside of the columns
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Spacer

    # Display the track SVG in a dedicated section
    track_id = get_track_id(track)
    svg_path = f"../public/f1-circuits/svgs/{track_id}.svg"
    if os.path.exists(svg_path):
        with open(svg_path, "r") as f:
            svg_content = f.read()
        
        # Track SVG with dark theme background that complements the page
        st.markdown(
            f"""
            <div style='width: 100%; text-align: center; margin: 20px auto;'>
                <div style='width: 80%; max-width: 600px; margin: 0 auto; background-color: #1e1e2e; padding: 20px; border-radius: 10px; border: 1px solid #333344;'>
                    {svg_content}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )