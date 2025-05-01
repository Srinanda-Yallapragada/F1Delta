import streamlit as st
import numpy as np
import plotly.graph_objects as go

from data_processing import *


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


##Crap code TODO
def interactive_overlaid_rpm_trace_with_corners(
    telemetry_2024, color_2024, telemetry_2025, color_2025, driver_name, corners
):
    if telemetry_2024 is None or telemetry_2025 is None:
        return None  # Return None if telemetry data is missing

    fig = go.Figure(
        layout_title_text=f"{driver_name} Fastest Qualifying Lap RPM Comparison with Corners"
    )

    fig.add_trace(
        go.Scattergl(
            x=telemetry_2024["Distance"],
            y=telemetry_2024["RPM"],
            mode="lines",
            name="2024",
            line=dict(color=color_2024),
            hovertemplate="Distance: %{x:.1f}m<br>RPM 2024: %{y:.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=telemetry_2025["Distance"],
            y=telemetry_2025["RPM"],
            mode="lines",
            name="2025",
            line=dict(color=color_2025),
            hovertemplate="Distance: %{x:.1f}m<br>RPM 2025: %{y:.0f}<extra></extra>",
        )
    )

    if corners is not None and not corners.empty:
        v_min_rpm = min(
            telemetry_2024["RPM"].min() if not telemetry_2024.empty else 0,
            telemetry_2025["RPM"].min() if not telemetry_2025.empty else 0,
        )
        v_max_rpm = max(
            telemetry_2024["RPM"].max() if not telemetry_2024.empty else 0,
            telemetry_2025["RPM"].max() if not telemetry_2025.empty else 0,
        )

        for _, corner in corners.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[corner["Distance"], corner["Distance"]],
                    y=[v_min_rpm - 500, v_max_rpm + 500],
                    mode="lines",
                    line=dict(color="grey", dash="dot"),
                    name=f"Corner {corner['Number']}{corner['Letter']}",
                    showlegend=False,
                    hovertemplate=f"Corner {corner['Number']}{corner['Letter']}<extra></extra>",
                )
            )
            fig.add_annotation(
                x=corner["Distance"],
                y=v_min_rpm - 750,
                text=f"{corner['Number']}{corner['Letter']}",
                showarrow=False,
                align="center",
            )

    fig.update_layout(
        xaxis_title="Distance in m",
        yaxis_title="RPM",
        legend_title="Year",
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        title_font_color="white",
        legend_font_color="white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


##Crap code TODO
def fastest_qualifying_lap_overlaid_rpm_view(track, driver, abbreviation):
    st.markdown(
        f"<span class='large'>Fastest Qualifying Lap Overlaid RPM Comparison with Corners</span>",
        unsafe_allow_html=True,
    )

    result_24 = get_driver_result_info(2024, track, abbreviation)
    result_25 = get_driver_result_info(2025, track, abbreviation)

    if result_24 and result_25:
        _, team_color_2024, _ = result_24
        _, team_color_2025, _ = result_25

        telemetry_2024 = get_fastest_qualifying_lap_telemetry(2024, track, abbreviation)
        telemetry_2025 = get_fastest_qualifying_lap_telemetry(2025, track, abbreviation)

        corners = get_circuit_info(2024, track)  # Assuming track layout is consistent

        fig_rpm = interactive_overlaid_rpm_trace_with_corners(
            telemetry_2024,
            team_color_2024,
            telemetry_2025,
            team_color_2025,
            driver,
            corners,
        )
        if fig_rpm:
            st.plotly_chart(fig_rpm, use_container_width=True)
        else:
            st.warning(
                f"Could not generate RPM comparison plot with corners for {driver} at {track}."
            )

        st.markdown(
            "<span class='regular'>The plot above shows the overlaid engine RPM of the driver during their fastest qualifying lap in 2024 and 2025, with vertical lines indicating the approximate locations of corners.</span>",
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            f"Could not retrieve team color information for {driver} at {track}."
        )


##Crap code TODO
def interactive_overlaid_speed_trace_with_corners_highlight(
    telemetry_2024, color_2024, telemetry_2025, color_2025, driver_name, corners
):
    """
    Plots the speed of two laps on the same graph, with corner annotations and
    highlighting the background based on which team is faster.

    Args:
        telemetry_2024 (pd.DataFrame): Telemetry data for the first lap (2024).
        color_2024 (str): Color for the first lap's line and highlight.
        telemetry_2025 (pd.DataFrame): Telemetry data for the second lap (2025).
        color_2025 (str): Color for the second lap's line and highlight.
        driver_name (str): Name of the driver.
        corners (pd.DataFrame): DataFrame containing corner information.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object, or None on error.
    """
    if telemetry_2024 is None or telemetry_2025 is None:
        return None

    fig = go.Figure(
        layout_title_text=f"{driver_name} Fastest Qualifying Lap Speed Comparison with Corners (Highlighted)"
    )

    fig.add_trace(
        go.Scattergl(
            x=telemetry_2024["Distance"],
            y=telemetry_2024["Speed"],
            mode="lines",
            name="2024",
            line=dict(color=color_2024),
            hovertemplate="Distance: %{x:.1f}m<br>Speed 2024: %{y:.1f} km/h<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scattergl(
            x=telemetry_2025["Distance"],
            y=telemetry_2025["Speed"],
            mode="lines",
            name="2025",
            line=dict(color=color_2025),
            hovertemplate="Distance: %{x:.1f}m<br>Speed 2025: %{y:.1f} km/h<extra></extra>",
        )
    )

    # Highlight based on speed difference
    if not telemetry_2024.empty and not telemetry_2025.empty:
        # Interpolate speeds to common distance points for comparison
        common_distances = np.sort(
            np.unique(
                np.concatenate(
                    [
                        telemetry_2024["Distance"].values,
                        telemetry_2025["Distance"].values,
                    ]
                )
            )
        )
        speed_2024_interp = np.interp(
            common_distances,
            telemetry_2024["Distance"],
            telemetry_2024["Speed"],
            left=np.nan,
            right=np.nan,
        )
        speed_2025_interp = np.interp(
            common_distances,
            telemetry_2025["Distance"],
            telemetry_2025["Speed"],
            left=np.nan,
            right=np.nan,
        )

        highlight_shapes = []
        for i in range(len(common_distances) - 1):
            dist_start = common_distances[i]
            dist_end = common_distances[i + 1]
            speed_diff = speed_2024_interp[i] - speed_2025_interp[i]

            if not np.isnan(speed_2024_interp[i]) and not np.isnan(
                speed_2025_interp[i]
            ):
                if speed_diff > 1:  # 2024 is significantly faster
                    highlight_shapes.append(
                        go.layout.Shape(
                            type="rect",
                            x0=dist_start,
                            y0=min(
                                telemetry_2024["Speed"].min(),
                                telemetry_2025["Speed"].min(),
                            )
                            - 10,
                            x1=dist_end,
                            y1=max(
                                telemetry_2024["Speed"].max(),
                                telemetry_2025["Speed"].max(),
                            )
                            + 10,
                            fillcolor=color_2024,
                            opacity=0.15,
                            layer="below",
                            line_width=0,
                        )
                    )
                elif speed_diff < -1:  # 2025 is significantly faster
                    highlight_shapes.append(
                        go.layout.Shape(
                            type="rect",
                            x0=dist_start,
                            y0=min(
                                telemetry_2024["Speed"].min(),
                                telemetry_2025["Speed"].min(),
                            )
                            - 10,
                            x1=dist_end,
                            y1=max(
                                telemetry_2024["Speed"].max(),
                                telemetry_2025["Speed"].max(),
                            )
                            + 10,
                            fillcolor=color_2025,
                            opacity=0.15,
                            layer="below",
                            line_width=0,
                        )
                    )
        fig.update_layout(shapes=highlight_shapes)

    if corners is not None and not corners.empty:
        v_min_speed = min(
            telemetry_2024["Speed"].min() if not telemetry_2024.empty else 0,
            telemetry_2025["Speed"].min() if not telemetry_2025.empty else 0,
        )
        v_max_speed = max(
            telemetry_2024["Speed"].max() if not telemetry_2024.empty else 0,
            telemetry_2025["Speed"].max() if not telemetry_2025.empty else 0,
        )

        for _, corner in corners.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[corner["Distance"], corner["Distance"]],
                    y=[v_min_speed - 10, v_max_speed + 10],
                    mode="lines",
                    line=dict(color="grey", dash="dot"),
                    name=f"Corner {corner['Number']}{corner['Letter']}",
                    showlegend=False,
                    hovertemplate=f"Corner {corner['Number']}{corner['Letter']}<extra></extra>",
                )
            )
            fig.add_annotation(
                x=corner["Distance"],
                y=v_min_speed - 20,
                text=f"{corner['Number']}{corner['Letter']}",
                showarrow=False,
                align="center",
            )

    fig.update_layout(
        xaxis_title="Distance in m",
        yaxis_title="Speed in km/h",
        legend_title="Year",
        xaxis=dict(color="white"),
        yaxis=dict(color="white"),
        title_font_color="white",
        legend_font_color="white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


##Crap code TODO
def fastest_qualifying_lap_speed_view(track, driver, abbreviation):
    st.markdown(
        f"<span class='large'>Fastest Qualifying Lap Speed Comparison with Corners (Highlighted)</span>",
        unsafe_allow_html=True,
    )

    result_24 = get_driver_result_info(2024, track, abbreviation)
    result_25 = get_driver_result_info(2025, track, abbreviation)

    if result_24 and result_25:
        team_color_2024 = result_24[1]
        team_color_2025 = result_25[1]

        telemetry_2024 = get_fastest_qualifying_lap_telemetry(2024, track, abbreviation)
        telemetry_2025 = get_fastest_qualifying_lap_telemetry(2025, track, abbreviation)
        corners = get_circuit_info(2024, track)

        fig_speed_highlight = interactive_overlaid_speed_trace_with_corners_highlight(
            telemetry_2024,
            team_color_2024,
            telemetry_2025,
            team_color_2025,
            driver,
            corners,
        )
        if fig_speed_highlight:
            st.plotly_chart(fig_speed_highlight, use_container_width=True)
        else:
            st.warning(
                f"Could not generate highlighted speed comparison plot with corners for {driver} at {track}."
            )

        st.markdown(
            "<span class='regular'>The plot above shows the overlaid speed of the driver during their fastest qualifying lap in 2024 and 2025, with vertical lines indicating the approximate locations of corners. The background is highlighted in the color of the team that was significantly faster at that part of the lap.</span>",
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            f"Could not retrieve team color information for {driver} at {track}."
        )
