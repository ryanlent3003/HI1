import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define station names
station_names = {
    '09180000': 'Dolores River Near Cisco',
    '09180500': 'Colorado River North of La Sals',
    '09183600': 'Headwater Catchment In The Same Region'
}

# Load the three streamflow datasets
df1 = pd.read_csv('09180000')
df2 = pd.read_csv('09180500')
df3 = pd.read_csv('09183600')

# Convert Datetime column to datetime format
df1['Datetime'] = pd.to_datetime(df1['Datetime'])
df2['Datetime'] = pd.to_datetime(df2['Datetime'])
df3['Datetime'] = pd.to_datetime(df3['Datetime'])

# ============================================================================
# FIGURE 1: Initial Time-Series Plot with All Three Stations
# ============================================================================
fig1, ax = plt.subplots(figsize=(14, 6))

ax.plot(df1['Datetime'], df1['USGS_flow'], label=station_names['09180000'], linewidth=1.5, alpha=0.8)
ax.plot(df2['Datetime'], df2['USGS_flow'], label=station_names['09180500'], linewidth=1.5, alpha=0.8)
ax.plot(df3['Datetime'], df3['USGS_flow'], label=station_names['09183600'], linewidth=1.5, alpha=0.8)

ax.set_title('Streamflow Time Series - Three USGS Stations (2014-2020)', fontsize=14, fontweight='bold')
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Streamflow (ft³/s)', fontsize=12, fontweight='bold')
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('01_timeseries_all_stations.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 2: Four Subplots for Comprehensive Analysis
# ============================================================================
fig2, axes = plt.subplots(2, 2, figsize=(16, 10))

# Subplot 1: Individual Time Series for Station 09180000
axes[0, 0].plot(df1['Datetime'], df1['USGS_flow'], color='steelblue', linewidth=1.2)
axes[0, 0].set_title(station_names['09180000'] + ' - Streamflow Time Series', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Date', fontsize=10)
axes[0, 0].set_ylabel('Streamflow (ft³/s)', fontsize=10)
axes[0, 0].grid(True, alpha=0.3)

# Subplot 2: Individual Time Series for Station 09180500
axes[0, 1].plot(df2['Datetime'], df2['USGS_flow'], color='darkorange', linewidth=1.2)
axes[0, 1].set_title(station_names['09180500'] + ' - Streamflow Time Series', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Date', fontsize=10)
axes[0, 1].set_ylabel('Streamflow (ft³/s)', fontsize=10)
axes[0, 1].grid(True, alpha=0.3)

# Subplot 3: Individual Time Series for Station 09183600
axes[1, 0].plot(df3['Datetime'], df3['USGS_flow'], color='forestgreen', linewidth=1.2)
axes[1, 0].set_title(station_names['09183600'] + ' - Streamflow Time Series', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Date', fontsize=10)
axes[1, 0].set_ylabel('Streamflow (ft³/s)', fontsize=10)
axes[1, 0].grid(True, alpha=0.3)

# Subplot 4: Overlaid Comparison (normalized for comparison)
df1_normalized = (df1['USGS_flow'] - df1['USGS_flow'].mean()) / df1['USGS_flow'].std()
df2_normalized = (df2['USGS_flow'] - df2['USGS_flow'].mean()) / df2['USGS_flow'].std()
df3_normalized = (df3['USGS_flow'] - df3['USGS_flow'].mean()) / df3['USGS_flow'].std()

axes[1, 1].plot(df1['Datetime'], df1_normalized, label=station_names['09180000'], linewidth=1.2, alpha=0.8)
axes[1, 1].plot(df2['Datetime'], df2_normalized, label=station_names['09180500'], linewidth=1.2, alpha=0.8)
axes[1, 1].plot(df3['Datetime'], df3_normalized, label=station_names['09183600'], linewidth=1.2, alpha=0.8)
axes[1, 1].set_title('Normalized Streamflow Comparison', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Date', fontsize=10)
axes[1, 1].set_ylabel('Normalized Streamflow (Standard Deviations)', fontsize=10)
axes[1, 1].legend(loc='best', fontsize=10)
axes[1, 1].grid(True, alpha=0.3)

# Overall figure title
fig2.suptitle('Streamflow Analysis - Four-Panel Visualization (2014-2020)', 
              fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('02_four_subplots_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Print summary statistics
print("=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print(f"\n{station_names['09180000']}:")
print(df1['USGS_flow'].describe())
print(f"\n{station_names['09180500']}:")
print(df2['USGS_flow'].describe())
print(f"\n{station_names['09183600']}:")
print(df3['USGS_flow'].describe())
