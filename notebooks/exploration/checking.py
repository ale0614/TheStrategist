
#session.load()
#ssion.load(laps=True, telemetry=True, weather=True, messages=False)

#print(session.laps.head())
#print(dir(session))
#print(session.results[['Position', 'Abbreviation', 'FullName']])
#print(session.weather_data.head)

#lec=session.laps.pick_driver('LEC')
#ver = session.laps.pick_driver('VER')
#sai=session.laps.pick_driver('SAI')
#ant=session.laps.pick_driver('ANT')
#print(lec[['LapNumber', 'LapTime']].head())
#print(session.date)              
#print(ant[['LapNumber', 'LapTime']].head())
import fastf1

fastf1.Cache.enable_cache('cache')
session = fastf1.get_session(2024, 'Monaco', 'R')
session.load(laps=True, telemetry=False, weather=False, messages=False)

laps = session.laps
print(laps[['Driver', 'LapNumber', 'LapTime', 'Compound', 'TyreLife', 'Stint', 'TrackStatus']].head(20))