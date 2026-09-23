# Kathmandu Basin: Extreme Daily Precipitation & Extreme Value Analysis (1982–2026)

## Overview
This repository provides an empirical Extreme Value Theory (EVT) analysis of daily precipitation extremes in the Kathmandu Valley (27.7172° N, 85.3240° E), motivated by recurrent devastating monsoon flooding, including the catastrophic August 2026 flood event.

The primary objective is to evaluate whether stationary assumptions in traditional peril pricing and municipal drainage criteria remain valid given shifting tail risk in high-altitude Himalayan catchments.

## Methodology
- **Data Source:** Daily precipitation series retrieved from the NASA POWER API (1982–2026).
- **Extreme Value Modeling:** Block Maxima approach fitting a Generalized Extreme Value (GEV) distribution via Maximum Likelihood Estimation (MLE):
  
  $$G(z) = \exp\left\{ -\left[1 + \xi \left(\frac{z - \mu}{\sigma}\right)\right]^{-1/\xi}\right\}$$

- **Key Parameters:**
  - $\mu$ (Location)
  - $\sigma$ (Scale)
  - $\xi$ (Shape parameter determining tail heaviness: Fréchet vs. Gumbel)
- **Actuarial Implications:** Evaluates return level compression and the basis risk of parametric catastrophe triggers versus indemnity coverage in low-penetration insurance markets.

## Results
![GEV Return Level Plot](kathmandu_gev_return_level.png)

## Reproduction
```bash
pip install -r requirements.txt
python analyze_evt.py

Author
Sagar Niraula
Master of Actuarial Practice, Macquarie University
Former Actuarial Analyst, Nepal Life Insurance Co. Ltd.