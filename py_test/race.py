import streamlit as st
import numpy as np
import plotly.graph_objects as go

from data_processing import *


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

    st.markdown(
        f"<span class='regular'>In 2024, {driver} finished in position {formatted_pos_24}. In 2025, he finished in position {formatted_pos_25}.</span>",
        unsafe_allow_html=True,
    )
    if driver_pos_24 < driver_pos_25:
        performance_text = f"{driver} performed <span class='medium'>WORSE</span> in {track} in 2025 compared to 2024."
    elif driver_pos_24 > driver_pos_25:
        performance_text = f"{driver} performed <span class='medium'>BETTER</span> in {track} in 2025 compared to 2024."
    else:
        performance_text = f"{driver}'s finishing position in {track} was the <span class='medium'>SAME</span> in both 2024 and 2025."

    st.markdown(
        f"<span class='regular'>{performance_text}</span>", unsafe_allow_html=True
    )


def avg_speed_vs_distance_race_plotly(
    telemetry_2024, color_2024, telemetry_2025, color_2025, driver_name, corners
):

    fig = go.Figure(
        layout_title_text=f"2024 vs 2025 {driver_name} Average Race Speed Comparison",
        layout_title_font=dict(
            size=30,
        ),
    )

    num_segments = 200  # Number of segments to calculate average speed over

    # Calculate average speed for 2024
    if not telemetry_2024.empty:
        max_distance_2024 = telemetry_2024["Distance"].max()
        distance_points_2024 = np.linspace(0, max_distance_2024, num_segments + 1)
        avg_speed_2024 = []
        mid_points_2024 = []
        for i in range(num_segments):
            start_dist = distance_points_2024[i]
            end_dist = distance_points_2024[i + 1]
            segment = telemetry_2024[
                (telemetry_2024["Distance"] >= start_dist)
                & (telemetry_2024["Distance"] < end_dist)
            ]
            if not segment.empty:
                avg_speed_2024.append(segment["Speed"].mean())
                mid_points_2024.append((start_dist + end_dist) / 2)
            else:
                avg_speed_2024.append(np.nan)
                mid_points_2024.append((start_dist + end_dist) / 2)

        fig.add_trace(
            go.Scattergl(
                x=mid_points_2024,
                y=avg_speed_2024,
                mode="lines",
                name="2024",
                line=dict(color=color_2024),
                hovertemplate="Distance: %{x:.1f}m<br>Avg Speed 2024: %{y:.1f} km/h<extra></extra>",
            )
        )

    # Calculate average speed for 2025
    if not telemetry_2025.empty:
        max_distance_2025 = telemetry_2025["Distance"].max()
        distance_points_2025 = np.linspace(0, max_distance_2025, num_segments + 1)
        avg_speed_2025 = []
        mid_points_2025 = []
        for i in range(num_segments):
            start_dist = distance_points_2025[i]
            end_dist = distance_points_2025[i + 1]
            segment = telemetry_2025[
                (telemetry_2025["Distance"] >= start_dist)
                & (telemetry_2025["Distance"] < end_dist)
            ]
            if not segment.empty:
                avg_speed_2025.append(segment["Speed"].mean())
                mid_points_2025.append((start_dist + end_dist) / 2)
            else:
                avg_speed_2025.append(np.nan)
                mid_points_2025.append((start_dist + end_dist) / 2)

        fig.add_trace(
            go.Scattergl(
                x=mid_points_2025,
                y=avg_speed_2025,
                mode="lines",
                name="2025",
                line=dict(color=color_2025),
                hovertemplate="Distance: %{x:.1f}m<br>Avg Speed 2025: %{y:.1f} km/h<extra></extra>",
            )
        )

    # Add corner markers
    if corners is not None and not corners.empty:
        min_y = min(
            telemetry_2024["Speed"].min() if not telemetry_2024.empty else 0,
            telemetry_2025["Speed"].min() if not telemetry_2025.empty else 0,
        )
        max_y = max(
            telemetry_2024["Speed"].max() if not telemetry_2024.empty else 0,
            telemetry_2025["Speed"].max() if not telemetry_2025.empty else 0,
        )
        y_range = max_y - min_y
        y_offset = y_range * 0.1  # Small offset for annotation

        for _, corner in corners.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[corner["Distance"], corner["Distance"]],
                    y=[min_y - y_offset, max_y + y_offset],
                    mode="lines",
                    line=dict(color="grey", dash="dot"),
                    name=f"Corner {corner['Number']}{corner['Letter']}",
                    showlegend=False,
                    hovertemplate=f"Corner {corner['Number']}{corner['Letter']}<extra></extra>",
                )
            )
            fig.add_annotation(
                x=corner["Distance"],
                y=min_y - 2 * y_offset,
                text=f"{corner['Number']}{corner['Letter']}",
                showarrow=False,
                align="center",
            )

    fig.update_layout(
        xaxis_title="Distance in m",
        yaxis_title="Average Speed in km/h",
        legend_title="Year",
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        title_font_color="white",
        legend_font_color="white",
        paper_bgcolor="rgba(0,0,0,0)",  # transparency
        plot_bgcolor="rgba(0,0,0,0)",  # transparency
    )
    return fig


def avg_speed_vs_distance_race_view(track, driver, abbreviation):
    _, team_color_2024, _ = get_driver_result_info(2024, track, abbreviation)
    _, team_color_2025, _ = get_driver_result_info(2025, track, abbreviation)

    telemetry_2024 = get_race_telemetry(2024, track, abbreviation)
    telemetry_2025 = get_race_telemetry(2025, track, abbreviation)

    corners = get_circuit_info(2024, track)  # Assuming track layout is consistent

    fig_speed = avg_speed_vs_distance_race_plotly(
        telemetry_2024,
        team_color_2024,
        telemetry_2025,
        team_color_2025,
        driver,
        corners,
    )

    st.plotly_chart(fig_speed, use_container_width=True)
    # TODO improve write up and explanantion of the graph
    st.markdown(
        "<span class='regular'>The plot above shows the overlaid engine RPM of the driver during their fastest qualifying lap in 2024 and 2025, with vertical lines indicating the approximate locations of corners.</span>",
        unsafe_allow_html=True,
    )
