import click
from dotenv import load_dotenv
from bot.logging_config import logger
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.client import BinanceFuturesClient
from bot.orders import place_order

# Load environment variables from .env file
load_dotenv()

@click.command()
@click.option('--symbol', prompt='Trading Symbol (e.g., BTCUSDT)', help='The symbol to trade.')
@click.option('--side', prompt='Order Side (BUY/SELL)', help='Order side: BUY or SELL.')
@click.option('--type', 'order_type', prompt='Order Type (MARKET/LIMIT)', help='Order type: MARKET or LIMIT.')
@click.option('--quantity', prompt='Quantity', type=float, help='Quantity to trade.')
@click.option('--price', type=float, default=None, help='Price for LIMIT orders.')
def main(symbol, side, order_type, quantity, price):
    """
    Binance Futures Testnet Trading Bot
    Places orders on the testnet according to the provided parameters.
    """
    click.echo("\n--- Binance Futures Trade Config ---")
    click.echo(f"Symbol: {symbol}")
    click.echo(f"Side: {side}")
    click.echo(f"Type: {order_type}")
    click.echo(f"Quantity: {quantity}")
    if price:
        click.echo(f"Price: {price}")
    click.echo("------------------------------------\n")

    try:
        # Validate Inputs
        symbol_v = validate_symbol(symbol)
        side_v = validate_side(side)
        type_v = validate_order_type(order_type)
        qty_v = validate_quantity(quantity)
        price_v = validate_price(price, type_v)

        if type_v == "LIMIT" and not price_v:
            price_str = click.prompt("Price is required for LIMIT orders. Enter price", type=float)
            price_v = validate_price(price_str, type_v)

        client = BinanceFuturesClient()
        response = place_order(client, symbol_v, side_v, type_v, qty_v, price_v)
        
        click.secho("[SUCCESS] Order Placed Successfully!", fg='green')
        click.echo(f"Order ID: {response.get('orderId')}")
        click.echo(f"Status: {response.get('status')}")
        click.echo(f"Executed Qty: {response.get('executedQty')}")
        click.echo(f"Avg Price: {response.get('avgPrice')}")

    except ValueError as ve:
        click.secho(f"[ERROR] Input Validation Error: {ve}", fg='red')
        logger.error(f"CLI Input Error: {ve}")
    except Exception as e:
        click.secho(f"[ERROR] Order Execution Failed. See bot.log for details.", fg='red')
        # Error is already logged in lower layers

if __name__ == '__main__':
    main()
