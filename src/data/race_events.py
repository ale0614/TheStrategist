import fastf1
import pandas as pd


def race_events(message):
    message = message.upper()
    if "STANDING START PROCEDURE" in message:
        return "RESTART_RACE"
    
    if "RED FLAG" == message:
            return "RED_FLAG"
    
    if "VIRTUAL SAFETY CAR DEPLOYED" in message:
            return "VIRTUAL_SAFETY_CAR"
    
    if "SAFETY CAR DEPLOYED" in message:
            return "SAFETY_CAR"
    else:
        return "OTHER"

# Find the moments a red flag ended
def find_red_flag_ends(track_status):
    rows = track_status.reset_index(drop=True)
    ends = []
    for i in range(len(rows) - 1):
        # a red flag ends when status is '5' and the next status is not '5'
        if rows.loc[i, 'Status'] == '5' and rows.loc[i + 1, 'Status'] != '5':
            ends.append(rows.loc[i + 1, 'Time'])
    return ends


# Mark each driver's first n laps after every red flag ends
def flag_red_flag_laps(laps, track_status, n_laps=2):
    laps = laps.copy()
    laps['AffectedByRedFlag'] = False

    for end in find_red_flag_ends(track_status):
        after = laps[laps['LapStartTime'] >= end]
        first_laps = after.sort_values('LapNumber').groupby('Driver').head(n_laps)
        laps.loc[first_laps.index, 'AffectedByRedFlag'] = True

    return laps

if __name__ == "__main__":
    #TEST
    import os
    fastf1.Cache.enable_cache(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'notebooks', 'cache'))
    session = fastf1.get_session(2024, "Japan", "R")
    session.load(laps=True, telemetry=False, weather=False, messages=True)

    laps=session.laps.copy()
    print( laps[laps['LapNumber'].isin([1, 2, 3, 4])][
            ["Driver", "LapNumber", "LapTime", "TrackStatus"]
        ].to_string(index=False)

    )

    # Race control messages can't be downloaded anymore (F1 archive needs login since Oct 2026)
    # Kept for reference; works only for races whose messages are already cached
    '''
    messages = session.race_control_messages.copy()
    #classify messages
    messages["EventType"] = messages["Message"].apply(race_events)

    #EventType
    events=messages[messages["EventType"]!='OTHER']

    print(events[["Lap", "Message", "EventType"]])

    print(
        laps[laps["LapNumber"].isin([2, 3, 4])][
            ["Driver", "LapNumber", "LapStartTime", "Time", "LapTime"]
        ].head(12).to_string(index=False)
    )

    print(
        events[
            ["Time", "Lap", "Message", "EventType"]
        ].to_string(index=False)
    )
    print("Session reference:", session.t0_date)
    # pick restart rows by their label, not by position
    restarts = events[events["EventType"] == "RESTART_RACE"].copy()
    # convert real clock time -> time since the session's zero point
    restarts["SessionTime"] = restarts["Time"] - session.t0_date
    print(restarts[["Time", "SessionTime", "Lap", "Message"]].to_string(index=False))
    '''

    # Track status IS cached: one row per flag change, Time is relative to session start
    status = session.track_status
    print(status.to_string(index=False))

    # Lap start/end times in the same units, to compare against the status changes
    print(
        laps[laps["LapNumber"].isin([1, 2, 3, 4]) & laps["Driver"].isin(["VER", "BOT"])][
            ["Driver", "LapNumber", "LapStartTime", "Time", "LapTime", "TrackStatus"]
        ].to_string(index=False)
    )
