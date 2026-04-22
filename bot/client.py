import hmac
import hashlib
import time
import requests
import os
from .logging_config import logger

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_TESTNET_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_TESTNET_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            logger.error("API credentials not found. Please set them in .env or provide them.")
            raise ValueError("Missing API credentials.")

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method: str, endpoint: str, payload: dict = None):
        if payload is None:
            payload = {}
        
        payload['timestamp'] = int(time.time() * 1000)
        
        query_string = '&'.join([f"{k}={v}" for k, v in payload.items()])
        signature = self._generate_signature(query_string)
        query_string += f"&signature={signature}"

        url = f"{self.BASE_URL}{endpoint}?{query_string}"
        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        logger.info(f"Sending {method} request to {endpoint}")
        try:
            response = requests.request(method, url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info("Request successful.")
            return data
        except requests.exceptions.HTTPError as e:
            error_data = response.json() if response.status_code != 404 else "404 Not Found"
            logger.error(f"HTTPError: {response.status_code} - {error_data}")
            raise Exception(f"API Error: {error_data}")
        except Exception as e:
            logger.error(f"Network/Unexpected Error: {str(e)}")
            raise
