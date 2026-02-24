import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('09180500')

# Convert Datetime to datetime format
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Store original for comparison
missing_before = df['USGS_flow'].isna().sum()
print(f"Missing values before interpolation: {missing_before}")
print(f"Percentage missing: {100 * missing_before / len(df):.2f}%")

# Interpolate using linear method (good for time-series data)
df['USGS_flow'] = df['USGS_flow'].interpolate(method='linear')

# Check if any NaNs remain at edges (interpolate doesn't fill edge NaNs)
remaining_missing = df['USGS_flow'].isna().sum()
print(f"Missing values after linear interpolation: {remaining_missing}")

# If there are any remaining NaNs (typically at start/end), use forward/backward fill
if remaining_missing > 0:
    df['USGS_flow'] = df['USGS_flow'].bfill().ffill()
    print(f"Missing values after forward/backward fill: {df['USGS_flow'].isna().sum()}")

# Save the interpolated data
df.to_csv('09180500', index=False)
print("\nInterpolated data saved to 09180500")

# Print summary
print("\n" + "="*60)
print("INTERPOLATION SUMMARY")
print("="*60)
print(f"Total records: {len(df)}")
print(f"Records with interpolated values: {missing_before}")
print(f"Remaining missing values: {df['USGS_flow'].isna().sum()}")
print("\nStreamflow statistics after interpolation:")
print(df['USGS_flow'].describe())
