#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Feature Extraction Utility - Enhanced Version
Professional wrapper around URLFeatureExtraction functions

Provides type hints, error handling, and detailed feature extraction
"""

from typing import List, Tuple, Optional
import logging
from URLFeatureExtraction import (
    havingIP, haveAtSign, getLength, getDepth, redirection,
    httpDomain, tinyURL, prefixSuffix
)
from safe_web_traffic import safe_web_traffic

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """Professional feature extraction class with error handling."""
    
    # Feature configuration
    TOTAL_FEATURES = 17
    FEATURE_NAMES = [
        "IP Address in URL",
        "@ Symbol Present",
        "URL Length",
        "URL Depth",
        "Redirection //",
        "HTTPS in Domain",
        "TinyURL Service",
        "Prefix/Suffix",
        "DNS Record",
        "Web Traffic",
        "Domain Age",
        "Domain End",
        "iFrame",
        "Mouse Over",
        "Right Click",
        "Web Forwards",
        "Additional Feature"
    ]
    
    @staticmethod
    def extract(url: str) -> Optional[List[int]]:
        """
        Extract all 17 features from a URL.
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            List[int]: List of 17 binary/numeric features or None if error
            
        Raises:
            ValueError: If URL is invalid
            Exception: If feature extraction fails
        """
        if not url or not isinstance(url, str):
            raise ValueError("Invalid URL provided")
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            features = [
                FeatureExtractor._safe_extract(havingIP, url, "IP Address", 0),
                FeatureExtractor._safe_extract(haveAtSign, url, "@ Symbol", 0),
                FeatureExtractor._safe_extract(getLength, url, "URL Length", 0),
                FeatureExtractor._safe_extract(getDepth, url, "URL Depth", 0),
                FeatureExtractor._safe_extract(redirection, url, "Redirection", 0),
                FeatureExtractor._safe_extract(httpDomain, url, "HTTPS Domain", 0),
                FeatureExtractor._safe_extract(tinyURL, url, "TinyURL", 0),
                FeatureExtractor._safe_extract(prefixSuffix, url, "Prefix/Suffix", 0),
                0,  # DNS Record - requires whois
            ]
            
            # Web traffic with safe fallback
            web_traffic_val = FeatureExtractor._safe_extract(
                safe_web_traffic, url, "Web Traffic", 0
            )
            features.append(web_traffic_val)
            
            # Advanced features (require additional data)
            features.extend([0] * 7)  # Features 11-17
            
            # Validate feature count
            if len(features) != FeatureExtractor.TOTAL_FEATURES:
                raise ValueError(
                    f"Feature count mismatch: expected {FeatureExtractor.TOTAL_FEATURES}, "
                    f"got {len(features)}"
                )
            
            logger.info(f"Successfully extracted {len(features)} features from URL")
            return features
        
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return None
    
    @staticmethod
    def _safe_extract(func, url: str, feature_name: str, default: int) -> int:
        """
        Safely extract a single feature with error handling.
        
        Args:
            func: Feature extraction function
            url (str): URL to process
            feature_name (str): Name of feature (for logging)
            default (int): Default value if extraction fails
            
        Returns:
            int: Feature value or default
        """
        try:
            result = func(url)
            return int(result) if result is not None else default
        except Exception as e:
            logger.warning(f"Error extracting {feature_name}: {str(e)}")
            return default
    
    @staticmethod
    def get_feature_description(feature_index: int) -> str:
        """Get description for a feature by index."""
        descriptions = {
            0: "Checks if URL contains IP address instead of domain",
            1: "Detects @ symbol which can hide the real address",
            2: "Analyzes URL length (phishing URLs are often longer)",
            3: "Counts subdirectories in the URL path",
            4: "Detects unusual // redirects in the URL",
            5: "Checks if http/https appears in the domain part",
            6: "Identifies URL shortening services (bit.ly, etc)",
            7: "Detects dashes in domain name",
            8: "Validates DNS record existence",
            9: "Analyzes website traffic and popularity",
            10: "Checks domain registration age",
            11: "Checks domain expiration timeline",
            12: "Detects hidden iframe elements",
            13: "Detects JavaScript mouse over events",
            14: "Checks if right-click is disabled",
            15: "Detects multiple page forwarding",
            16: "Additional security feature check"
        }
        return descriptions.get(feature_index, "Unknown feature")

class FeatureAnalyzer:
    """Analyze and interpret extracted features."""
    
    RISK_LEVELS = {
        'HIGH': 1,      # Feature present = suspicious
        'LOW': 0,       # Feature absent = normal
    }
    
    @staticmethod
    def analyze(features: List[int]) -> dict:
        """
        Analyze features and return risk assessment.
        
        Args:
            features (List[int]): List of feature values
            
        Returns:
            dict: Risk assessment and statistics
        """
        high_risk_count = sum(1 for f in features if f == 1)
        low_risk_count = len(features) - high_risk_count
        risk_percentage = (high_risk_count / len(features)) * 100
        
        return {
            'high_risk': high_risk_count,
            'low_risk': low_risk_count,
            'total': len(features),
            'risk_percentage': risk_percentage,
            'risk_level': FeatureAnalyzer._determine_risk_level(risk_percentage)
        }
    
    @staticmethod
    def _determine_risk_level(percentage: float) -> str:
        """Determine overall risk level from percentage."""
        if percentage >= 70:
            return "CRITICAL"
        elif percentage >= 50:
            return "HIGH"
        elif percentage >= 30:
            return "MEDIUM"
        else:
            return "LOW"

# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://bit.ly/test",
        "https://site@fake.com"
    ]
    
    print("=" * 70)
    print("FEATURE EXTRACTION TEST")
    print("=" * 70)
    
    for url in test_urls:
        print(f"\n🔍 Analyzing: {url}")
        print("-" * 70)
        
        features = FeatureExtractor.extract(url)
        
        if features:
            analysis = FeatureAnalyzer.analyze(features)
            print(f"✅ Features extracted: {len(features)}")
            print(f"🔴 High risk features: {analysis['high_risk']}")
            print(f"🟢 Low risk features: {analysis['low_risk']}")
            print(f"📊 Risk percentage: {analysis['risk_percentage']:.1f}%")
            print(f"⚠️ Risk level: {analysis['risk_level']}")
        else:
            print("❌ Error extracting features")
    
    print("\n" + "=" * 70)
