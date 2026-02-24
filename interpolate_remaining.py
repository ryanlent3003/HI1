import pandas as pd

# Process both stations
stations = ['09180000', '09183600']

for station in stations:
    df = pd.read_csv(station)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    missing_before = df['USGS_flow'].isna().sum()
    print(f"\n{station}:")
    print(f"  Missing values before: {missing_before}")
    
    # Linear interpolation
    df['USGS_flow'] = df['USGS_flow'].interpolate(method='linear')
    
    # Fill any remaining edge NaNs
    remaining = df['USGS_flow'].isna().sum()
    if remaining > 0:
        df['USGS_flow'] = df['USGS_flow'].bfill().ffill()
    
    # Save
    df.to_csv(station, index=False)
    print(f"  Missing values after: {df['USGS_flow'].isna().sum()}")
    print(f"  Data saved to {station}")

print("\n" + "="*60)
print("INTERPOLATION COMPLETE")
print("="*60)
print("\nAll stations (09180000 and 09183600) have been interpolated.")
print("Regenerate the workspace.py visualizations to see the updated graphs.")
