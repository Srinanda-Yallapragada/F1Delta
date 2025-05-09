import streamlit as st
import fastf1
import pandas as pd
import plotly.graph_objects as go
from data_processing import *


def relative_performance_view(track, driver, abbreviation):

    st.subheader("Comparision Against Team-Mate. Qualifying and Race Position")

    fig = go.Figure()
    y_labels = []  # To track unique y-axis labels in the desired order

    for year in [2024, 2025]:
        if track not in (
            get_completed_events_2025() if year == 2025 else get_completed_events_2024()
        ):
            continue

        try:
            # Driver info
            qual_pos, _, team_color, _ = get_driver_qualifying_info(
                year, track, abbreviation
            )
            race_pos, _ = get_driver_race_info(year, track, abbreviation)

            # Teammate info
            teammate = get_teammate_info(year, track, abbreviation)
            teammate_abbr = teammate["Abbreviation"]
            teammate_name = teammate["FullName"]
            qual_pos_tm, _, team_color_tm, _ = get_driver_qualifying_info(
                year, track, teammate_abbr
            )
            race_pos_tm, _ = get_driver_race_info(year, track, teammate_abbr)

            # Add y-axis labels in order
            y_labels.append(f"{driver} ({year})")
            y_labels.append(f"{teammate_name} ({year})")

            # Add traces for driver
            fig.add_trace(
                go.Scatter(
                    x=[qual_pos, race_pos],
                    y=[f"{driver} ({year})", f"{driver} ({year})"],
                    mode="lines+markers",
                    line=dict(color="lightgray", width=3),
                    marker=dict(size=12, color=team_color),
                    name=f"{driver} ({year})",
                    showlegend=True,
                    hovertemplate=[
                        f"{driver} ({year})<br>Qualifying Position: {qual_pos}<extra></extra>",
                        f"{driver} ({year})<br>Race Finish Position: {race_pos}<extra></extra>",
                    ],
                )
            )
            fig.add_annotation(
                x=race_pos,
                y=f"{driver} ({year})",
                ax=qual_pos,
                ay=f"{driver} ({year})",
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor=team_color,
            )

            # Add traces for teammate
            fig.add_trace(
                go.Scatter(
                    x=[qual_pos_tm, race_pos_tm],
                    y=[f"{teammate_name} ({year})", f"{teammate_name} ({year})"],
                    mode="lines+markers",
                    line=dict(color="lightgray", width=3),
                    marker=dict(size=12, color=team_color_tm),
                    name=f"{teammate_name} ({year})",
                    showlegend=True,
                    hovertemplate=[
                        f"{teammate_name} ({year})<br>Qualifying Position: {qual_pos_tm}<extra></extra>",
                        f"{teammate_name} ({year})<br>Race Finish Position: {race_pos_tm}<extra></extra>",
                    ],
                )
            )
            fig.add_annotation(
                x=race_pos_tm,
                y=f"{teammate_name} ({year})",
                ax=qual_pos_tm,
                ay=f"{teammate_name} ({year})",
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor=team_color_tm,
            )

        except Exception as e:
            st.error(f"Data not available for {driver} at {track} ({year})")
            st.exception(e)

    # Deduplicate y-labels while preserving order
    seen = set()
    unique_y_labels = []
    for label in y_labels:
        if label not in seen:
            seen.add(label)
            unique_y_labels.append(label)

    fig.update_layout(
        title=f"Relative Performance at {track} (2024 vs 2025)",
        xaxis_title="Position",
        yaxis_title="Driver",
        xaxis=dict(
            autorange=False,
            tickmode="linear",
            dtick=1,
            range=[20.5, 0.5],  # Show grid positions from 1 to 20
            ticktext=[str(i) for i in range(1, 21)],
            tickvals=[i for i in range(1, 21)],
        ),
        yaxis=dict(
            title="Driver",
            categoryorder="array",
            categoryarray=unique_y_labels,
        ),
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )

    st.plotly_chart(fig)