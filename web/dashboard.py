import streamlit as st
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time
from datetime import datetime

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="🚀 HackShield Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("Controls")
theme_choice = st.sidebar.radio("Select Theme", ["Light", "Dark"])
update_interval = st.sidebar.slider("Auto-refresh Interval (seconds)", 1, 10, 5)

# ----------------------------
# Theme
# ----------------------------
if theme_choice == "Dark":
    plt.style.use('dark_background')
else:
    plt.style.use('default')

# ----------------------------
# System Stats Function
# ----------------------------
def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    memory_percent = mem.percent
    return cpu_percent, memory_percent

# ----------------------------
# Module Status
# ----------------------------
# Replace with actual project modules
modules = pd.DataFrame({
    "Module": ["Module A", "Module B", "Module C", "Module D"],
    "Status": ["Running", "Idle", "Error", "Running"],
    "Load (%)": [45, 12, 90, 60]
})

# ----------------------------
# Alerts Log
# ----------------------------
ALERT_LOG_FILE = "alerts_log.csv"

def log_alert(module_name, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([[now, module_name, message]], columns=["Timestamp", "Module", "Alert"])
    try:
        existing = pd.read_csv(ALERT_LOG_FILE)
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(ALERT_LOG_FILE, index=False)

# ----------------------------
# Main Dashboard Loop
# ----------------------------
placeholder = st.empty()

while True:
    cpu_percent, memory_percent = get_system_stats()
    
    with placeholder.container():
        st.title("🚀 HackShield Dashboard")
        
        # System Metrics
        st.subheader("System Metrics")
        col1, col2 = st.columns(2)
        col1.metric("CPU Usage (%)", f"{cpu_percent}%")
        col2.metric("Memory Usage (%)", f"{memory_percent}%")
        
        # Module Status
        st.subheader("Module Status Table")
        st.dataframe(modules)
        
        # Alerts & Solutions
        st.subheader("Alerts & Solutions")
        alerts = modules[modules["Status"] == "Error"]
        if not alerts.empty:
            for idx, row in alerts.iterrows():
                st.error(f"⚠ {row['Module']} is in ERROR state!")
                st.info("💡 Suggested Solution: Restart the module or check logs.")
                log_alert(row["Module"], "Error detected")
        else:
            st.success("✅ No errors detected.")
        
        # Load Charts
        st.subheader("Module Load Chart (Interactive)")
        fig = px.bar(modules, x="Module", y="Load (%)", color="Status", text="Load (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    time.sleep(update_interval)
