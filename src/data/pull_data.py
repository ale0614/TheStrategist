import fastf1
import pandas as pd
import os

cache_path = r'C:/Users/alren/Downloads/F1Prediction/notebooks/cache'
print(os.path.exists(cache_path))  # should print True
fastf1.Cache.enable_cache(cache_path)


def pull_data(season):
    schedule = fastf1.get_event_schedule(season)
    schedule = schedule[schedule['RoundNumber'] > 0]
    schedule = schedule[schedule['F1ApiSupport'] == True]
    
    race_laps=[]
    for index, race in schedule.iterrows():
        try:
            session = fastf1.get_session(season, race['EventName'], 'R')
            session.load(laps=True, telemetry=False, weather=False, messages=True)
            laps = pd.DataFrame(session.laps)
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
