import pandas as pd
import numpy as np

# Define station names and files
stations = {
    '09180000': 'Dolores River Near Cisco',
    '09180500': 'Colorado River North of La Sals',
    '09183600': 'Headwater Catchment In The Same Region'
}

print("="*70)
print("RESAMPLING DAILY DATA TO MONTHLY VOLUMES")
print("="*70)

# Conversion factor: ft³/s to acre-feet per day
# 1 day = 86,400 seconds
# 1 acre-foot = 43,560 ft³
# Flow (ft³/s) × 86,400 s/day ÷ 43,560 ft³/acre-ft = acre-feet/day
SECONDS_PER_DAY = 86400
FT3_PER_ACRE_FT = 43560

for station_id, station_name in stations.items():
    # Load the data
    df = pd.read_csv(station_id)
    
    # Convert Datetime to datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    # Convert daily flow (ft³/s) to daily volume (acre-feet)
    df['daily_volume_acft'] = (df['USGS_flow'] * SECONDS_PER_DAY) / FT3_PER_ACRE_FT
    
    # Set Datetime as index
    df.set_index('Datetime', inplace=True)
    
    # Get original statistics
    print(f"\n{station_name}:")
    print(f"  Original data points: {len(df)}")
    print(f"  Date range: {df.index.min()} to {df.index.max()}")
    
    # Resample to monthly total volume (sum of daily volumes)
    df_monthly = df[['daily_volume_acft']].resample('MS').sum()
    
    # Rename column
    df_monthly.rename(columns={'daily_volume_acft': 'USGS_flow'}, inplace=True)
    
    print(f"  Resampled to monthly: {len(df_monthly)} months")
    
    # Reset index to keep Datetime as a column
    df_monthly.reset_index(inplace=True)
    
    # Add back the other columns
    df_monthly['variable'] = 'streamflow_volume'
    df_monthly['USGS_ID'] = int(station_id)
    df_monthly['measurement_unit'] = 'acre-ft'
    df_monthly['qualifiers'] = "['M']"  # Marking as monthly aggregated data
    df_monthly['series'] = 0
    
    # Reorder columns to match original
    df_monthly = df_monthly[['Datetime', 'USGS_flow', 'variable', 'USGS_ID', 'measurement_unit', 'qualifiers', 'series']]
    
    # Save with _monthly suffix
    df_monthly.to_csv(f'{station_id}_monthly', index=False)
    print(f"  Saved to: {station_id}_monthly")
    print(f"  Monthly volume statistics (acre-feet):")
    print(f"    Mean: {df_monthly['USGS_flow'].mean():.2f} acre-ft")
    print(f"    Std: {df_monthly['USGS_flow'].std():.2f} acre-ft")
    print(f"    Min: {df_monthly['USGS_flow'].min():.2f} acre-ft")
    print(f"    Max: {df_monthly['USGS_flow'].max():.2f} acre-ft")

print("\n" + "="*70)
print("MONTHLY VOLUME RESAMPLING COMPLETE")
print("="*70)
print("\nMonthly files created:")
print("  - 09180000_monthly")
print("  - 09180500_monthly")
print("  - 09183600_monthly")
print("\nUnits: acre-feet (monthly total volume)")
