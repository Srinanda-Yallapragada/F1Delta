import streamlit as st
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

# Page title
st.title("F1 Data Visualization")
st.write("Charles Leclerc's Speed Data from Monza 2019 Qualifying")

# Initialize and load F1 data
@st.cache_data  # This caches the data to improve performance
def load_f1_data():
    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')
    session = fastf1.get_session(2019, 'Monza', 'Q')
    session.load()
    fast_leclerc = session.laps.pick_drivers('LEC').pick_fastest()
    lec_car_data = fast_leclerc.get_car_data()
    return lec_car_data

# Show a loading spinner while data is being fetched
with st.spinner("Loading F1 data..."):
    lec_car_data = load_f1_data()

# Extract time and speed data
t = lec_car_data['Time']
vCar = lec_car_data['Speed']

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, vCar, label='Fast', color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')
ax.set_title('Leclerc Speed Data - Monza 2019 Qualifying')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Add some additional information
st.subheader("Data Information")
st.write(f"Maximum Speed: {vCar.max()} Km/h")
st.write(f"Average Speed: {vCar.mean():.2f} Km/h")

# Show raw data in an expandable section
with st.expander("View Raw Data"):
    st.dataframe(lec_car_data)