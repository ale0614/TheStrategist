from data.clean_data import clean_data
from data.pull_data import pull_data, PROJECT_ROOT
import pandas as pd
import os


def main():
    seasons=[2022, 2023, 2024]
    
    all_clean_laps=[]
    total_raw_rows = 0
    total_clean_rows = 0
    
    for season in seasons:
        print("Pulling data from: ", season)

        raw_season_laps=pull_data(season)

        print("Cleaning data from: ", season)
        clean_season_data=clean_data(raw_season_laps)

        print("Before:", len(raw_season_laps))
        print("After:", len(clean_season_data))
        print("Removed:", len(raw_season_laps) - len(clean_season_data))
        print()

        total_raw_rows += len(raw_season_laps)
        total_clean_rows += len(clean_season_data)

        all_clean_laps.append(clean_season_data)
    
    final_data = pd.concat(all_clean_laps, ignore_index=True)
    #not be callign each time the laps
    output_dir = os.path.join(PROJECT_ROOT, 'data', 'cleaned')
    os.makedirs(output_dir, exist_ok=True)
    final_data.to_csv(os.path.join(output_dir, 'all_laps_2022_2023_2024.csv'), index=False)
    print("FINAL SUMMARY")
    print("Total raw rows:", total_raw_rows)
    print("Total cleaned rows:", total_clean_rows)
    print("Total removed:", total_raw_rows - total_clean_rows)
    print("Saved:", len(final_data), "cleaned rows")







if __name__ == "__main__": 
    main()
