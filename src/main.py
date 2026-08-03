from data.clean_data import clean_data
from data.pull_data import pull_data
import pandas as pd


def main():
    seasons=[2022]
    
    all_clean_laps=[]
    
    for season in seasons:
        print("Pulling data from: ", season)

        raw_season_laps=pull_data(season)

        print("Cleaning data from: ", season)
        clean_season_data=clean_data(raw_season_laps)

        all_clean_laps.append(clean_season_data)


        
    
    final_data = pd.concat(all_clean_laps, ignore_index=True)
    #not be callign each time the laps
    final_data.to_csv(r'C:/Users/alren/Downloads/F1Prediction/data/cleaned/all_laps_2022.csv', index=False)
    print(f"Saved {len(final_data)} cleaned rows")
    print("Antes:", len(raw_season_laps))
    print("Después:", len(all_clean_laps))
    print("Eliminadas:", len(raw_season_laps) - len(final_data))






if __name__ == "__main__": 
    main()
