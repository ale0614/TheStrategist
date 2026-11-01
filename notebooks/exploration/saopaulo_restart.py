import fastf1
import pandas as pd

session= fastf1.get_session(2024,'São Paulo','R')

session.load()
laps=session.laps
saopaulo=laps[laps['LapNumber'].between(1,5)]
messages = session.race_control_messages

pd.set_option('display.max_rows', None)

print(messages.to_string(index=False))

columns = [
    'Driver',
    'LapNumber',
    'Stint',
    'LapTime',
    'TrackStatus',
    'PitInTime',
    'PitOutTime'
]
standing_starts = messages[
    messages["Message"].str.contains(
        "STANDING START PROCEDURE",
        case=False,
        na=False
    )
]

print("\nSTANDING RESTART MESSAGES:")
print(standing_starts[["Time", "Message", "Lap"]].to_string(index=False))

'''
print(suzuka[columns].sort_values(
    ['Driver', 'LapNumber']
).to_string(index=False))

print("\nSUZUKA LAP 3 ACCURACY:")

print(
    laps[
        (laps['LapNumber'] == 3) &
        (laps['Driver'].isin(['BOT', 'OCO', 'GAS', 'STR']))
    ][['Driver', 'LapTime', 'TrackStatus', 'IsAccurate']]
)
print("\nACCURACY COUNTS:")
inaccurate = laps[laps['IsAccurate'] == False]

print(
    inaccurate['LapNumber']
    .value_counts()
    .sort_index()
)'''