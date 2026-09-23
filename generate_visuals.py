import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import genextreme as gev

# Load previously downloaded NASA dataset
df = pd.read_csv("kathmandu_daily_rainfall_1982_2026.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# -------------------------------------------------------------
# VISUALIZATION 1: Seasonal Extreme Rainfall Heatmap (Monsoon Peak)
# -------------------------------------------------------------
# Group by Year and Month to extract monthly maximum daily rainfall
monthly_max = df.pivot_table(
    index="Year", 
    columns="Month", 
    values="Precipitation_mm", 
    aggfunc="max"
)

# Rename columns to standard 3-letter month abbreviations
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly_max.columns = month_labels

plt.figure(figsize=(11, 8), dpi=200)
cmap = sns.color_palette("YlGnBu", as_cmap=True)

ax1 = sns.heatmap(
    monthly_max, 
    cmap=cmap, 
    cbar_kws={'label': 'Peak 24-hr Rainfall (mm/day)'},
    linewidths=0.2, 
    linecolor="#f0f0f0"
)

plt.title("Kathmandu Basin: Monthly Maximum Daily Precipitation Matrix (1982–2026)", fontsize=13, weight="bold", pad=15)
plt.xlabel("Month", fontsize=11, labelpad=10)
plt.ylabel("Year", fontsize=11)
plt.tight_layout()
plt.savefig("kathmandu_monsoon_heatmap.png")
print("Saved: kathmandu_monsoon_heatmap.png")
plt.close()

# -------------------------------------------------------------
# VISUALIZATION 2: Rolling 15-Year Non-Stationary Return Levels
# -------------------------------------------------------------
# Test whether 20-year and 50-year return levels are increasing over time
years = np.sort(df["Year"].unique())
window_size = 15
rolling_results = []

for start_yr in range(years.min(), years.max() - window_size + 2):
    end_yr = start_yr + window_size - 1
    sub_df = df[(df["Year"] >= start_yr) & (df["Year"] <= end_yr)]
    annual_peaks = sub_df.groupby("Year")["Precipitation_mm"].max().values
    
    if len(annual_peaks) == window_size:
        try:
            # Fit GEV
            c, loc, scale = gev.fit(annual_peaks)
            # Calculate 20-year and 50-year return levels
            rl_20 = gev.ppf(1 - 1/20, c, loc=loc, scale=scale)
            rl_50 = gev.ppf(1 - 1/50, c, loc=loc, scale=scale)
            mid_year = end_yr
            rolling_results.append({
                "Window_End": mid_year,
                "RL_20yr": rl_20,
                "RL_50yr": rl_50
            })
        except Exception:
            continue

roll_df = pd.DataFrame(rolling_results)

plt.figure(figsize=(10, 5), dpi=200)
plt.plot(roll_df["Window_End"], roll_df["RL_50yr"], color="#b2182b", lw=2.5, marker="o", label="50-Year Return Level (15-yr Rolling GEV)")
plt.plot(roll_df["Window_End"], roll_df["RL_20yr"], color="#2166ac", lw=2, marker="s", linestyle="--", label="20-Year Return Level (15-yr Rolling GEV)")

plt.title("Tail Risk Non-Stationarity: Rolling 15-Year Extreme Rainfall Thresholds", fontsize=13, weight="bold")
plt.xlabel("Window End Year", fontsize=11)
plt.ylabel("Estimated Return Level (mm/day)", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig("kathmandu_rolling_return_levels.png")
print("Saved: kathmandu_rolling_return_levels.png")
plt.close()