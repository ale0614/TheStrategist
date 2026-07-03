import fastf1
import pandas as pd


session= fastf1.get_session(2024,"Monaco", "R")
#load into pandas dataframe organization
session.load()
df=pd.DataFrame(session.laps)
'''Print all the information it has
pd.set_option('display.max_columns', None)
print(df.head())
'''

#Preparing data for use
def clean_data(df):
    laps=df.copy()

    
    laps["LapTimeSeconds"]= laps["LapTime"].dt.total_seconds()

    laps= laps.dropna(subset=["LapTimeSeconds"])

    #Use only laps that have a green flag and arent pit stop lap before and after
    laps=laps[laps["TrackStatus"]=='1']
    laps=laps[laps["PitInTime"].isna() & laps["PitOutTime"].isna()]
    #if column missing
    laps=laps.dropna(subset=["LapTime", "TyreLife", "Stint", "Driver", "Compound"])
    print(len(laps)) 

    return laps

clean_data=clean_data(df)


