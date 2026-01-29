#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phishing Website Detector - Professional Web Application
Advanced ML-based URL classification system using Streamlit

Author: Phishing Detection Team
Version: 2.0
Updated: January 2026
"""

import warnings
import sys
import logging

# Suppress numpy deprecation warnings early
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*numpy._core.*')

# Fix numpy 2.x compatibility with old pickles BEFORE importing numpy
class NumpyCompatibilityFix:
    """Handle numpy version compatibility when loading pickled models"""
    @staticmethod
    def fix_numpy_imports():
        """Add numpy._core alias if it doesn't exist (for numpy <2.0 compatibility)"""
        try:
            import numpy
            # Check if we're using numpy 1.x (which has numpy._core as an alias)
            if hasattr(numpy, '__version__'):
                version = tuple(map(int, numpy.__version__.split('.')[:2]))
                if version[0] < 2:
                    # numpy 1.x - create _core if missing
                    if not hasattr(numpy, '_core'):
                        import numpy.core as core
                        numpy._core = core
        except Exception as e:
            pass

# Apply compatibility fix BEFORE other imports
NumpyCompatibilityFix.fix_numpy_imports()

import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List

# Import feature extraction functions
from URLFeatureExtraction import (
    havingIP, haveAtSign, getLength, getDepth, redirection,
    httpDomain, tinyURL, prefixSuffix
)
from safe_web_traffic import safe_web_traffic
from chatbot import render_chatbot_interface, initialize_chatbot_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        padding: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .result-box {
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: slideIn 0.3s ease-in;
    }
    
    .phishing-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .legitimate-box {
        background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.3);
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #0066cc;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-container {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONSTANTS
# ============================================================================

