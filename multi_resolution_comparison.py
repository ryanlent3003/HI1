import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Define station names
station_names = {
    '09180000': 'Dolores River Near Cisco',
    '09180500': 'Colorado River North of La Sals',
    '09183600': 'Headwater Catchment In The Same Region'
}

# Define colors and markers for each station
colors = {
    '09180000': '#1f77b4',  # blue
    '09180500': '#ff7f0e',  # orange
    '09183600': '#2ca02c'   # green
}

markers = {
    '09180000': 'o',
    '09180500': 's',
    '09183600': '^'
}

# Load all three resolutions of data
print("Loading data...")
daily_data = {}
weekly_data = {}
monthly_data = {}

for station_id in ['09180000', '09180500', '09183600']:
    # Daily
    df_daily = pd.read_csv(station_id)
    df_daily['Datetime'] = pd.to_datetime(df_daily['Datetime'])
    daily_data[station_id] = df_daily
    
    # Weekly
    df_weekly = pd.read_csv(f'{station_id}_weekly')
    df_weekly['Datetime'] = pd.to_datetime(df_weekly['Datetime'])
    weekly_data[station_id] = df_weekly
    
    # Monthly
    df_monthly = pd.read_csv(f'{station_id}_monthly')
    df_monthly['Datetime'] = pd.to_datetime(df_monthly['Datetime'])
    monthly_data[station_id] = df_monthly

# Create the figure with custom layout
fig = plt.figure(figsize=(18, 12))

# Create grid for 3 plots on left, legend on right
gs = fig.add_gridspec(2, 4, hspace=0.35, wspace=0.3)
ax_daily = fig.add_subplot(gs[0, :2])
ax_weekly = fig.add_subplot(gs[0, 2:])
ax_monthly = fig.add_subplot(gs[1, :2])
ax_legend = fig.add_subplot(gs[1, 2:])

# ============================================================================
# PANEL A: Daily (Raw) - Flow in ft³/s
# ============================================================================
for station_id in ['09180000', '09180500', '09183600']:
    df = daily_data[station_id]
    ax_daily.plot(df['Datetime'], df['USGS_flow'], 
                 label=station_names[station_id], 
                 color=colors[station_id], 
                 linewidth=1, alpha=0.7)

ax_daily.set_title('Panel A: Daily (Raw)', fontsize=13, fontweight='bold', loc='left')
ax_daily.set_ylabel('Flow (ft³/s)', fontsize=11, fontweight='bold')
ax_daily.grid(True, alpha=0.3)
ax_daily.set_xlim(daily_data['09180000']['Datetime'].min(), daily_data['09180000']['Datetime'].max())

# ============================================================================
# PANEL B: Weekly Mean - Flow in ft³/s
# ============================================================================
for station_id in ['09180000', '09180500', '09183600']:
    df = weekly_data[station_id]
    ax_weekly.plot(df['Datetime'], df['USGS_flow'], 
                  label=station_names[station_id], 
                  color=colors[station_id], 
                  linewidth=1.5, alpha=0.8, 
                  marker=markers[station_id], markersize=3)

ax_weekly.set_title('Panel B: Weekly Mean', fontsize=13, fontweight='bold', loc='left')
ax_weekly.set_ylabel('Flow (ft³/s)', fontsize=11, fontweight='bold')
ax_weekly.grid(True, alpha=0.3)
ax_weekly.set_xlim(weekly_data['09180000']['Datetime'].min(), weekly_data['09180000']['Datetime'].max())

# ============================================================================
# PANEL C: Monthly Volume - in Acre-Feet
# ============================================================================
for station_id in ['09180000', '09180500', '09183600']:
    df = monthly_data[station_id]
    ax_monthly.plot(df['Datetime'], df['USGS_flow'], 
                   label=station_names[station_id], 
                   color=colors[station_id], 
                   linewidth=1.5, alpha=0.8,
                   marker=markers[station_id], markersize=5)
    ax_monthly.fill_between(df['Datetime'], df['USGS_flow'], 
                           alpha=0.2, color=colors[station_id])

ax_monthly.set_title('Panel C: Monthly Volume', fontsize=13, fontweight='bold', loc='left')
ax_monthly.set_xlabel('Date', fontsize=11, fontweight='bold')
ax_monthly.set_ylabel('Volume (acre-feet)', fontsize=11, fontweight='bold')
ax_monthly.grid(True, alpha=0.3)
ax_monthly.set_xlim(monthly_data['09180000']['Datetime'].min(), monthly_data['09180000']['Datetime'].max())

# ============================================================================
# PANEL D: Legend
# ============================================================================
ax_legend.axis('off')

# Create legend patches
legend_elements = []
for station_id in ['09180000', '09180500', '09183600']:
    legend_elements.append(mpatches.Patch(
        color=colors[station_id], 
        label=station_names[station_id],
        alpha=0.7
    ))

# Add legend with title and detailed info
legend = ax_legend.legend(handles=legend_elements, 
                         loc='center', 
                         fontsize=12, 
                         title='Stations',
                         title_fontsize=13,
                         frameon=True,
                         fancybox=True,
                         shadow=True)


# Overall figure title
fig.suptitle('Multi-Resolution Streamflow Analysis: Daily, Weekly, and Monthly Comparison (2014-2020)', 
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig('05_multi_resolution_comparison.png', dpi=300, bbox_inches='tight')
print("Figure saved: 05_multi_resolution_comparison.png")
plt.close()

# Print summary
print("\n" + "="*80)
print("MULTI-RESOLUTION COMPARISON CREATED")
print("="*80)
print("\nFigure includes:")
print("  Panel A: Daily (Raw) - Flow in ft³/s")
print("  Panel B: Weekly Mean - Flow in ft³/s")
print("  Panel C: Monthly Volume - Volume in acre-feet")
print("  Panel D: Legend and Information")
print("\nAll three stations plotted on each panel with consistent colors:")
for station_id in ['09180000', '09180500', '09183600']:
    print(f"  • {station_names[station_id]}")
