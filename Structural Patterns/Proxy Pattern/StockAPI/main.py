"""
Proxy Design Pattern: Production-Style Caching Example
------------------------------------------------------
This script demonstrates the Proxy Pattern using a Stock API scenario.
It simulates:
1. An expensive External API (The Real Subject).
2. A Smart Caching Proxy that reduces costs and latency.
3. Client code that works seamlessly with either.

Usage:
Run this file directly: `python proxy_pattern_demo.py`
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

# --- 1. The Data Object ---
@dataclass
class StockData:
    """
    A simple data container for passing stock information.
    """
    ticker: str
    price: float
    timestamp: float

# --- 2. The Subject Interface ---
class StockService(ABC):
    """
    The Common Interface.
    Both the Real API and the Proxy must implement this.
    The client relies on this contract.
    """
    @abstractmethod
    def get_stock_price(self, ticker: str) -> StockData:
        pass

# --- 3. The Real Subject (Heavy/Expensive) ---
class ExternalStockAPI(StockService):
    """
    Represents the actual third-party service.
    In a real app, this would make HTTP requests (e.g., using `requests`).
    """
    def get_stock_price(self, ticker: str) -> StockData:
        print(f"   [Network] Connecting to Wall St. API for {ticker}...")
        
        # Simulate network latency (The "Heavy" part)
        time.sleep(1.5) 
        
        # Simulate fetching data (Mock database)
        mock_prices = {
            "AAPL": 150.25, 
            "GOOGL": 2800.50, 
            "MSFT": 310.10,
            "TSLA": 720.00
        }
        price = mock_prices.get(ticker, 0.0)
        
        print(f"   [Network] $$$ CHARGED: API Call completed for {ticker}")
        return StockData(ticker, price, time.time())

# --- 4. The Proxy (Smart/Protection/Cache) ---
class CachingProxy(StockService):
    """
    The Proxy controls access to the Real Subject.
    It adds caching logic to save time and money.
    """
    def __init__(self, real_service: StockService, cache_ttl_seconds: int):
        self._real_service = real_service
        self._cache_ttl = cache_ttl_seconds
        # Dictionary acts as our in-memory storage: { "AAPL": StockData(...) }
        self._cache: Dict[str, StockData] = {} 

    def get_stock_price(self, ticker: str) -> StockData:
        print(f"[Proxy] Request received for {ticker}")
        
        current_time = time.time()
        cached_item = self._cache.get(ticker)

        # 1. Check if we have data in the cache
        if cached_item:
            age = current_time - cached_item.timestamp
            
            # 2. Check if the data is fresh (Virtual Proxy logic)
            if age < self._cache_ttl:
                print(f"   [Cache] HIT. Data is only {age:.2f}s old. Returning local copy.")
                return cached_item
            else:
                print(f"   [Cache] EXPIRED. Data is {age:.2f}s old. Refreshing...")
        else:
            print("   [Cache] MISS. No data found.")

        # 3. If missing or expired, delegate to the Real Subject
        # This is the only time the heavy operation runs.
        fresh_data = self._real_service.get_stock_price(ticker)
        
        # 4. Save result to cache for future requests
        self._cache[ticker] = fresh_data
        
        return fresh_data

# --- 5. The Client Code ---
def client_app(service: StockService, ticker: str):
    """
    The client logic. Notice it is loosely coupled; it works with
    ANY class that implements StockService (Proxy or Real).
    """
    start_time = time.time()
    data = service.get_stock_price(ticker)
    end_time = time.time()
    
    print(f"   -> Result: {data.ticker} is ${data.price}")
    print(f"   -> Time taken: {end_time - start_time:.4f} seconds\n")

# --- 6. Execution Block ---
if __name__ == "__main__":
    print("=== STARTING STOCK DASHBOARD ===\n")

    # A. Setup
    real_api = ExternalStockAPI()
    # We wrap the real API with our Proxy.
    # Cache expires every 5 seconds for this demo.
    secure_service = CachingProxy(real_api, cache_ttl_seconds=5)

    # B. Simulation
    print("--- 1. First Request (Cold Start) ---")
    # Cache is empty. This hits the network (slow).
    client_app(secure_service, "AAPL")

    print("--- 2. Second Request (Immediate Follow-up) ---")
    # Cache is fresh. This hits the proxy only (fast).
    client_app(secure_service, "AAPL")

    print("--- 3. Sleeping for 6 seconds (Simulating user delay) ---")
    time.sleep(6)

    print("--- 4. Third Request (After TTL) ---")
    # Cache has expired. This hits the network again (slow).
    client_app(secure_service, "AAPL")