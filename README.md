# F1 Telemetry Stream Engine 🏎️

This is a custom-built, purely standard Python pipeline for extracting, synchronizing, and visualizing F1 live telemetry data natively from the [OpenF1 API](https://openf1.org).

## 🚀 Features
- **Built from Scratch**: No `fastf1` overhead. Fully reliant on `requests`, `pandas`, `numpy`, and `streamlit`.
- **Custom Mathematical Integration**: Translates temporal data (time) into spatial distance using cumulative NumPy arrays for accurate side-by-side spatial overlays of two drivers.
- **Interactive UI**: View side-by-side Speed and Throttle deployment mapping arrays using `plotly`.

## ⚙️ Setup & Execution

1. Install requirements:
   ```bash
   pip install pandas numpy plotly requests streamlit
   ```

2. Boot the Dashboard Server:
   ```bash
   streamlit run app.py
   ```

## 🏎️ How to find Data: OpenF1 Session & Driver Keys

To use the dashboard, you must enter valid OpenF1 Session Keys and Driver Numbers.

### ✅ Valid 2024 Session Keys
You can search the full list natively via: `https://api.openf1.org/v1/sessions?year=2024&session_type=Race`

**Popular 2024 Races:**
* `9472` — Bahrain Grand Prix
* `9480` — Saudi Arabian Grand Prix
* `9488` — Australian Grand Prix
* `9496` — Japanese Grand Prix
* `9523` — Monaco Grand Prix
* `9566` — Hungarian Grand Prix
* `9574` — Belgian Grand Prix (Spa)

### 🏎️ Driver / Car Numbers
Driver numbers belong natively to the drivers themselves. You can list drivers via: `https://api.openf1.org/v1/drivers?session_key=...`

**Top Grid Drivers:**
* `1` — Max Verstappen (Red Bull)
* `11` — Sergio Perez (Red Bull)
* `16` — Charles Leclerc (Ferrari)
* `55` — Carlos Sainz (Ferrari)
* `4` — Lando Norris (McLaren)
* `81` — Oscar Piastri (McLaren)
* `44` — Lewis Hamilton (Mercedes)
* `63` — George Russell (Mercedes)
* `14` — Fernando Alonso (Aston Martin)
