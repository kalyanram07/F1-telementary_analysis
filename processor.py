import numpy as np
import pandas as pd

def process_raw_telemetry(df):
    """Cleans, converts timestamps, and calculates distance traces from scratch."""
    if df is None or df.empty:
        return pd.DataFrame()

    # Deep copy to avoid SettingWithCopyWarning if it's a slice
    df = df.copy()

    # Convert ISO strings to datetime objects and sort sequentially
    df['date'] = pd.to_datetime(df['date'], format='ISO8601')
    df = df.sort_values('date').reset_index(drop=True)
    
    # Calculate time differentials (dt) in seconds between data points
    df['dt'] = df['date'].diff().dt.total_seconds().fillna(0)
    
    # Handle potentially missing 'speed' column gracefully
    if 'speed' not in df.columns:
        df['speed'] = 0
        
    # Convert Speed from km/h to m/s for calculus integration
    speed_mps = df['speed'] / 3.6
    
    # Mathematical integration: Distance = cumulative sum of (Speed * dt)
    df['distance'] = (speed_mps * df['dt']).cumsum()
    
    return df
