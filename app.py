import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from client import fetch_fastest_lap, fetch_raw_telemetry
from processor import process_raw_telemetry

st.set_page_config(layout="wide", page_title="F1 Telemetry Engine")
st.title("🏎️ Custom F1 Telemetry Stream Engine (Built From Scratch)")

st.sidebar.header("Data Stream Target")
session_key = st.sidebar.text_input("OpenF1 Session Key", "9159")
driver1 = st.sidebar.text_input("Driver 1 Car Number", "1")
driver2 = st.sidebar.text_input("Driver 2 Car Number", "16")

if st.sidebar.button("Stream & Process Data"):
    with st.spinner("Streaming raw data packets from OpenF1 API..."):
        try:
            # 1. Fetch lap boundaries
            lap1 = fetch_fastest_lap(session_key, driver1)
            lap2 = fetch_fastest_lap(session_key, driver2)
            
            # 2. Extract telemetry within those boundaries
            raw_tel1 = fetch_raw_telemetry(session_key, driver1, lap1['date_start_iso'], lap1['date_end_iso'])
            raw_tel2 = fetch_raw_telemetry(session_key, driver2, lap2['date_start_iso'], lap2['date_end_iso'])
            
            # 3. Process data traces through custom math engine
            tel1 = process_raw_telemetry(raw_tel1)
            tel2 = process_raw_telemetry(raw_tel2)
            
            if tel1.empty or tel2.empty:
                st.error("One or both telemetry streams returned empty data. Check session key or driver numbers.")
            else:
                # 4. Render Telemetry Graph Maps
                fig = make_subplots(
                    rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.08,
                    subplot_titles=("Speed Profile (km/h)", "Throttle Deployment %")
                )
                
                # Speed Traces
                fig.add_trace(go.Scatter(x=tel1['distance'], y=tel1.get('speed', []), name=f"Car {driver1}", line=dict(color='#1A73E8')), row=1, col=1)
                fig.add_trace(go.Scatter(x=tel2['distance'], y=tel2.get('speed', []), name=f"Car {driver2}", line=dict(color='#E52521')), row=1, col=1)
                
                # Throttle Traces
                fig.add_trace(go.Scatter(x=tel1['distance'], y=tel1.get('throttle', []), showlegend=False, line=dict(color='#1A73E8')), row=2, col=1)
                fig.add_trace(go.Scatter(x=tel2['distance'], y=tel2.get('throttle', []), showlegend=False, line=dict(color='#E52521')), row=2, col=1)
                
                fig.update_layout(height=650, title_text="Distance-Based Telemetry Analytics Engine", hovermode="x unified")
                fig.update_xaxes(title_text="Distance (m)", row=2, col=1)
                fig.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
                fig.update_yaxes(title_text="Throttle %", row=2, col=1)
                
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Data stream pipeline execution aborted: {str(e)}")
