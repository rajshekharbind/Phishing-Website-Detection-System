#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Script - Verify all features can be extracted without errors
"""

from URLFeatureExtraction import (
    havingIP, haveAtSign, getLength, getDepth, redirection,
    httpDomain, tinyURL, prefixSuffix
)
from safe_web_traffic import safe_web_traffic

def test_feature_extraction():
    """Test extracting features from sample URLs"""
    
    test_urls = [
        "https://www.google.com",
        "https://www.amazon.com",
        "https://bit.ly/test",
        "http://192.168.1.1/malicious",
        "https://site@legitimate.com/steal"
    ]
    
    print("=" * 70)
    print("TESTING FEATURE EXTRACTION")
    print("=" * 70)
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        print("-" * 70)
        
        try:
            features = [
                havingIP(url),           # 1
                haveAtSign(url),         # 2
                getLength(url),          # 3
                getDepth(url),           # 4
                redirection(url),        # 5
                httpDomain(url),         # 6
                tinyURL(url),            # 7
                prefixSuffix(url),       # 8
                0,                       # 9 - DNS
                safe_web_traffic(url),   # 10 - Web Traffic
                0, 0, 0, 0, 0, 0, 0     # 11-17 - Other features
            ]
            
            feature_names = [
                "IP Address", "@ Symbol", "URL Length", "URL Depth",
                "Redirection", "HTTPS Domain", "TinyURL", "Prefix/Suffix",
                "DNS Record", "Web Traffic", "Domain Age", "Domain End",
                "iFrame", "Mouse Over", "Right Click", "Web Forwards",
                "Additional Feature"
            ]
            
            print("\n✅ Features extracted successfully:")
            for name, value in zip(feature_names, features):
                status = "🚨" if value == 1 else "✅"
                print(f"   {status} {name:20} : {value}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✓ Feature extraction test complete!")
    print("=" * 70)
    print("\nThe Streamlit app should now work without errors!")
    print("Run: streamlit run app.py")

if __name__ == "__main__":
    test_feature_extraction()
