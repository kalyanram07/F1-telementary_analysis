import requests
import pandas as pd

BASE_URL = "https://api.openf1.org/v1"

def _fetch_with_validation(url):
    """Fetches URL with a requests session, checking status and edge cases."""
    with requests.Session() as session:
        response = session.get(url, timeout=15)
        if response.status_code == 404:
            raise ValueError("Data not found (HTTP 404). Please verify the Session Key and Driver Numbers.")
        if response.status_code == 429:
            raise ConnectionError("HTTP 429: Rate limit exceeded for OpenF1 API.")
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return None
        return data

def fetch_fastest_lap(session_key, driver_number):
    """Fetches the timing details of a driver's fastest lap in a session."""
    url = f"{BASE_URL}/laps?session_key={session_key}&driver_number={driver_number}"
    data = _fetch_with_validation(url)
    
    if not data:
        raise ValueError(f"No lap data found for driver {driver_number} in session {session_key}.")
        
    df = pd.DataFrame(data)
    if 'lap_duration' not in df.columns:
        raise ValueError(f"Invalid payload format: 'lap_duration' missing for driver {driver_number}.")
        
    # Filter out out-laps/in-laps (null durations) and find min
    valid_laps = df[df['lap_duration'].notna()]
    if valid_laps.empty:
        raise ValueError(f"No valid timed laps found for driver {driver_number}.")
        
    fastest = valid_laps.loc[valid_laps['lap_duration'].idxmin()]
    return fastest

def fetch_raw_telemetry(session_key, driver_number, start_time, end_time):
    """Pulls the high-frequency telemetry data streams between two timestamps."""
    url = (f"{BASE_URL}/car_data?session_key={session_key}&driver_number={driver_number}"
           f"&date>={start_time}&date<={end_time}")
    data = _fetch_with_validation(url)
    
    if not data:
        return pd.DataFrame()
        
    return pd.DataFrame(data)
