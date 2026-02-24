import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define stations
stations = {
    '09180000': 'Dolores River Below Reservoir',
    '09183600': 'Headwater Catchment'
}

colors = {
    '09180000': '#1f77b4',  # blue
    '09183600': '#2ca02c'   # green
}

wet_year = 2019
dry_year = 2018

print("="*80)
print("COMPARATIVE ANALYSIS: WET vs DRY YEAR")
print("="*80)
print(f"\nWet Year: {wet_year}")
print(f"Dry Year: {dry_year}")

# Load daily data
data_dict = {}
for station_id in ['09180000', '09183600']:
    df = pd.read_csv(station_id)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Year'] = df['Datetime'].dt.year
    df['DayOfYear'] = df['Datetime'].dt.dayofyear
    data_dict[station_id] = df

# Create figure with 2 subplots (one per station)
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# For each station
for idx, (station_id, station_name) in enumerate([('09180000', 'Dolores River Below Reservoir (Regulated)'),
                                                    ('09183600', 'Headwater Catchment (Unregulated)')]):
    df = data_dict[station_id]
    color = colors[station_id]
    
    # Get wet year and dry year data
    df_wet = df[df['Year'] == wet_year].copy()
    df_dry = df[df['Year'] == dry_year].copy()
    
    # Calculate daily range (min/max for each day of year across all years)
    daily_stats = df.groupby('DayOfYear')['USGS_flow'].agg(['min', 'max', 'mean', 'median', 'std'])
    
    # Use actual day of year values from the groupby index
    doy = daily_stats.index.values
    
    # Calculate percentiles
    daily_10 = df.groupby('DayOfYear')['USGS_flow'].quantile(0.1)
    daily_90 = df.groupby('DayOfYear')['USGS_flow'].quantile(0.9)
    
    print(f"\n{station_name}:")
    print(f"  Wet Year ({wet_year}) - Mean: {df_wet['USGS_flow'].mean():.1f} ft³/s, Peak: {df_wet['USGS_flow'].max():.1f} ft³/s")
    print(f"  Dry Year ({dry_year}) - Mean: {df_dry['USGS_flow'].mean():.1f} ft³/s, Peak: {df_dry['USGS_flow'].max():.1f} ft³/s")
    
    # Find peak flow timing
    if len(df_wet) > 0:
        wet_peak_doy = df_wet.loc[df_wet['USGS_flow'].idxmax(), 'DayOfYear']
        wet_peak_date = df_wet.loc[df_wet['USGS_flow'].idxmax(), 'Datetime']
        print(f"  Wet year peak on DOY {wet_peak_doy} ({wet_peak_date.strftime('%B %d')})")
    
    if len(df_dry) > 0:
        dry_peak_doy = df_dry.loc[df_dry['USGS_flow'].idxmax(), 'DayOfYear']
        dry_peak_date = df_dry.loc[df_dry['USGS_flow'].idxmax(), 'Datetime']
        print(f"  Dry year peak on DOY {dry_peak_doy} ({dry_peak_date.strftime('%B %d')})")
    
    # Plot on appropriate subplot
    ax = axes[idx]
    
    # Fill between min/max range
    ax.fill_between(doy, daily_stats['min'], daily_stats['max'], 
                    alpha=0.15, color=color, label='Min-Max Range')
    
    # Fill between 10th/90th percentile
    ax.fill_between(daily_10.index, daily_10.values, daily_90.values, 
                    alpha=0.25, color=color, label='10th-90th Percentile')
    
    # Plot mean
    ax.plot(daily_stats.index, daily_stats['mean'], 
           color=color, linewidth=2, alpha=0.6, label='Mean (All Years)')
    
    # Plot wet year
    df_wet_sorted = df_wet.sort_values('DayOfYear')
    ax.plot(df_wet_sorted['DayOfYear'], df_wet_sorted['USGS_flow'], 
           color='red', linewidth=2.5, marker='o', markersize=3, 
           alpha=0.9, label=f'Wet Year ({wet_year})')
    
    # Plot dry year
    df_dry_sorted = df_dry.sort_values('DayOfYear')
    ax.plot(df_dry_sorted['DayOfYear'], df_dry_sorted['USGS_flow'], 
           color='orange', linewidth=2.5, marker='s', markersize=3, 
           alpha=0.9, label=f'Dry Year ({dry_year})')
    
    ax.set_xlim(1, 365)
    ax.set_xlabel('Day of Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Flow (ft³/s)', fontsize=11, fontweight='bold')
    ax.set_title(f'{station_name}\nDaily Flow Ranges and Year Comparison', 
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=9)
    
    # Add month labels on x-axis
    month_days = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    month_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 'J']
    ax.set_xticks(month_days)
    ax.set_xticklabels(month_labels)


# Overall figure title
fig.suptitle(f'Comparative Hydrologic Analysis: Wet vs Dry Years ({dry_year}, {wet_year})\nDolores River (Regulated) vs Headwater Catchment (Unregulated)',
            fontsize=15, fontweight='bold', y=0.995)

plt.tight_layout()
plt.savefig('06_wet_dry_comparative_analysis.png', dpi=300, bbox_inches='tight')
print("\n" + "="*80)
print("Figure saved: 06_wet_dry_comparative_analysis.png")
print("="*80)
plt.close()
