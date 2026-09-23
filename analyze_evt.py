import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev

# 1. Fetch Daily Precipitation Data via NASA POWER API (Kathmandu Basin: 27.7172 N, 85.3240 E)
latitude = 27.7172
longitude = 85.3240
start_date = "19820101"
end_date = "20260831"  # Captures historical record up to August 2026

url = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"parameters=PRECTOTCORR&community=AG&longitude={longitude}"
    f"&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"
)

print("Fetching precipitation data from NASA POWER...")
response = requests.get(url)
data = response.json()

# Parse JSON into a clean DataFrame
precip_dict = data["properties"]["parameter"]["PRECTOTCORR"]
df = pd.DataFrame(list(precip_dict.items()), columns=["Date", "Precipitation_mm"])
df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df["Year"] = df["Date"].dt.year

# Filter out NASA no-data flags (-999)
df = df[df["Precipitation_mm"] >= 0]

# Save raw data locally
df.to_csv("kathmandu_daily_rainfall_1982_2026.csv", index=False)
print("Saved raw daily data to kathmandu_daily_rainfall_1982_2026.csv")

# 2. Extract Annual Block Maxima (Peak daily rainfall per year)
annual_max = df.groupby("Year")["Precipitation_mm"].max().reset_index()

# 3. Fit Stationary GEV Distribution
# scipy.stats.genextreme uses parameter c = -xi
shape_c, loc_fit, scale_fit = gev.fit(annual_max["Precipitation_mm"])
xi = -shape_c  # Academic notation (xi > 0 indicates Fréchet / heavy-tailed)

print("\n--- Fitted GEV Parameters ---")
print(f"Location (mu): {loc_fit:.2f}")
print(f"Scale (sigma): {scale_fit:.2f}")
print(f"Shape (xi)   : {xi:.2f} (Heavy tail if > 0)")

# 4. Compute Return Periods and Levels
return_periods = np.linspace(1.1, 100, 300)
probabilities = 1 - (1 / return_periods)
return_levels = gev.ppf(probabilities, shape_c, loc=loc_fit, scale=scale_fit)

# Empirical plotting positions (Weibull Formula)
annual_max_sorted = annual_max.sort_values(by="Precipitation_mm", ascending=False).reset_index(drop=True)
n = len(annual_max_sorted)
annual_max_sorted["Rank"] = annual_max_sorted.index + 1
annual_max_sorted["Empirical_T"] = (n + 1) / annual_max_sorted["Rank"]

# 5. Plot Return Level Curve
plt.figure(figsize=(9, 5.5), dpi=200)
plt.scatter(
    annual_max_sorted["Empirical_T"], 
    annual_max_sorted["Precipitation_mm"], 
    color="#1f77b4", edgecolor="black", s=50, zorder=3, label="Annual Maxima (1982–2026)"
)
plt.plot(
    return_periods, 
    return_levels, 
    color="#d62728", lw=2, label=f"Fitted GEV Model (Shape $\\xi$ = {xi:.2f})"
)

# Highlight August 2026 event (highest recorded or peak point)
aug_2026_val = df[(df["Date"].dt.year == 2026) & (df["Date"].dt.month == 8)]["Precipitation_mm"].max()
if not np.isnan(aug_2026_val) and aug_2026_val > 0:
    plt.axhline(y=aug_2026_val, color="darkorange", linestyle="--", alpha=0.8, label=f"August 2026 Peak (~{aug_2026_val:.1f} mm)")

plt.xscale("log")
plt.title("Extreme Daily Precipitation & GEV Return Levels: Kathmandu Basin", fontsize=13, weight="bold")
plt.xlabel("Return Period (Years, Log Scale)", fontsize=11)
plt.ylabel("Daily Precipitation (mm/day)", fontsize=11)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(frameon=True, loc="upper left")

plt.tight_layout()
plt.savefig("kathmandu_gev_return_level.png")
print("\nPlot saved successfully as kathmandu_gev_return_level.png")
plt.show()