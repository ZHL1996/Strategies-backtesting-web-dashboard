# 📊 Fama-French 3-Factor Strategies Backtesting Dashboard

An interactive Python web dashboard for exploring, backtesting, and visualizing **Fama-French 3-Factor** equity investment strategies across time, sectors, and regions.

---

## 🧠 Overview

This tool allows users to:
- Construct long/short portfolios based on **Size (SMB)**, **Value (HML)**, and **Market (MKT)** factors.
- Perform **historical backtesting** of each factor individually or in combination.
- Visualize performance, risk metrics, and factor exposures over time.
- Interactively adjust parameters (e.g., rebalance frequency, ranking percentile, region).

---

## 🧮 Fama-French 3-Factor Model

\[
R_i - R_f = \alpha + \beta_{MKT}(R_m - R_f) + \beta_{SMB} \cdot \text{SMB} + \beta_{HML} \cdot \text{HML} + \epsilon
\]

Where:
- \(R_i\): Asset return  
- \(R_f\): Risk-free rate  
- \(R_m\): Market return  
- **SMB**: Small minus big (Size effect)  
- **HML**: High minus low (Value effect)

---

## 🚀 Key Features

- 📈 **Factor Portfolio Construction**: Build portfolios based on FF3 characteristics (size/value).
- 🧪 **Backtesting Engine**: Supports rolling rebalancing and out-of-sample evaluation.
- 📊 **Interactive Dashboard**:
  - Cumulative returns, drawdowns, and performance ratios
  - Factor exposure analysis (regression on FF3)
  - Compare factor-based portfolios with market and equal-weighted benchmarks
- 🔧 **Custom Settings**:
  - Rebalancing frequency (monthly, quarterly)
  - Factor ranking thresholds (e.g., top 30% value)
  - Investment universe filters (e.g., S&P 500, Russell 1000)

---

## 📁 File Structure

- `main.py`: The main web application script (Streamlit or Dash)
- `rets.csv`: Asset or strategy return data
- `smb.csv`: Size factor (SMB) returns
- `sp500.csv`: Benchmark returns (S&P 500)
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation

---

## 👤 Author

**Zhuohang Li**  
Quant Portfolio Manager & PhD Candidate  
📧 zhuohang.li@edhec.com  
[LinkedIn](https://www.linkedin.com/in/goethe-uni-zhuohang-li/?locale=en_US)

---

## 📄 License

MIT License — for academic and non-commercial use with proper attribution.

