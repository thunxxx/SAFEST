#!/usr/bin/env python3
"""
HTTP Load Testing Tool
"""

import asyncio
import aiohttp
import random
import argparse
import signal
import sys
from typing import List

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
]

class HTTPFlood:
    def __init__(self, target: str, rate: int, duration: int):
        self.target = target if target.startswith('http') else f'http://{target}'
        self.rate = rate
        self.duration = duration
        self.counter = 0
        self.running = True
        
    def get_random_ua(self) -> str:
        return random.choice(USER_AGENTS)
    
    async def send_request(self, session: aiohttp.ClientSession):
        headers = {'User-Agent': self.get_random_ua()}
        try:
            async with session.get(self.target, headers=headers, timeout=5) as response:
                self.counter += 1
                if self.counter % 100 == 0:
                    print(f"Requests sent: {self.counter}")
        except Exception as e:
            pass
    
    async def worker(self):
        async with aiohttp.ClientSession() as session:
            while self.running:
                tasks = [self.send_request(session) for _ in range(self.rate)]
                await asyncio.gather(*tasks, return_exceptions=True)
                await asyncio.sleep(1)
    
    async def run(self):
        print(f"Starting load test against {self.target}")
        print(f"Rate: {self.rate} req/sec, Duration: {self.duration} seconds")
        
        # Set up duration timeout
        asyncio.create_task(self.duration_timer())
        
        # Start workers
        workers = [self.worker() for _ in range(10)]  # 10 concurrent workers
        await asyncio.gather(*workers)
    
    async def duration_timer(self):
        await asyncio.sleep(self.duration)
        self.running = False
        print(f"\nTest completed. Total requests: {self.counter}")

def main():
    parser = argparse.ArgumentParser(description='HTTP Load Testing Tool')
    parser.add_argument('--target', default='target.example.com', help='Target URL')
    parser.add_argument('--rate', type=int, default=50, help='Requests per second')
    parser.add_argument('--duration', type=int, default=30, help='Test duration in seconds')
    
    args = parser.parse_args()
    
    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print("\nStopping test...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the flood
    flood = HTTPFlood(args.target, args.rate, args.duration)
    asyncio.run(flood.run())

if __name__ == '__main__':
    main()