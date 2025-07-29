import pandas as pd
import numpy as np
from datetime import datetime,timedelta

# data={
#     'Speed':[76,9.5,'N/A',np.nan,'','',24,None,''],
#     'Steering Torque':[-34,2.7,'','','N/A',77,66,2.7,'N/A'],

# }
# df = pd.DataFrame(data)
# df_steering = df.copy()
# df_steering['Steering Torqe']=pd.to_numeric(df['Steering Torque'],errors='coerce')
# print(df_steering)

#methods for org
# 1) dropna()
# removes the rows and columns with Nan Values
    
#     axis=0 for rows and axis=1 for columns
#     how='any' or 'all'
#     thresh=minimum number of values too Look
#     subset = Only columns
# df_na = df.copy()
# df_na.dropna(how='any')

# #drop all rows with nan {even if it has 1 nan in the frame it drops that row}
# df_na.dropna(how='all')
# df_na.dropna(thresh=3)
# df_na.dropna(subset='Speed')

#only consider speed column while dropping

# Homework During the 20 seconds leading up to crash/collision, Autonomous Driving State was in an active state at some point.


df_car = pd.read_excel(r"D:\Projects\Veracity Software Inc\cardata_814 1 (3) (1).xlsx")
df_car_c = df_car.copy()
df_car_c["DATE (UTC)"] = pd.to_datetime(df_car_c["DATE (UTC)"])

ADS_cols_to_fill = [col for col in df_car_c.columns if col.startswith('Autonomous Driving State')]
df_car_c[ADS_cols_to_fill] = df_car_c[ADS_cols_to_fill].ffill().bfill()

crash_columns = [col for col in df_car_c.columns if col.startswith('Crash Type')]

left_side_mask = (df_car_c[crash_columns] == 'Left-Side Collision').any(axis=1)
left_side_crashes = df_car_c[left_side_mask]['DATE (UTC)']

adas_active_states = ['Autosteer', 'Cruise Control Active', 'Full Self-Driving', 'Autopilot']

for crash_time in left_side_crashes:
    window_start = crash_time - pd.Timedelta(seconds=20)
    window_data = df_car_c[(df_car_c['DATE (UTC)'] >= window_start) & (df_car_c['DATE (UTC)'] <= crash_time)]
    
    # VECTORIZED: Check which rows have active ADS states
    ads_active_mask = window_data[ADS_cols_to_fill].isin(adas_active_states).any(axis=1)
    active_rows = window_data[ads_active_mask]
    
    print(f"Crash at {crash_time}:")
    
    if not active_rows.empty:
        print("ADS ACTIVE during 20-second window:")
        for idx in active_rows.index:
            timestamp = active_rows.loc[idx, 'DATE (UTC)']
            # Find which ADS column was active
            for col in ADS_cols_to_fill:
                if active_rows.loc[idx, col] in adas_active_states:
                    print(f"  {timestamp} - {active_rows.loc[idx, col]}")
                    break
    else:
        print("ADS NOT ACTIVE during 20-second window")
        outside_window = df_car_c[(df_car_c['DATE (UTC)'] < window_start) | (df_car_c['DATE (UTC)'] > crash_time)]
        
        # VECTORIZED: Find active ADS outside window
        outside_ads_mask = outside_window[ADS_cols_to_fill].isin(adas_active_states).any(axis=1)
        outside_active = outside_window[outside_ads_mask]
        
        if not outside_active.empty:
            print("ADS active outside 20-second window:")
            count = 0
            for idx in outside_active.index:
                if count >= 3:
                    break
                timestamp = outside_active.loc[idx, 'DATE (UTC)']
                for col in ADS_cols_to_fill:
                    if outside_active.loc[idx, col] in adas_active_states:
                        print(f"  {timestamp} - {outside_active.loc[idx, col]}")
                        count += 1
                        break
        else:
            print("No ADS activity found in dataset")
    print()


#print(f"Autonomous Driving State was in an active state during the 20 seconds leading up to crash/collision" , crash_flags)

#During the 10 seconds preceding the crash, collision, Vehicle Speed exceeds 75 mph.

df_car_c['Vehicle_speed'] = df_car_c['Vehicle Speed'].ffill().bfill()

for crash_time in left_side_crashes:
    window_start_v = crash_time-timedelta(seconds=10)
    window_data_v = df_car_c[(df_car_c['DATE (UTC)']>=window_start_v) & (df_car_c['DATE (UTC)']<=crash_time)]

    overspeed_mask = window_data_v['Vehicle Speed']>75
    overspeed_rows = window_data_v[overspeed_mask]

    if not overspeed_rows.empty:
        print("Vehicle speed greater than 75mph")
        for idx in overspeed_rows.index:
            overspeed_timestamps = overspeed_rows.loc[idx, 'DATE (UTC)'] 
            speed_value = overspeed_rows.loc[idx,'Vehicle Speed']
            print(f"{overspeed_timestamps} - {speed_value}")
            

    else:
        print("speed not exceeding  75mph")


    
# #During the 10 seconds preceding the crash/collision,  Steering Torque exceeds +/- 3

for crash_time in left_side_crashes:
    window_start_t = crash_time-timedelta(seconds=10)
    window_data_t = df_car_c[(df_car_c['DATE (UTC)']>=window_start_t) & (df_car_c['DATE (UTC)']<=crash_time)]
    
    torque_mask = (window_data_t['Steering Torque'] > 3.0) | (window_data_t['Steering Torque'] < -3.0)
    torque_rows = window_data_t[torque_mask]
  
    if not torque_rows.empty:
        print(f"Steering torque exceeding +/-3 before crash at {crash_time}:")
        for idx in torque_rows.index:
            torque_timestamps = torque_rows.loc[idx, 'DATE (UTC)'] 
            torque_value = torque_rows.loc[idx,'Steering Torque']
            print(f"{torque_timestamps} - {torque_value}")






