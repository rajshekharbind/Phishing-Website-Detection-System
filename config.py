#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration and Constants Module
Centralized configuration for the entire application
"""

import os
from typing import Dict, List

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

class AppConfig:
    """Application configuration settings."""
    
    # Paths
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
    DATA_DIR = os.path.join(PROJECT_ROOT, 'DataFiles')
    
    # Model configuration
    MODEL_FILE = 'best_model.pickle'
    METRICS_FILE = 'best_model_metrics.json'
    MODEL_PATH = os.path.join(MODELS_DIR, MODEL_FILE)
    METRICS_PATH = os.path.join(MODELS_DIR, METRICS_FILE)
    
    # Application settings
    APP_NAME = "Phishing Website Detector"
    APP_VERSION = "2.0"
    APP_DESCRIPTION = "Advanced ML-powered URL classification system"
    
    # Feature configuration
    TOTAL_FEATURES = 17
    
    # Model parameters
    CONFIDENCE_THRESHOLD = 0.5
    MODEL_TYPE = "Random Forest (Demo) / XGBoost (Production)"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class FeatureConfig:
    """Feature extraction configuration."""
    
    FEATURE_NAMES: List[str] = [
        "IP Address in URL",
        "@ Symbol Present",
        "URL Length (>54 chars)",
        "URL Depth",
        "Redirection (//)",
        "HTTPS in Domain",
        "TinyURL Service",
        "Prefix/Suffix (-)",
        "DNS Record",
        "Web Traffic",
        "Domain Age",
        "Domain End Period",
        "iFrame Present",
        "Mouse Over Event",
        "Right Click Disabled",
        "Web Forwarding",
        "Additional Security Feature"
    ]
    
    FEATURE_DESCRIPTIONS: Dict[str, str] = {
        "IP Address in URL": (
            "Using IP address instead of domain name to hide the real domain"
        ),
        "@ Symbol Present": (
            "@ symbol in URL to bypass URL bar display"
        ),
        "URL Length (>54 chars)": (
            "Very long URLs to hide suspicious parts"
        ),
        "URL Depth": (
            "Number of sub-directories in URL path"
        ),
        "Redirection (//)": (
            "Unusual // redirects outside protocol"
        ),
        "HTTPS in Domain": (
            "HTTPS token in domain to appear legitimate"
        ),
        "TinyURL Service": (
            "URL shortening services (bit.ly, goo.gl, etc)"
        ),
        "Prefix/Suffix (-)": (
            "Dashes in domain to mimic legitimate sites"
        ),
        "DNS Record": (
            "DNS record availability for the domain"
        ),
        "Web Traffic": (
            "Website traffic and Alexa ranking"
        ),
        "Domain Age": (
            "Domain registration age (phishing < 6 months)"
        ),
        "Domain End Period": (
            "Domain expiration timeline"
        ),
        "iFrame Present": (
            "Hidden iframe elements for content embedding"
        ),
        "Mouse Over Event": (
            "JavaScript on mouse over events"
        ),
        "Right Click Disabled": (
            "JavaScript disabling right-click functionality"
        ),
        "Web Forwarding": (
            "Multiple page redirections and forwarding"
        ),
        "Additional Security Feature": (
            "Extra security and content features"
        )
    }
    
    FEATURE_CATEGORIES: Dict[str, List[int]] = {
        "Address Bar Features": [0, 1, 2, 3, 4, 5, 6, 7],
        "Domain Features": [8, 9, 10, 11],
        "HTML & JavaScript Features": [12, 13, 14, 15, 16]
    }

class ModelConfig:
    """Model performance configuration."""
    
    DEFAULT_METRICS = {
        'accuracy': 0.864,
        'precision': 0.862,
        'recall': 0.874,
        'f1_score': 0.868,
        'model_type': 'Random Forest (Demo)',
        'training_samples': 10000,
        'test_accuracy': '86.4%'
    }
    
    EXPECTED_INPUT_SHAPE = (1, 17)
    PREDICTION_CLASS_NAMES = {
        0: "Legitimate",
        1: "Phishing"
    }

class UIConfig:
    """UI and styling configuration."""
    
    # Colors
    COLOR_PHISHING = "#ff6b6b"
    COLOR_LEGITIMATE = "#51cf66"
    COLOR_WARNING = "#ffa94d"
    COLOR_INFO = "#0066cc"
    
    # Icons
    ICON_PHISHING = "🚨"
    ICON_LEGITIMATE = "✅"
    ICON_WARNING = "⚠️"
    ICON_ANALYSIS = "🔍"
    ICON_FEATURE = "📊"
    
    # Text
    PHISHING_TITLE = "PHISHING DETECTED"
    LEGITIMATE_TITLE = "LEGITIMATE SITE"
    
    # Layout
    SIDEBAR_STATE = "expanded"
    PAGE_LAYOUT = "wide"

# ============================================================================
# UTILITY CLASSES
# ============================================================================

class MessageTemplates:
    """Standard message templates for the application."""
    
    MODEL_ERROR = (
        "⚠️ **Model Not Found**\n\n"
        "Please ensure `models/best_model.pickle` exists in the project directory."
    )
    
    FEATURE_ERROR = "❌ Error extracting URL features. Please check the URL format."
    
    PREDICTION_ERROR = "❌ Error making prediction. Please try again."
    
    EMPTY_URL_WARNING = "⚠️ Please enter a valid URL"
    
    PHISHING_WARNING = (
        "⚠️ This URL appears to be **PHISHING**.\n\n"
        "**Do not:**\n"
        "- Click on suspicious links\n"
        "- Enter personal information\n"
        "- Download files from this site\n\n"
    )
    
    LEGITIMATE_INFO = (
        "✓ This URL appears to be **LEGITIMATE**.\n\n"
        "This website seems safe to visit, but always:\n"
        "- Check the address bar\n"
        "- Look for HTTPS padlock\n"
        "- Verify the domain name\n\n"
    )
    
    DISCLAIMER = (
        "⚠️ **Disclaimer:** This tool provides additional security analysis. "
        "No tool is 100% accurate. Always use multiple security checks."
    )

class RiskLevels:
    """Risk level definitions and thresholds."""
    
    CRITICAL = {
        'threshold': 70,
        'label': 'CRITICAL',
        'icon': '🔴',
        'color': '#ff6b6b'
    }
    
    HIGH = {
        'threshold': 50,
        'label': 'HIGH',
        'icon': '🟠',
        'color': '#ff8c42'
    }
    
    MEDIUM = {
        'threshold': 30,
        'label': 'MEDIUM',
        'icon': '🟡',
        'color': '#ffa94d'
    }
    
    LOW = {
        'threshold': 0,
        'label': 'LOW',
        'icon': '🟢',
        'color': '#51cf66'
    }
    
    @classmethod
    def get_risk_level(cls, percentage: float) -> dict:
        """Get risk level definition based on percentage."""
        if percentage >= cls.CRITICAL['threshold']:
            return cls.CRITICAL
        elif percentage >= cls.HIGH['threshold']:
            return cls.HIGH
        elif percentage >= cls.MEDIUM['threshold']:
            return cls.MEDIUM
        else:
            return cls.LOW

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    return url.startswith(('http://', 'https://', 'www.')) or '.' in url

def validate_features(features: list) -> bool:
    """Validate feature list."""
    if not isinstance(features, (list, tuple)):
        return False
    
    if len(features) != FeatureConfig.FEATURE_NAMES.__len__():
        return False
    
    return all(isinstance(f, (int, float)) for f in features)

# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("APPLICATION CONFIGURATION")
    print("=" * 70)
    
    print(f"\n📁 Project Structure:")
    print(f"   Root: {AppConfig.PROJECT_ROOT}")
    print(f"   Models: {AppConfig.MODELS_DIR}")
    print(f"   Data: {AppConfig.DATA_DIR}")
    
    print(f"\n📊 Model Configuration:")
    print(f"   Type: {AppConfig.MODEL_TYPE}")
    print(f"   Path: {AppConfig.MODEL_PATH}")
    print(f"   Total Features: {AppConfig.TOTAL_FEATURES}")
    
    print(f"\n✨ UI Configuration:")
    print(f"   Primary Color: {UIConfig.COLOR_PHISHING}")
    print(f"   Success Color: {UIConfig.COLOR_LEGITIMATE}")
    print(f"   Layout: {UIConfig.PAGE_LAYOUT}")
    
    print(f"\n📈 Default Metrics:")
    for key, value in ModelConfig.DEFAULT_METRICS.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
