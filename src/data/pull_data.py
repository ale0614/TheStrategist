import fastf1
import pandas as pd
import os
from data.race_events import flag_red_flag_laps

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cache_path = os.path.join(PROJECT_ROOT, 'notebooks', 'cache')
os.makedirs(cache_path, exist_ok=True)
fastf1.Cache.enable_cache(cache_path)


def pull_data(season):
    schedule = fastf1.get_event_schedule(season)
    schedule = schedule[schedule['RoundNumber'] > 0]
    schedule = schedule[schedule['F1ApiSupport'] == True]
    
    race_laps=[]
    for index, race in schedule.iterrows():
        try:
            session = fastf1.get_session(season, race['EventName'], 'R')
            session.load(laps=True, telemetry=False, weather=False, messages=False)
            laps = pd.DataFrame(session.laps)
            laps=flag_red_flag_laps(laps,session.track_status)
            laps['Season'] = season
            laps['EventName'] = race['EventName']
            laps['RoundNumber'] = race['RoundNumber']
            laps['Location'] = race['Location']
            race_laps.append(laps)
            print(f"{season} {race['EventName']}")

        except Exception as e:
            print(f"Skipped {race['EventName']}: {e}")
            import traceback
            traceback.print_exc()

    return pd.concat(race_laps,ignore_index=True)


'''schedule = fastf1.get_event_schedule(2024)
print(schedule.columns.tolist())  # see all available columns
print(schedule.head())  '''
