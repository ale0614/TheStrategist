import fastf1
import pandas as pd
import numpy as np

# 1. Enable caching to speed up script runs
fastf1.Cache.enable_cache('f1_cache') 

def extract_race_features(year, location, driver_1, driver_2):
    print(f"Loading {year} {location} Grand Prix...")
    session = fastf1.get_session(year, location, 'R')
    session.load(telemetry=True, laps=True, weather=True)
    
    # 2. Extract Lap and Tire Data
    laps_d1 = session.laps.pick_driver(driver_1)
    laps_d2 = session.laps.pick_driver(driver_2)
    
    # Example feature engineering: Track evolution / Tire Age vs Lap Time
    features_d1 = laps_d1[['LapNumber', 'LapTime', 'Stint', 'Compound', 'TyreLife']].copy()
    
    # Convert LapTime Timedelta to floating seconds for your models
    features_d1['LapTime_s'] = features_d1['LapTime'].dt.total_seconds()
    
    # 3. Pull High-Frequency Telemetry from the fastest lap as a test
    fastest_telemetry = laps_d1.pick_fastest().get_telemetry()
    
    print(f"Successfully processed {len(features_d1)} laps for {driver_1}")
    return features_d1, fastest_telemetry

if __name__ == "__main__":
    # Test with a historical race
    d1_laps, telemetry = extract_race_features(2025, 'Silverstone', 'HAM', 'VER')
    print(d1_laps.head())