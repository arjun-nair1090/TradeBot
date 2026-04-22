from .client import BinanceFuturesClient
from .logging_config import logger

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    endpoint = "/fapi/v1/order"
    
    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"
    
    logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}.")
    
    try:
        response = client.send_signed_request("POST", endpoint, payload)
        
        if response:
            logger.info(f"Order Success - ID: {response.get('orderId')}, Status: {response.get('status')}")
            return response
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        raise
