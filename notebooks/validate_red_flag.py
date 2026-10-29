import sys
import fastf1
import pandas as pd

# Reuse the real clean_data so we compare against exactly what the model trains on
sys.path.insert(0, r'C:/Users/alren/Downloads/F1Prediction/src/data')
from clean_data import clean_data
from race_events import find_red_flag_ends
from race_events import flag_red_flag_laps

fastf1.Cache.enable_cache(r'C:/Users/alren/Downloads/F1Prediction/notebooks/cache')
fastf1.set_log_level('ERROR')



# Compare clean_data alone vs clean_data + rule for one race
def validate(year, event):
    session = fastf1.get_session(year, event, 'R')
    session.load(laps=True, telemetry=False, weather=False, messages=False)
    raw = pd.DataFrame(session.laps)

    print('\n' + '=' * 70)
    print(year, event)
    print('Red flag ended at:', [str(t) for t in find_red_flag_ends(session.track_status)])

    flagged = flag_red_flag_laps(raw, session.track_status)
    cleaned = clean_data(flagged)  # original cleaning, untouched; the new column rides along

    newly_removed = cleaned[cleaned['AffectedByRedFlag']].copy()
    kept = cleaned[~cleaned['AffectedByRedFlag']]

    print('Raw laps:', len(raw))
    print('Kept by clean_data only:', len(cleaned))
    print('Flagged by rule (total):', flagged['AffectedByRedFlag'].sum(),
          '| already removed by clean_data:', flagged['AffectedByRedFlag'].sum() - len(newly_removed),
          '| NEWLY removed:', len(newly_removed))

    if len(newly_removed) == 0:
        return newly_removed

    # Is a removed lap really abnormal? Compare it to that driver's typical (median) clean lap
    median = kept.groupby('Driver')['LapTimeSeconds'].median()
    newly_removed['DriverMedian'] = newly_removed['Driver'].map(median)
    newly_removed['PctSlower'] = (newly_removed['LapTimeSeconds'] / newly_removed['DriverMedian'] - 1) * 100
    newly_removed['LooksNormal'] = newly_removed['PctSlower'] < 5

    print(newly_removed[['Driver', 'LapNumber', 'LapTimeSeconds', 'DriverMedian', 'PctSlower', 'LooksNormal']]
          .sort_values(['LapNumber', 'Driver']).round(1).to_string(index=False))
    return newly_removed


if __name__ == '__main__':
    races = [
        (2024, 'Japanese Grand Prix'),
        (2022, 'Monaco Grand Prix'),
        (2022, 'British Grand Prix'),
        (2022, 'Japanese Grand Prix'),
        (2023, 'Australian Grand Prix'),
        (2023, 'Dutch Grand Prix'),
        (2023, 'Mexico City Grand Prix'),
        (2023, 'São Paulo Grand Prix'),
        (2024, 'Monaco Grand Prix'),
        (2024, 'São Paulo Grand Prix'),
    ]
    for year, event in races:
        validate(year, event)
