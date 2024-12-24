
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Inject custom CSS for the background
page_bg = """
<style>
    body {
        background-image: url('https://images.unsplash.com/photo-1597754707831-bc713fa453b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    .stApp {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# App Title
st.title("ð² ForestDISP Model - Web Version")

# First Section: UAV Type
st.header("1. UAV Type")
with st.expander("Rotor Type and Details"):
    rotor_type = st.radio("Rotor Type:", ["Single", "Multiple"])
    num_rotors = st.selectbox("Number of Rotors:", [1, 4, 6, 8])
    arm_length = st.number_input("Arm Length (m):", min_value=0.1, value=1.0)
    nozzle_position = st.number_input("Nozzle Position (m):", min_value=0.0, value=0.5)

# Second Section: Application Method
st.header("2. Application Method")
with st.expander("Flight Parameters"):
    flight_speed = st.number_input("Flight Speed (m/s):", min_value=0.1, value=5.0)
    flight_height = st.number_input("Flight Height (m):", min_value=1.0, value=10.0)
    application_rate = st.number_input("Application Rate (L/Ha):", min_value=0.1, value=10.0)
    flow_rate = st.number_input("Flow Rate (L/min):", min_value=0.1, value=1.0)
    swath_width = st.number_input("Swath Width (m):", min_value=0.1, value=5.0)

# Third Section: Meteorology
st.header("3. Meteorology")
with st.expander("Environmental Conditions"):
    wind_speed = st.number_input("Wind Speed (m/s):", min_value=0.0, value=2.0)
    wind_direction = st.slider("Wind Direction (Â°):", min_value=0, max_value=360, value=90)
    temperature = st.number_input("Temperature (Â°C):", min_value=-10.0, max_value=50.0, value=25.0)
    humidity = st.slider("Humidity (%):", min_value=0, max_value=100, value=50)

# Fourth Section: Spray Material
st.header("4. Spray Material")
with st.expander("Mixing Ratios"):
    water_ratio = st.number_input("Water (ratio):", min_value=0.0, value=1.0)
    adjuvant_type = st.selectbox("Adjuvant Type:", ["None", "Surfactant", "Oil", "Other"])
    dye_ratio = st.number_input("Dye (ratio):", min_value=0.0, value=0.0)
    pesticide_ratio = st.number_input("Pesticide (ratio):", min_value=0.0, value=0.0)

# Fifth Section: Surface Material
st.header("5. Surface Material")
with st.expander("Surface Characteristics"):
    cover_type = st.selectbox("Cover Type:", ["Grass", "Crop", "Tree", "Other"])
    canopy_height = st.number_input("Canopy Height (m):", min_value=0.0, value=1.0)
    row_spacing = st.number_input("Row Spacing (m):", min_value=0.1, value=1.0)
    column_spacing = st.number_input("Column Spacing (m):", min_value=0.1, value=1.0)

# Results Section
if st.sidebar.button("Run Simulation"):
    # Generate data
    x = np.linspace(0, 100, 200)  # Distance in meters
    drift_factor = np.exp(-x / (20 + wind_speed))  # Drift decay
    deposition_rate = (
        application_rate
        * flow_rate
        / (swath_width * flight_speed)
        * drift_factor
    )
    spray_drift = deposition_rate * (1 - wind_speed / 10)

    # Calculate cumulative drift percentage
    cumulative_drift = np.cumsum(spray_drift) / np.sum(spray_drift) * 100

    # Find distance for 90% cumulative drift
    threshold_index = np.argmax(cumulative_drift >= 90)  # First index where cumulative drift >= 90%
    threshold_distance = x[threshold_index] if threshold_index < len(x) else None

    # Plot results
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Primary axis: Deposition and Drift
    ax1.plot(x, deposition_rate, label="Spray Deposition", color="green")
    ax1.plot(x, spray_drift, label="Spray Drift", color="blue", linestyle="--")
    ax1.set_xlabel("Distance (m)")
    ax1.set_ylabel("Rate (L/mÂ²)")
    ax1.legend(loc="upper left")

    # Secondary axis: Cumulative Drift Percentage
    ax2 = ax1.twinx()
    ax2.plot(x, cumulative_drift, label="Cumulative Drift %", color="red", linestyle="-.")
    ax2.set_ylabel("Cumulative Drift (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.axhline(90, color="gray", linestyle=":", linewidth=1)  # Horizontal line at 90%

    # Mark 90% cumulative drift point
    if threshold_distance is not None:
        ax2.plot(
            threshold_distance,
            90,
            marker="o",
            markersize=8,
            color="black",
            label=f"90% Drift at {threshold_distance:.1f} m",
        )
        ax1.annotate(
            f"{threshold_distance:.1f} m",
            xy=(threshold_distance, deposition_rate[threshold_index]),
            xytext=(threshold_distance + 5, deposition_rate[threshold_index] + 0.1),
            arrowprops=dict(facecolor="black", arrowstyle="->"),
        )

    # Finalize plot
    fig.tight_layout()
    ax2.legend(loc="upper right")
    ax1.set_title("Spray Deposition and Drift with Cumulative Drift Percentage")
    st.pyplot(fig)

    # Display Results
    st.subheader("Simulation Results")
    st.write("### Spray Deposition and Drift")
    st.write(f"- **Maximum Deposition Rate:** {np.max(deposition_rate):.2f} L/mÂ²")
    st.write(f"- **Maximum Drift Intensity:** {np.max(spray_drift):.2f} L/mÂ²")
    st.write(f"- **90% Cumulative Drift Distance:** {threshold_distance:.2f} m")
else:
    st.write("Adjust parameters and click **Run Simulation** in the sidebar to see results.")

if __name__ == "__main__":
    import os
    os.system(f"streamlit run {os.path.abspath(__file__)}")
