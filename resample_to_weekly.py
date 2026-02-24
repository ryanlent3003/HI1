import pandas as pd

# Define station names and files
stations = {
    '09180000': 'Dolores River Near Cisco',
    '09180500': 'Colorado River North of La Sals',
    '09183600': 'Headwater Catchment In The Same Region'
}

print("="*70)
print("RESAMPLING DAILY DATA TO WEEKLY MEANS")
print("="*70)

for station_id, station_name in stations.items():
    # Load the data
    df = pd.read_csv(station_id)
    
    # Convert Datetime to datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    # Set Datetime as index
    df.set_index('Datetime', inplace=True)
    
    # Get original statistics
    print(f"\n{station_name}:")
    print(f"  Original data points: {len(df)}")
    print(f"  Date range: {df.index.min()} to {df.index.max()}")
    
    # Resample to weekly mean
    df_weekly = df[['USGS_flow']].resample('W').mean()
    
    print(f"  Resampled to weekly: {len(df_weekly)} weeks")
    
    # Reset index to keep Datetime as a column
    df_weekly.reset_index(inplace=True)
    
    # Add back the other columns (keeping them consistent with original)
    df_weekly['variable'] = 'streamflow'
    df_weekly['USGS_ID'] = int(station_id)
    df_weekly['measurement_unit'] = 'ft3/s'
    df_weekly['qualifiers'] = "['W']"  # Marking as weekly aggregated data
    df_weekly['series'] = 0
    
    # Reorder columns to match original
    df_weekly = df_weekly[['Datetime', 'USGS_flow', 'variable', 'USGS_ID', 'measurement_unit', 'qualifiers', 'series']]
    
    # Save with _weekly suffix
    df_weekly.to_csv(f'{station_id}_weekly', index=False)
    print(f"  Saved to: {station_id}_weekly")
    print(f"  Weekly statistics:")
    print(f"    Mean: {df_weekly['USGS_flow'].mean():.2f} ft³/s")
    print(f"    Std: {df_weekly['USGS_flow'].std():.2f} ft³/s")
    print(f"    Min: {df_weekly['USGS_flow'].min():.2f} ft³/s")
    print(f"    Max: {df_weekly['USGS_flow'].max():.2f} ft³/s")

print("\n" + "="*70)
print("RESAMPLING COMPLETE")
print("="*70)
print("\nWeekly files created:")
print("  - 09180000_weekly")
print("  - 09180500_weekly")
print("  - 09183600_weekly")
