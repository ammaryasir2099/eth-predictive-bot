# eth-predictive-bot
High-frequency Ethereum (ETHUSDT) Binance Futures trading bot using progressive grid strategy, auto profit scaling, and dual-side intelligent order execution

⚡ ETH Futures Trading Bot (Binance USDT-M)

A high-frequency Ethereum futures trading bot built using Python and Binance Futures API. Designed for precision grid-based trading with progressive capital scaling and real-time decision making.  

> 📌 Disclaimer: This bot is intended for educational and testing purposes only. Use in live trading at your own risk.

---

🚀 Features

- 📈 Supports ETH/USDT Perpetual Futures (Binance USDT-M)
- 🧠 Uses step-wise progressive grid strategy (buy/sell based on price distance)
- 🔁 Alternating market + limit order logic with geometric progression investment
- 📊 Leverages real-time Binance mark price API
- 💵 11x leverage (can be configured)
- 💡 Uses only one API account (single-account version)
- 🔧 Auto-adjusts for tick size and quantity precision
- 🧪 Tested and ready for cross-platform usage (Windows, macOS, Linux)

---

📈 Strategy Overview

This bot uses a progressive buy-sell laddering strategy tailored for Ethereum’s volatility.

🔁 Logic Summary:

1. Places an initial market BUY and SELL order at current ETH/USDT mark price.
2. Monitors price in real-time.
3. On price drop:  
   - Places a BUY limit order below last buy using a step gap  
   - Increases investment with geometric progression (e.g., $5 → $5.5 → $6.05)
4. On price rise:  
   - Places a SELL limit order above last sell using similar logic  
5. Repeats this alternating logic infinitely until manually stopped.

📌 Bot Configuration:
- `symbol`: ETHUSDT
- `base_investment`: `$5` (scales using 1.1x multiplier)
- `leverage`: `11x`  
- `step_size`: `1.5` (price gap in USDT between each grid level)
- Uses accurate Binance tick size & quantity precision

---

⚙️ Installation & Usage

Prerequisites
- Python 3.10+ (Install from [python.org](https://www.python.org/downloads/))
- Binance Futures Account (with API key and secret)

🔧 Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/eth-futures-bot.git
cd eth-futures-bot

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate.bat     # On Windows

# 3. Install required libraries
pip install -r requirements.txt

# 4. Add your Binance credentials in a `.env` file:
# .env
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here

# 5. Run the bot
python eth_bot.py
________________________________________
💡 Best Use Cases
This bot is ideal in the following market conditions:
Market Type	Recommended	Notes
🔁 Sideways/Range-Bound	✅ Yes	Works best in chop/flat markets with micro-volatility
📉 Downtrend	⚠️ Caution	Bot will continue buying lower; ensure capital buffer
📈 Uptrend	⚠️ Caution	Bot will continue selling higher; use manual monitoring
🧨 High Volatility	❌ Avoid	Extreme spikes can trigger fast successive orders
________________________________________
📌 Recommendations
•	Start with small test amounts ($5) and paper trade to observe behavior.
•	Monitor execution through Binance app or browser for learning.
•	Make sure you have sufficient USDT margin to support progressive orders.
•	Ensure Futures trading is enabled on your Binance account.
________________________________________
Disclaimer
This software is provided "as is", without warranty of any kind.
Cryptocurrency trading involves high risk. You are solely responsible for any losses.
This bot does not use stop-loss and assumes manual monitoring for critical conditions.
________________________________________
License
This project is licensed under the MIT License — feel free to use and adapt it.
________________________________________
Contributions
Feel free to fork, raise issues, or suggest improvements via pull requests.
________________________________________
Contact
Author: Rana Ammar Yasir
Mission: Building AI & Bots for Climate Action, Efficiency & Peace
Email: ammar.yasir2099@gmail.com 
Website Portfolio: www.planetsavetoken.com
Linkedin :  https://www.linkedin.com/in/rana-ammar-yasir 

