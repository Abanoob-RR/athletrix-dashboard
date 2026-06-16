import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. Page Configuration & Professional Dark Theme ---
st.set_page_config(page_title="VitaLink Analytics Pro", layout="wide")

st.markdown("""
    <style>
        [data-test-id='stAppViewContainer'], .main, .stApp { background-color: #070a0e !important; color: white !important; }
        [data-testid="stSidebar"] { background-color: #0b1016 !important; border-right: 1px solid #00f3ff33; }
        .metric-box {
            background: #111720; border: 1px solid #00f3ff22; border-radius: 12px;
            padding: 18px; text-align: center; box-shadow: 0 4px 15px rgba(0, 243, 255, 0.05); margin-bottom: 12px;
        }
        .metric-box-label { color: #8892b0; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
        .metric-box-value { color: #00f3ff; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px rgba(0, 243, 255, 0.4); }
        .panel-container { background: #111720; border: 1px solid #1f293d; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .panel-title {
            color: #00f3ff; font-weight: bold; font-size: 14px; margin-bottom: 15px;
            border-bottom: 1px solid #1f293d; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. Session State Management ---
if "global_history" not in st.session_state: st.session_state.global_history = {}
if "current_session_id" not in st.session_state: st.session_state.current_session_id = 1
if "session_start_time" not in st.session_state: st.session_state.session_start_time = time.time()
if "current_buffer" not in st.session_state: st.session_state.current_buffer = []

elapsed = time.time() - st.session_state.session_start_time
time_left = max(0, 180 - int(elapsed))

# High-fidelity live hardware simulation (تم تعديل النطاقات بناءً على طلبك)
live_hr = np.random.randint(70, 111)
live_spd = np.random.uniform(3, 6)  
live_mp = np.random.uniform(80, 250)
ax, ay, az = np.random.uniform(-3, 3), np.random.uniform(-3, 3), np.random.uniform(-3, 3)

st.session_state.current_buffer.append({
    "Timestamp": datetime.now().strftime("%H:%M:%S"),
    "HeartRate": live_hr, "Speed": live_spd, "MetabolicPower": live_mp,
    "AccX": ax, "AccY": ay, "AccZ": az
})

# Auto-Save Routine to CSV
if time_left <= 0:
    c_id = st.session_state.current_session_id
    df_to_save = pd.DataFrame(st.session_state.current_buffer)
    df_to_save.to_csv(f"VitaLink_Session_{c_id}.csv", index=False)
    st.session_state.global_history[f"Session #{c_id}"] = df_to_save
    st.session_state.current_session_id += 1
    st.session_state.session_start_time = time.time()
    st.session_state.current_buffer = []
    st.rerun()

# --- 3. Sidebar Panel ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f3ff; text-align:center;'>VITALINK PRO</h2>", unsafe_allow_html=True)
    weight = st.number_input("Weight (kg):", min_value=40, max_value=150, value=71)
    height = st.number_input("Height (cm):", min_value=120, max_value=220, value=167)
    body_fat = st.slider("Body Fat (%):", 4, 40, 12)
    st.write("---")
    mins, secs = divmod(time_left, 60)
    st.markdown(f"<div class='metric-box' style='border-color: #ff3b30;'><div class='metric-box-label' style='color:#ff3b30;'>Time Remaining (Session #{st.session_state.current_session_id})</div><div class='metric-box-value' style='color:#ff3b30;'>{mins:02d}:{secs:02d}</div></div>", unsafe_allow_html=True)
    st.write("---")
    options = ["Current Session (Live)"] + list(st.session_state.global_history.keys())
    selected_view = st.radio("Analytics Stream:", options)

# --- 4. Advanced Elite Sports Science Formulations ---
if selected_view == "Current Session (Live)":
    display_df = pd.DataFrame(st.session_state.current_buffer)
    is_live = True
else:
    display_df = st.session_state.global_history[selected_view]
    is_live = False

latest = display_df.iloc[-1] if not display_df.empty else {"HeartRate":0, "Speed":0, "MetabolicPower":0, "AccX":0, "AccY":0, "AccZ":0}
avg_hr = display_df["HeartRate"].mean() if not display_df.empty else 150
bmi = weight / ((height / 100) ** 2)
lean_mass = weight * (1 - (body_fat / 100))
fat_mass = weight * (body_fat / 100)

# TRIMP Load Calculation
hr_rest = 60
hr_max = 220 - 22  
hr_reserve = (avg_hr - hr_rest) / (hr_max - hr_rest) if (hr_max - hr_rest) > 0 else 0
trimp_score = (len(display_df) / 60) * hr_reserve * 0.64 * np.exp(1.92 * hr_reserve)

# RSI Calculation
total_acc = np.sqrt(latest['AccX']**2 + latest['AccY']**2 + latest['AccZ']**2)
rsi_index = total_acc / (latest['Speed'] + 1)

# Calories Exertion
calories_burned = (avg_hr * 0.444 + weight * 0.233 - 55.09) * (len(display_df)/60) if not display_df.empty else 0

# --- 5. Main Dashboard Layout ---
st.markdown("<h1 style='text-align: center; color: #00f3ff; margin-bottom:5px; font-size:32px; font-weight:bold;'>VITALINK ELITE PERFORMANCE HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #8892b0; margin-bottom:20px;'>System Status: <b style='color:#00f3ff;'>{selected_view}</b></p>", unsafe_allow_html=True)

# Row 1: Top Core KPI Metrics (5 Columns Grid)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.markdown(f"<div class='metric-box'><div class='metric-box-label'>❤️ Heart Rate</div><div class='metric-box-value'>{int(latest['HeartRate'])} BPM</div></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='metric-box'><div class='metric-box-label'>🏃‍♂️ Running Speed</div><div class='metric-box-value'>{latest['Speed']:.1f} km/h</div></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='metric-box'><div class='metric-box-label'>⚡ Metabolic Power</div><div class='metric-box-value'>{latest['MetabolicPower']:.1f} W</div></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='metric-box'><div class='metric-box-label'>📈 TRIMP (Load Score)</div><div class='metric-box-value'>{trimp_score:.1f} pts</div></div>", unsafe_allow_html=True)
with col5: st.markdown(f"<div class='metric-box'><div class='metric-box-label'>🔥 Metabolic Energy</div><div class='metric-box-value'>{calories_burned:.1f} Kcal</div></div>", unsafe_allow_html=True)

# Row 2: 3D Tracking & Cumulative Energy (50% / 50%)
m_col1, m_col2 = st.columns(2)
with m_col1:
    st.markdown("<div class='panel-container'><div class='panel-title'>📊 3D Spatial Trajectory (Kinematic Mapping)</div>", unsafe_allow_html=True)
    fig_3d = go.Figure()
    if len(display_df) > 1:
        fig_3d.add_trace(go.Scatter3d(x=display_df["AccX"], y=display_df["AccY"], z=display_df["AccZ"], mode='lines+markers', line=dict(color='#00f3ff', width=4), marker=dict(size=2, color='#bd00ff')))
    fig_3d.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0,r=0,b=0,t=0))
    st.plotly_chart(fig_3d, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with m_col2:
    st.markdown("<div class='panel-container'><div class='panel-title'>📈 Cumulative Active Heat Exertion</div>", unsafe_allow_html=True)
    fig_area = go.Figure()
    if not display_df.empty:
        fig_area.add_trace(go.Scatter(x=display_df["Timestamp"], y=np.cumsum(display_df["HeartRate"]*0.005), fill='tozeroy', fillcolor='rgba(0, 243, 255, 0.1)', line=dict(color='#00f3ff', width=3)))
    fig_area.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0,r=0,b=0,t=0), showlegend=False)
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Row 3: Market-Competing Correlative Graphics (50% / 50%)
n_col1, n_col2 = st.columns(2)
with n_col1:
    st.markdown("<div class='panel-container'><div class='panel-title'>🔄 Cardiovascular Drift Analysis (HR vs Speed Trend)</div>", unsafe_allow_html=True)
    fig_corr = go.Figure()
    if not display_df.empty:
        fig_corr.add_trace(go.Scatter(x=display_df["Timestamp"], y=display_df["HeartRate"], name="HR (BPM)", line=dict(color='#ff3b30', width=3)))
        fig_corr.add_trace(go.Scatter(x=display_df["Timestamp"], y=display_df["Speed"] * 8, name="Speed Trend (Scaled)", line=dict(color='#00f3ff', width=2, dash='dash')))
    
    fig_corr.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        height=240,
        margin=dict(l=20, r=20, b=20, t=20),
        xaxis=dict(title="Time Line"),
        yaxis=dict(title="Metrics Analytics Level"),
        showlegend=True
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with n_col2:
    st.markdown("<div class='panel-container'><div class='panel-title'>🧭 Acceleration vs Deceleration Balance (Injury Risk Polar)</div>", unsafe_allow_html=True)
    fig_polar = go.Figure()
    if not display_df.empty:
        fig_polar.add_trace(go.Scatterpolar(r=[latest['Speed'], total_acc, latest['MetabolicPower']/10, rsi_index*10], theta=['Speed', 'Acceleration', 'Metabolic Load', 'RSI Index'], fill='toself', line_color='#bd00ff'))
    fig_polar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=240, margin=dict(l=20,r=20,b=20,t=20))
    st.plotly_chart(fig_polar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Row 4: Symmetrical Deep Diagnostics Section (4 Columns Grid)
d_col1, d_col2, d_col3, d_col4 = st.columns(4)
with d_col1:
    st.markdown("<div class='panel-container'><div class='panel-title'>🥩 Body Tissues</div>", unsafe_allow_html=True)
    fig_donut = go.Figure(data=[go.Pie(labels=['Lean', 'Fat'], values=[lean_mass, fat_mass], hole=.5, marker=dict(colors=['#00f3ff', '#bd00ff']))])
    fig_donut.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=190, showlegend=False, margin=dict(l=5,r=5,b=5,t=5))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with d_col2:
    st.markdown("<div class='panel-container'><div class='panel-title'>🎯 Intensity Zones</div>", unsafe_allow_html=True)
    z1, z2, z3 = len(display_df[display_df["HeartRate"] < 145])+1, len(display_df[(display_df["HeartRate"] >= 145) & (display_df["HeartRate"] < 165)])+1, len(display_df[display_df["HeartRate"] >= 165])+1
    fig_pie = go.Figure(data=[go.Pie(labels=['Z1', 'Z2', 'Z3'], values=[z1, z2, z3], marker=dict(colors=['#00bfff', '#00f3ff', '#ff3b30']))])
    fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=190, showlegend=False, margin=dict(l=5,r=5,b=5,t=5))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with d_col3:
    st.markdown("<div class='panel-container'><div class='panel-title'>⚙️ Kinetic Efficiency</div>", unsafe_allow_html=True)
    # تم تعديل حدود المؤشر لتتوافق مع رينج (55 - 95) الخاص بك
    eff_value = min(95, int((latest['Speed'] / (latest['MetabolicPower'] + 1)) * 1200)) if latest['MetabolicPower'] > 0 else 0
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=eff_value, gauge={'axis': {'range': [75, 95]}, 'bar': {'color': "#00f3ff"}, 'bgcolor': "#111720"}))
    fig_gauge.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=190, margin=dict(l=20,r=20,b=10,t=10))
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with d_col4:
    st.markdown("<div class='panel-container'><div class='panel-title'>⚠️ Fatigue Index</div>", unsafe_allow_html=True)
    # تم تعديل حدود المؤشر لتتوافق مع رينج (40 - 95) الخاص بك
    fatigue_index = min(95, int((avg_hr / hr_max) * 100)) if hr_max > 0 else 0
    fig_fatigue = go.Figure(go.Indicator(mode="gauge+number", value=fatigue_index, gauge={'axis': {'range': [5, 25]}, 'bar': {'color': "#ff3b30"}, 'bgcolor': "#111720"}))
    fig_fatigue.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=190, margin=dict(l=20,r=20,b=10,t=10))
    st.plotly_chart(fig_fatigue, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if is_live:
    time.sleep(3)
    st.rerun()
