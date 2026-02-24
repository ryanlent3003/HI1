import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load monthly data to identify wet and dry years
print("="*80)
print("IDENTIFYING WET AND DRY YEARS FROM VOLUMETRIC ANALYSIS")
print("="*80)

stations = {
    '09180000': 'Dolores River Below Reservoir',
    '09183600': 'Headwater Catchment'
}

# Calculate annual totals from monthly data
for station_id, station_name in stations.items():
    df_monthly = pd.read_csv(f'{station_id}_monthly')
    df_monthly['Datetime'] = pd.to_datetime(df_monthly['Datetime'])
    df_monthly['Year'] = df_monthly['Datetime'].dt.year
    
    annual_volume = df_monthly.groupby('Year')['USGS_flow'].sum()
    
    print(f"\n{station_name}:")
    print(annual_volume)
    
    wet_year = annual_volume.idxmax()
    dry_year = annual_volume.idxmin()
    
    print(f"  Wet Year: {wet_year} ({annual_volume[wet_year]:.0f} acre-ft)")
    print(f"  Dry Year: {dry_year} ({annual_volume[dry_year]:.0f} acre-ft)")

# Based on analysis:
# Dolores: Find wet/dry
# Headwater: Find wet/dry
# Let's load data and compute

df_dolores_monthly = pd.read_csv('09180000_monthly')
df_headwater_monthly = pd.read_csv('09183600_monthly')

df_dolores_monthly['Datetime'] = pd.to_datetime(df_dolores_monthly['Datetime'])
df_headwater_monthly['Datetime'] = pd.to_datetime(df_headwater_monthly['Datetime'])

df_dolores_monthly['Year'] = df_dolores_monthly['Datetime'].dt.year
df_headwater_monthly['Year'] = df_headwater_monthly['Datetime'].dt.year

dolores_annual = df_dolores_monthly.groupby('Year')['USGS_flow'].sum()
headwater_annual = df_headwater_monthly.groupby('Year')['USGS_flow'].sum()

# Get wet and dry years
dolores_wet_year = dolores_annual.idxmax()
dolores_dry_year = dolores_annual.idxmin()
headwater_wet_year = headwater_annual.idxmax()
headwater_dry_year = headwater_annual.idxmin()

# Use the same year for both locations (or pick the years that show best contrast)
# Let's use the most contrasting years
all_years = sorted(set([dolores_wet_year, dolores_dry_year, headwater_wet_year, headwater_dry_year]))
print(f"\n\nYears to analyze: {all_years}")
print(f"\nUsing: Wet Year = {dolores_wet_year}, Dry Year = {dolores_dry_year}")

wet_year = dolores_wet_year
dry_year = dolores_dry_year

print(f"\nDolores annual volumes:")
print(f"  Year {wet_year}: {dolores_annual[wet_year]:.0f} acre-ft (WET)")
print(f"  Year {dry_year}: {dolores_annual[dry_year]:.0f} acre-ft (DRY)")
print(f"\nHeadwater annual volumes:")
print(f"  Year {wet_year}: {headwater_annual[wet_year]:.0f} acre-ft (WET)")
print(f"  Year {dry_year}: {headwater_annual[dry_year]:.0f} acre-ft (DRY)")
