#!/usr/bin/env python3
"""
🔍 PHISHING DETECTOR - AUTOMATED TEST SUITE
======================================================================

Run comprehensive tests to verify the application works correctly.

Usage:
    python test_app.py
    
Expected: All tests pass ✅
"""

import sys
import os
from pathlib import Path

# Add project to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"✓ {text}")
    print("=" * 70)


def test_imports() -> bool:
    """Test that all required modules can be imported."""
    print_header("TEST 1: CHECKING IMPORTS")
    
    try:
        print("  → Importing streamlit...", end="")
        import streamlit
        print(" ✅")
        
        print("  → Importing sklearn...", end="")
        import sklearn
        print(" ✅")
        
        print("  → Importing pandas...", end="")
        import pandas
        print(" ✅")
        
        print("  → Importing numpy...", end="")
        import numpy
        print(" ✅")
        
        print("  → Importing requests...", end="")
        import requests
        print(" ✅")
        
        print("  → Importing URLFeatureExtraction...", end="")
        from URLFeatureExtraction import havingIP
        print(" ✅")
        
        print("  → Importing config...", end="")
        from config import AppConfig, FeatureConfig
        print(" ✅")
        
        print("  → Importing feature_extractor...", end="")
        from feature_extractor import FeatureExtractor
        print(" ✅")
        
        print("  → Importing safe_web_traffic...", end="")
        from safe_web_traffic import safe_web_traffic
        print(" ✅")
        
        print("\n✅ All imports successful!\n")
        return True
        
    except ImportError as e:
        print(f" ❌\n\n❌ Import Error: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def test_model_loading() -> bool:
    """Test that the model can be loaded."""
    print_header("TEST 2: LOADING ML MODEL")
    
    try:
        import pickle
        from config import AppConfig
        
        model_path = AppConfig.MODEL_PATH
        print(f"  → Looking for model at: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"  ❌ Model file not found at {model_path}")
            return False
        
        print(f"  → Loading model...", end="")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(" ✅")
        
        print(f"  → Model type: {type(model).__name__}")
        print(f"  → Model classes: {model.classes_}")
        
        print("\n✅ Model loaded successfully!\n")
        return True
        
    except Exception as e:
        print(f" ❌\n\n❌ Error: {e}")
        return False


def test_feature_extraction() -> bool:
    """Test feature extraction with sample URLs."""
    print_header("TEST 3: FEATURE EXTRACTION")
    
    try:
        from feature_extractor import FeatureExtractor
        from config import FeatureConfig
        
        test_urls = [
            "https://www.google.com",
            "https://www.github.com",
            "http://192.168.1.1",
        ]
        
        print(f"  Total features expected: {len(FeatureConfig.FEATURE_NAMES)}\n")
        
        for url in test_urls:
            print(f"  → Testing: {url}")
            features = FeatureExtractor.extract(url)
            
            if features is None:
                print(f"    ❌ Failed to extract features")
                return False
            
            if len(features) != 17:
                print(f"    ❌ Got {len(features)} features, expected 17")
                return False
            
            print(f"    ✅ Extracted {len(features)} features")
            print(f"       First 5: {features[:5]}")
        
        print("\n✅ Feature extraction working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prediction() -> bool:
    """Test model predictions with extracted features."""
    print_header("TEST 4: MODEL PREDICTION")
    
    try:
        import pickle
        from feature_extractor import FeatureExtractor
        from config import AppConfig, ModelConfig
        
        # Load model
        with open(AppConfig.MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        test_url = "https://www.google.com"
        print(f"  → Testing URL: {test_url}\n")
        
        # Extract features
        print(f"  → Extracting features...", end="")
        features = FeatureExtractor.extract(test_url)
        print(" ✅")
        
        if not features or len(features) != 17:
            print(f"  ❌ Feature extraction returned wrong count")
            return False
        
        # Make prediction
        print(f"  → Making prediction...", end="")
        prediction = model.predict([features])[0]
        confidence = model.predict_proba([features])[0]
        print(" ✅")
        
        # Format result
        label = "LEGITIMATE" if prediction == 0 else "PHISHING"
        confidence_pct = confidence[prediction] * 100
        
        print(f"  → Prediction: {label}")
        print(f"  → Confidence: {confidence_pct:.1f}%")
        print(f"  → Probabilities: Legitimate={confidence[0]:.2%}, Phishing={confidence[1]:.2%}")
        
        print("\n✅ Prediction working!\n")
        return True
        
    except Exception as e:
        print(f" ❌\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration() -> bool:
    """Test that configuration loads correctly."""
    print_header("TEST 5: CONFIGURATION")
    
    try:
        from config import (
            AppConfig, FeatureConfig, ModelConfig, 
            UIConfig, MessageTemplates, RiskLevels
        )
        
        print(f"  → AppConfig.MODEL_PATH: {AppConfig.MODEL_PATH}")
        print(f"  → Feature count: {len(FeatureConfig.FEATURE_NAMES)}")
        print(f"  → Model accuracy: {ModelConfig.ACCURACY:.1%}")
        print(f"  → UI colors configured: ✅")
        print(f"  → Messages templates loaded: ✅")
        print(f"  → Risk levels defined: ✅")
        
        # Validate features
        if len(FeatureConfig.FEATURE_NAMES) != 17:
            print(f"\n  ❌ Expected 17 features, got {len(FeatureConfig.FEATURE_NAMES)}")
            return False
        
        print("\n✅ Configuration valid!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analysis() -> bool:
    """Test feature analysis."""
    print_header("TEST 6: FEATURE ANALYSIS")
    
    try:
        from feature_extractor import FeatureExtractor, FeatureAnalyzer
        
        url = "https://www.google.com"
        print(f"  → Analyzing: {url}\n")
        
        features = FeatureExtractor.extract(url)
        if not features:
            print(f"  ❌ Failed to extract features")
            return False
        
        analysis = FeatureAnalyzer.analyze(features)
        
        print(f"  → High risk features: {analysis['high_risk']}")
        print(f"  → Low risk features: {analysis['low_risk']}")
        print(f"  → Risk percentage: {analysis['risk_percentage']:.1f}%")
        print(f"  → Risk level: {analysis['risk_level']}")
        
        print("\n✅ Feature analysis working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests() -> None:
    """Run all tests and report results."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔍 PHISHING DETECTOR - TEST SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    tests = [
        ("Imports", test_imports),
        ("Model Loading", test_model_loading),
        ("Feature Extraction", test_feature_extraction),
        ("Model Prediction", test_prediction),
        ("Configuration", test_configuration),
        ("Feature Analysis", test_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "🎉 " * 20)
        print("  ALL TESTS PASSED! ✨")
        print("  Application is ready to use!")
        print("  Run: streamlit run main_app.py")
        print("🎉 " * 20 + "\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("   Please check errors above\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
