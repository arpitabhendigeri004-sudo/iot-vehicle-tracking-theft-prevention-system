import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import os
import math

# Optional PDF Report Import
try:
    from reports.pdf_report import generate_report
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="IoT Vehicle Tracking & Theft Prevention",
    page_icon="🚗",
    layout="wide"
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🚗 Control Panel")

refresh_rate = st.sidebar.slider(
    "Refresh Rate (Seconds)",
    1,
    30,
    5
)

safe_radius = st.sidebar.slider(
    "Geofence Radius (Meters)",
    100,
    1000,
    500
)

st.sidebar.markdown("---")

st.sidebar.success("System Status: Online")

# ==================================================
# AUTO REFRESH
# ==================================================

st_autorefresh(
    interval=refresh_rate * 1000,
    key="vehicle_refresh"
)

# ==================================================
# LOAD DATA
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

csv_file = os.path.join(
    BASE_DIR,
    "data",
    "vehicle_data.csv"
)

try:
    df = pd.read_csv(csv_file)

    if len(df) == 0:
        st.warning("No vehicle data available.")
        st.stop()

except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# ==================================================
# LATEST RECORD
# ==================================================

latest = df.iloc[-1]

lat = float(latest["latitude"])
lon = float(latest["longitude"])
speed = float(latest["speed"])
status = str(latest["status"])
alert = str(latest["alert"])

# ==================================================
# GEOFENCE CALCULATION
# ==================================================

SAFE_LAT = 12.9716
SAFE_LON = 77.5946

distance = math.sqrt(
    ((lat - SAFE_LAT) ** 2)
    +
    ((lon - SAFE_LON) ** 2)
)

radius_degree = safe_radius / 111000

theft_detected = distance > radius_degree

# ==================================================
# HEADER
# ==================================================

st.title("🚗 IoT Vehicle Tracking & Theft Prevention System")

st.markdown(
    "### Real-Time GPS Monitoring | Geofence Security | Theft Prevention"
)

st.markdown("---")

# ==================================================
# ALERT PANEL
# ==================================================