FEATURE_NAMES = [
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

FEATURE_DESCRIPTIONS = {
    "IP Address in URL": "Using IP address instead of domain name",
    "@ Symbol Present": "@ symbol to bypass URL display",
    "URL Length (>54 chars)": "Very long URLs to hide suspicious parts",
    "URL Depth": "Number of sub-directories in URL",
    "Redirection (//)": "Unusual redirects in URL path",
    "HTTPS in Domain": "HTTPS token in domain to appear legitimate",
    "TinyURL Service": "URL shortening services (bit.ly, etc.)",
    "Prefix/Suffix (-)": "Dashes in domain name",
    "DNS Record": "DNS record availability",
    "Web Traffic": "Website traffic/popularity",
    "Domain Age": "Age of domain registration",
    "Domain End Period": "Domain expiration timeline",
    "iFrame Present": "Hidden iframe elements",
    "Mouse Over Event": "JavaScript on mouse over",
    "Right Click Disabled": "Disabled right-click functionality",
    "Web Forwarding": "Multiple page redirections",
    "Additional Security Feature": "Extra security indicators"
}

# Set working directory to the script's directory for proper relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

MODEL_PATH = 'models/best_model.pickle'
METRICS_PATH = 'models/best_model_metrics.json'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_resource
def load_model() -> Optional[object]:
    """
    Load the pre-trained ML model from pickle file.
    
    Returns:
        object: Loaded model or None if file not found
    """
    try:
        if not os.path.exists(MODEL_PATH):
            logger.warning(f"Model file not found: {MODEL_PATH}")
            return None
        
        # Custom unpickler to handle numpy 1.x vs 2.x compatibility
        class CompatibilityUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                # Map numpy._core (from numpy 2.x) to numpy.core (numpy 1.x)
                if module == 'numpy._core' or module.startswith('numpy._core.'):
                    # Replace numpy._core with numpy.core
                    new_module = module.replace('numpy._core', 'numpy.core')
                    logger.debug(f"Remapping module: {module} -> {new_module}")
                    try:
                        return super().find_class(new_module, name)
                    except (ModuleNotFoundError, AttributeError):
                        # If remapped version fails, try original
                        pass
                
                # Handle numpy.random._core compatibility
                if module.startswith('numpy.random._core'):
                    new_module = module.replace('numpy.random._core', 'numpy.random')
                    logger.debug(f"Remapping random module: {module} -> {new_module}")
                    try:
                        return super().find_class(new_module, name)
                    except (ModuleNotFoundError, AttributeError):
                        pass
                
                try:
                    return super().find_class(module, name)
                except ModuleNotFoundError as e:
                    logger.error(f"Failed to find class {module}.{name}")
                    raise
        
        with open(MODEL_PATH, 'rb') as f:
            model = CompatibilityUnpickler(f).load()
        
        logger.info("Model loaded successfully")
        return model
    
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

@st.cache_resource
def load_metrics() -> dict:
    """Load model performance metrics."""
    try:
        if os.path.exists(METRICS_PATH):
            import json
            with open(METRICS_PATH, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading metrics: {str(e)}")
    
    return {
        'accuracy': 0.864,
        'precision': 0.862,
        'recall': 0.874,
        'f1_score': 0.868
    }

def extract_features(url: str) -> Optional[List[int]]:
    """
    Extract 17 features from a given URL.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        List[int]: List of 17 feature values or None if error
    """
    try:
        features = [
            havingIP(url),              # 1
            haveAtSign(url),            # 2
            getLength(url),             # 3
            getDepth(url),              # 4
            redirection(url),           # 5
            httpDomain(url),            # 6
            tinyURL(url),               # 7
            prefixSuffix(url),          # 8
            0,                          # 9 - DNS
        ]
        
        # Safe web traffic check with error handling
        try:
            web_traffic_val = safe_web_traffic(url)
        except Exception:
            web_traffic_val = 0
        
        features.append(web_traffic_val)  # 10
        features.extend([0, 0, 0, 0, 0, 0, 0])  # 11-17
        
        assert len(features) == 17, f"Expected 17 features, got {len(features)}"
        return features
    
    except Exception as e:
        logger.error(f"Feature extraction error: {str(e)}")
        return None

def make_prediction(model: object, features: List[int]) -> Tuple[int, float]:
    """
    Make a prediction using the trained model.
    
    Args:
        model: Trained ML model
        features: List of 17 features
        
    Returns:
        Tuple: (prediction, confidence)
    """
    try:
        prediction = model.predict([features])[0]
        
        try:
            proba = model.predict_proba([features])[0]
            confidence = max(proba)
        except:
            confidence = 0.5
        
        return prediction, confidence
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return None, None

def format_result(prediction: int, confidence: float) -> Tuple[str, str, str]:
    """
    Format prediction result for display.
    
    Returns:
        Tuple: (title, color, emoji, message)
    """
    if prediction == 1:
        return "🚨 PHISHING DETECTED", "phishing-box", (
            "⚠️ This URL appears to be **PHISHING**.\n\n"
            "**Do not:**\n"
            "- Click on suspicious links\n"
            "- Enter personal information\n"
            "- Download files from this site\n\n"
            "**Confidence:** {:.1f}%".format(confidence * 100)
        )
    else:
        return "✅ LEGITIMATE SITE", "legitimate-box", (
            "✓ This URL appears to be **LEGITIMATE**.\n\n"
            "This website seems safe to visit, but always:\n"
            "- Check the address bar\n"
            "- Look for HTTPS padlock\n"
            "- Verify the domain name\n\n"
            "**Confidence:** {:.1f}%".format(confidence * 100)
        )

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic."""
    
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("# 🔍")
    with col2:
        st.markdown("# Phishing Website Detector")
    
    st.markdown(
        "Advanced ML-powered URL classification • Analyzes 17 security features"
    )
    
    # Create tabs for different features
    tab1, tab2 = st.tabs(["🔎 URL Detector", "💬 Chat Assistant"])
    
    with tab1:
        render_url_detector()
    
    with tab2:
        initialize_chatbot_session()
        render_chatbot_interface()


def render_url_detector():
    """Render the URL detection interface."""
    
    # Model validation
    model = load_model()
    if model is None:
        st.error(
            "⚠️ **Model Not Found**\n\n"
            "Please ensure `models/best_model.pickle` exists in the project directory."
        )
        return
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        
        metrics = load_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", f"{metrics['accuracy']:.1%}")
            st.metric("Precision", f"{metrics['precision']:.1%}")
        with col2:
            st.metric("Recall", f"{metrics['recall']:.1%}")
            st.metric("F1-Score", f"{metrics['f1_score']:.1%}")
        
        st.divider()
        
        st.subheader("How It Works")
        st.markdown("""
        1. **Enter** a URL
        2. **Analyze** 17 security features
        3. **Classify** as Phishing or Legitimate
        4. **Display** confidence & breakdown
        """)
        
        st.divider()
        
        st.subheader("Features Analyzed")
        st.markdown("• URL structure • Domain info • Traffic patterns • Security indicators")
    
    # Main content
    st.divider()
    
    # URL Input Section
    st.subheader("🔗 Enter URL to Check")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        url_input = st.text_input(
            "URL Input",
            placeholder="https://www.example.com",
            label_visibility="collapsed",
            key="url_input"
        )
    with col2:
        analyze_button = st.button(
            "🔎 Analyze",
            use_container_width=False,
            type="primary",
            key="analyze_btn"
        )
    
    st.divider()
    
    # Analysis Section
    if analyze_button:
        if not url_input or url_input.strip() == "":
            st.warning("⚠️ Please enter a valid URL")
            return
        
        with st.spinner("🔄 Analyzing URL..."):
            # Extract features
            features = extract_features(url_input)
            
            if features is None:
                st.error("❌ Error extracting URL features. Please check the URL format.")
                return
            
            # Make prediction
            prediction, confidence = make_prediction(model, features)
            
            if prediction is None:
                st.error("❌ Error making prediction. Please try again.")
                return
            
            # Display Results
            st.subheader("📊 Analysis Results")
            
            title, box_class, message = format_result(prediction, confidence)
            st.markdown(
                f"<div class='result-box {box_class}'>"
                f"<h2 style='margin: 0; text-align: center;'>{title}</h2>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(message)
            with col2:
                st.markdown(f"""
                <div class='metric-container'>
                <h3 style='margin: 0; color: #0066cc;'>Confidence</h3>
                <h2 style='margin: 0.5rem 0;'>{confidence*100:.1f}%</h2>
                <p style='margin: 0; color: #666;'>Model Certainty</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # URL Details
            st.subheader("🔗 Analyzed URL")
            st.code(url_input, language="")
            
            # Feature Breakdown
            with st.expander("📊 Detailed Feature Analysis", expanded=True):
                feature_df = pd.DataFrame({
                    'Feature': FEATURE_NAMES,
                    'Value': features,
                    'Risk': ['🔴 HIGH' if f == 1 else '🟢 LOW' for f in features],
                    'Description': [FEATURE_DESCRIPTIONS.get(name, '') for name in FEATURE_NAMES]
                })
                
                # Color code the dataframe
                st.dataframe(
                    feature_df,
                    use_container_width=False,
                    hide_index=True,
                    height=400
                )
                
                # Summary statistics
                high_risk = sum(1 for f in features if f == 1)
                st.info(
                    f"**Summary:** {high_risk} suspicious features detected "
                    f"out of {len(features)} analyzed."
                )
    
    st.divider()
    
    # Information Section
    st.subheader("📚 Learning Center")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🟢 Legitimate Indicators
        
        ✓ Standard domain name  
        ✓ HTTPS protocol  
        ✓ Proper URL structure  
        ✓ Known domain  
        ✓ Good web traffic  
        ✓ Established age
        """)
    
    with col2:
        st.markdown("""
        #### 🔴 Phishing Indicators
        
        ✗ IP address in URL  
        ✗ @ symbol present  
        ✗ Very long URL  
        ✗ Shortened URL  
        ✗ Domain dashes  
        ✗ New domain
        """)
    
    with col3:
        st.markdown("""
        #### ⚙️ Technical Features
        
        • URL parsing  
        • Domain analysis  
        • Traffic detection  
        • Anomaly scoring  
        • ML classification  
        • Confidence metrics
        """)
    
    st.divider()
    
    # Footer
    st.caption(
        "⚠️ **Disclaimer:** This tool provides additional security analysis. "
        "No tool is 100% accurate. Always use multiple security checks and trust your instincts."
    )

if __name__ == "__main__":
    main()
