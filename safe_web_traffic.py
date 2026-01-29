#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Safe Web Traffic Checker
Attempts to check web traffic but returns 0 if network fails
"""

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import socket

def safe_web_traffic(url):
    """
    Safe version of web_traffic that handles network errors
    Returns 0 (safe/legitimate) if cannot connect to Alexa
    """
    try:
        # Set a timeout to avoid hanging
        socket.setdefaulttimeout(5)
        
        # URL encode the input
        url_encoded = urllib.parse.quote(url)
        
        # Try to fetch from Alexa
        try:
            response = urllib.request.urlopen(
                f"http://data.alexa.com/data?cli=10&dat=s&url={url_encoded}",
                timeout=5
            )
            rank_data = BeautifulSoup(response.read(), "xml").find("REACH")
            
            if rank_data and 'RANK' in rank_data.attrs:
                rank = int(rank_data['RANK'])
                # If rank < 100000, consider it popular (0 = legitimate)
                # If rank >= 100000, consider it suspicious (1 = phishing)
                return 1 if rank >= 100000 else 0
            else:
                # Cannot find rank - assume suspicious
                return 1
                
        except (urllib.error.URLError, socket.timeout, ConnectionError):
            # Network error - assume safe (0 = legitimate)
            # This is a safe default when we can't verify
            return 0
            
    except Exception:
        # Any other error - return safe default
        return 0

if __name__ == "__main__":
    # Test the function
    test_urls = [
        "https://www.google.com",
        "https://www.amazon.com",
        "https://bit.ly/test"
    ]
    
    print("Testing safe_web_traffic function:")
    for url in test_urls:
        try:
            result = safe_web_traffic(url)
            status = "⚠️ Suspicious" if result == 1 else "✅ Legitimate"
            print(f"  {url:40} -> {status}")
        except Exception as e:
            print(f"  {url:40} -> Error: {e}")
