import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define station names
station_names = {
    '09180000': 'Dolores River Near Cisco',
    '09180500': 'Colorado River North of La Sals',
    '09183600': 'Headwater Catchment In The Same Region'
}

# Load the three weekly streamflow datasets
df1 = pd.read_csv('09180000_weekly')
df2 = pd.read_csv('09180500_weekly')
df3 = pd.read_csv('09183600_weekly')

# Convert Datetime column to datetime format
df1['Datetime'] = pd.to_datetime(df1['Datetime'])
df2['Datetime'] = pd.to_datetime(df2['Datetime'])
df3['Datetime'] = pd.to_datetime(df3['Datetime'])

# ============================================================================
# FIGURE 1: Weekly Time-Series Plot with All Three Stations
# ============================================================================
fig1, ax = plt.subplots(figsize=(14, 6))

ax.plot(df1['Datetime'], df1['USGS_flow'], label=station_names['09180000'], linewidth=2, alpha=0.8, marker='o', markersize=3)
ax.plot(df2['Datetime'], df2['USGS_flow'], label=station_names['09180500'], linewidth=2, alpha=0.8, marker='s', markersize=3)
ax.plot(df3['Datetime'], df3['USGS_flow'], label=station_names['09183600'], linewidth=2, alpha=0.8, marker='^', markersize=3)

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('03_weekly_timeseries_all_stations.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 2: Four Subplots for Weekly Data Analysis
# ============================================================================
fig2, axes = plt.subplots(2, 2, figsize=(16, 10))

# Subplot 1: Individual Weekly Time Series for Station 09180000
axes[0, 0].plot(df1['Datetime'], df1['USGS_flow'], color='steelblue', linewidth=2, marker='o', markersize=4)
axes[0, 0].fill_between(df1['Datetime'], df1['USGS_flow'], alpha=0.3, color='steelblue')
axes[0, 0].grid(True, alpha=0.3)

# Subplot 2: Individual Weekly Time Series for Station 09180500
axes[0, 1].plot(df2['Datetime'], df2['USGS_flow'], color='darkorange', linewidth=2, marker='s', markersize=4)
axes[0, 1].fill_between(df2['Datetime'], df2['USGS_flow'], alpha=0.3, color='darkorange')
axes[0, 1].grid(True, alpha=0.3)

# Subplot 3: Individual Weekly Time Series for Station 09183600
axes[1, 0].plot(df3['Datetime'], df3['USGS_flow'], color='forestgreen', linewidth=2, marker='^', markersize=4)
axes[1, 0].fill_between(df3['Datetime'], df3['USGS_flow'], alpha=0.3, color='forestgreen')
axes[1, 0].grid(True, alpha=0.3)

# Subplot 4: Overlaid Comparison (normalized)
df1_normalized = (df1['USGS_flow'] - df1['USGS_flow'].mean()) / df1['USGS_flow'].std()
df2_normalized = (df2['USGS_flow'] - df2['USGS_flow'].mean()) / df2['USGS_flow'].std()
df3_normalized = (df3['USGS_flow'] - df3['USGS_flow'].mean()) / df3['USGS_flow'].std()

axes[1, 1].plot(df1['Datetime'], df1_normalized, label=station_names['09180000'], linewidth=2, alpha=0.8, marker='o', markersize=3)
axes[1, 1].plot(df2['Datetime'], df2_normalized, label=station_names['09180500'], linewidth=2, alpha=0.8, marker='s', markersize=3)
axes[1, 1].plot(df3['Datetime'], df3_normalized, label=station_names['09183600'], linewidth=2, alpha=0.8, marker='^', markersize=3)
axes[1, 1].grid(True, alpha=0.3)

# Overall figure title
plt.tight_layout()
plt.savefig('04_weekly_four_subplots_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

