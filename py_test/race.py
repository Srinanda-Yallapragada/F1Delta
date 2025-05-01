import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt, mpld3  # use st.pyplot for interactivity
from mpld3 import fig_to_html, plugins
import fastf1
import fastf1.plotting
import pandas as pd
from datetime import datetime
import numpy as np

import plotly.express as px
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

