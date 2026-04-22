# Binance Futures Testnet Trading Bot

A robust, production-like Python CLI application to place orders on the Binance Futures Testnet (USDT-M). Built with lightweight dependencies and industry-standard practices.

## Features & Highlights (What was built)
This project fulfills all core requirements and includes several extra quality-of-life additions:
* **Native API Implementation**: Uses `requests` and implements cryptographically secure HMAC-SHA256 request signing manually, rather than relying on heavy monolithic libraries like `python-binance`.
* **Enhanced CLI UX**: Driven by `click`, the CLI provides clear parameter summaries, colored console text (success/errors), and interactive fallback prompts. If you forget to provide a required flag (like `--price` for a LIMIT order), the system pauses and asks you for it dynamically rather than crashing. 
* **Pre-Flight Input Validation**: The `bot/validators.py` module strictly filters bad inputs (negative quantities, missing prices, malformed symbols) natively before network requests are even attempted, saving API bandwidth.
* **Granular Exception Handling**: Traps and intercepts network errors, localized HTTP status codes (e.g. `401 Unauthorized`), and invalid configuration formatting gracefully.
* **Separation of Concerns**: Beautifully structured codebase segregating domain logic (`orders.py`) from network logic (`client.py`) and presentation (`cli.py`).

## Setup Steps

1. Create a virtual environment and load the project dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. Retrieve your Testnet Credentials:
   - Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
   - Login / Register and create API credentials.

3. Create a `.env` file in the root directory (where `cli.py` is located) for safe credential storage:
   ```env
   BINANCE_TESTNET_API_KEY=your_api_key_here
   BINANCE_TESTNET_API_SECRET=your_api_secret_here
   ```

## How to Run Examples

### 1. Market Order
Execute a trade at current market price instantly:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### 2. Limit Order
Execute a trade at a specific price:
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 2000
```

### 3. Interactive Mode
If you run the base script without arguments, it acts as a wizard and will prompt you for the necessary information step-by-step.
```bash
python cli.py
```

## Assumptions
- Code was targeted specifically for the USDT-M Futures Testnet. Base URL used: `https://testnet.binancefuture.com`
- User has created API keys via the testnet interface and funded their dummy account with testnet USDT to accurately execute live orders.
- Direct REST HTTP calls (`requests`) are explicitly used rather than `python-binance` to minimize overhead and highlight understanding of fundamental Binance API payload constructions.