if theft_detected:

    st.markdown(
        """
        <div style="
        background:red;
        color:white;
        padding:20px;
        border-radius:10px;
        text-align:center;
        font-size:28px;
        font-weight:bold;">
        🚨 VEHICLE THEFT ALERT 🚨
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.success("✅ Vehicle Inside Safe Zone")

# ==================================================
# KPI CARDS
# ==================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📍 Latitude",
    f"{lat:.6f}"
)

c2.metric(
    "📍 Longitude",
    f"{lon:.6f}"
)

c3.metric(
    "🏎 Speed",
    f"{speed:.2f} km/h"
)

c4.metric(
    "🛡 Security",
    "ALERT" if theft_detected else "SAFE"
)

# ==================================================
# MAP + GAUGE
# ==================================================

left, right = st.columns([2, 1])

with left:

    st.subheader("📍 Live Vehicle Location")

    vehicle_map = folium.Map(
        location=[lat, lon],
        zoom_start=15
    )

    folium.Marker(
        [lat, lon],
        popup="Vehicle Location",
        tooltip="Vehicle"
    ).add_to(vehicle_map)

    folium.Circle(
        radius=safe_radius,
        location=[SAFE_LAT, SAFE_LON],
        color="green",
        fill=True,
        fill_opacity=0.2
    ).add_to(vehicle_map)

    st_folium(
        vehicle_map,
        width=900,
        height=500
    )

with right:

    st.subheader("🏎 Speed Gauge")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,
            title={"text": "Speed (km/h)"},
            gauge={
                "axis": {"range": [0, 120]}
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

# ==================================================
# ROUTE HISTORY
# ==================================================

st.markdown("---")

st.subheader("🛰 Vehicle Route History")

route_map = folium.Map(
    location=[lat, lon],
    zoom_start=14
)

route_points = list(
    zip(
        df["latitude"],
        df["longitude"]
    )
)

if len(route_points) > 1:

    folium.PolyLine(
        route_points,
        color="blue",
        weight=5
    ).add_to(route_map)

folium.Marker(
    route_points[-1],
    tooltip="Current Position"
).add_to(route_map)

st_folium(
    route_map,
    width=1200,
    height=500
)

# ==================================================
# SPEED TREND
# ==================================================

st.markdown("---")

st.subheader("📈 Vehicle Speed Trend")

speed_chart = px.line(
    df.tail(100),
    y="speed",
    title="Speed Trend"
)

st.plotly_chart(
    speed_chart,
    use_container_width=True
)

# ==================================================
# SECURITY ANALYTICS
# ==================================================

st.subheader("🛡 Security Analytics")

a, b, c = st.columns(3)

a.metric(
    "Distance From Safe Zone",
    f"{distance:.5f}"
)

b.metric(
    "Total Records",
    len(df)
)

c.metric(
    "Theft Events",
    len(df[df["alert"] == "THEFT ALERT"])
)

# ==================================================
# FLEET ANALYTICS
# ==================================================

st.subheader("📊 Fleet Analytics")

avg_speed = df["speed"].mean()
max_speed = df["speed"].max()
min_speed = df["speed"].min()

f1, f2, f3 = st.columns(3)

f1.metric(
    "Average Speed",
    f"{avg_speed:.2f} km/h"
)

f2.metric(
    "Maximum Speed",
    f"{max_speed:.2f} km/h"
)

f3.metric(
    "Minimum Speed",
    f"{min_speed:.2f} km/h"
)

# ==================================================
# STATUS PIE CHART
# ==================================================

st.subheader("🚘 Vehicle Status Distribution")

status_counts = df["status"].value_counts()

pie = px.pie(
    values=status_counts.values,
    names=status_counts.index
)

st.plotly_chart(
    pie,
    use_container_width=True
)

# ==================================================
# SPEED HISTOGRAM
# ==================================================

st.subheader("📊 Speed Distribution")

hist = px.histogram(
    df,
    x="speed",
    nbins=20,
    title="Speed Frequency Analysis"
)

st.plotly_chart(
    hist,
    use_container_width=True
)

# ==================================================
# RECENT ALERTS
# ==================================================

st.subheader("🚨 Recent Alerts")

alerts_df = df[
    df["alert"] != "Normal"
]

if len(alerts_df) > 0:

    st.dataframe(
        alerts_df.tail(10),
        use_container_width=True
    )

else:

    st.success(
        "No security alerts detected."
    )

# ==================================================
# GOOGLE MAPS LINK
# ==================================================

maps_url = f"https://www.google.com/maps?q={lat},{lon}"

st.markdown(
    f"### 🌍 [Open Vehicle Location in Google Maps]({maps_url})"
)

# ==================================================
# SYSTEM OVERVIEW
# ==================================================

st.subheader("📋 System Overview")

overview = {
    "Total Records": len(df),
    "Average Speed": round(avg_speed, 2),
    "Maximum Speed": round(max_speed, 2),
    "Minimum Speed": round(min_speed, 2),
    "Security Events": len(
        df[df["alert"] == "THEFT ALERT"]
    )
}

st.json(overview)

# ==================================================
# VEHICLE LOGS
# ==================================================

st.subheader("📜 Vehicle Logs")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

# ==================================================
# PDF REPORT
# ==================================================

if PDF_AVAILABLE:

    if st.button("📄 Generate PDF Report"):

        generate_report(csv_file)

        st.success(
            "PDF Report Generated Successfully"
        )

# ==================================================
# DOWNLOAD LOGS
# ==================================================

csv_download = df.to_csv(index=False)

st.download_button(
    "⬇ Download Vehicle Logs",
    csv_download,
    "vehicle_logs.csv",
    "text/csv"
)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IoT Vehicle Tracking & Theft Prevention System | ESP32 + GPS + Streamlit Simulation"
)