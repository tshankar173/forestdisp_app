
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("ForestDISP Model - Web Version")

# Input Widgets
droplet_size = st.number_input("Droplet Size (microns):", min_value=1.0, value=50.0)
wind_speed = st.number_input("Wind Speed (m/s):", min_value=0.0, value=5.0)
canopy_density = st.slider("Canopy Density (0-1):", min_value=0.0, max_value=1.0, value=0.5)
spray_volume = st.number_input("Spray Volume (L):", min_value=1.0, value=10.0)
temperature = st.number_input("Temperature (°C):", min_value=-10.0, max_value=50.0, value=20.0)
humidity = st.slider("Humidity (%):", min_value=0, max_value=100, value=50)
nozzle_type = st.selectbox("Nozzle Type:", ["Flat Fan", "Hollow Cone", "Full Cone"])

# Calculate Nozzle Factor
nozzle_factor = {"Flat Fan": 1.2, "Hollow Cone": 1.0, "Full Cone": 0.8}.get(nozzle_type, 1.0)

# Simulate Dispersion
if st.sidebar.button("Simulate"):
    x = np.linspace(0, 100, 50)
    y = np.linspace(-20, 20, 50)
    X, Y = np.meshgrid(x, y)
    Z = (np.exp(-X / (10 + canopy_density)) * spray_volume / droplet_size) *         (1 - (wind_speed / 50)) * (1 - (humidity / 100)) * nozzle_factor
    Z *= (1 + (temperature - 20) / 100)

    # Plot 3D Dispersion
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title("Spray Dispersion - 3D Visualization")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Crosswind Spread (m)")
    ax.set_zlabel("Droplet Density")
    st.pyplot(fig)

# Display plot in Streamlit
    st.pyplot(fig)

    # Add numerical summary
    st.subheader("Simulation Results")
    st.write(f"### Input Parameters:")
    st.write(f"- Droplet Size: {droplet_size} microns")
    st.write(f"- Wind Speed: {wind_speed} m/s")
    st.write(f"- Canopy Density: {canopy_density}")
    st.write(f"- Spray Volume: {spray_volume} L")
    st.write(f"- Temperature: {temperature} °C")
    st.write(f"- Humidity: {humidity}%")
    st.write(f"- Nozzle Type: {nozzle_type}")
else:
    st.write("Adjust parameters in the sidebar and click **Simulate** to see the results.")
    
