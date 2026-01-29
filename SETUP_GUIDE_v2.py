"""
🔍 PHISHING WEBSITE DETECTION - SETUP & TESTING GUIDE
======================================================================

This guide walks you through setting up and testing the professional v2.0
implementation of the Phishing Website Detection system.
"""

# ======================================================================
# STEP 1: ENVIRONMENT SETUP
# ======================================================================

"""
1a. Open PowerShell or Command Prompt
    Navigate to project folder:
    
    cd "c:\Users\bramh\Downloads\Phishing-Website-Detection-by-Ml-Techniq\Phishing-Website"

1b. Create a virtual environment (RECOMMENDED):
    
    python -m venv venv
    
    Then activate it:
    - Windows: venv\Scripts\activate
    - Mac/Linux: source venv/bin/activate

1c. Install dependencies:
    
    pip install -r requirements.txt
    
    This installs:
    - streamlit (web interface)
    - scikit-learn (ML model)
    - pandas/numpy (data processing)
    - beautifulsoup4 (web scraping)
    - requests (HTTP library)
    - And other utilities
"""

# ======================================================================
# STEP 2: VERIFY FILES ARE PRESENT
# ======================================================================

"""
Check that all required files exist:

✓ main_app.py              ← NEW: Main application
✓ feature_extractor.py     ← NEW: Feature extraction
✓ config.py                ← NEW: Configuration
✓ URLFeatureExtraction.py  ← Original feature functions
✓ safe_web_traffic.py      ← Safe web traffic checker
✓ models/best_model.pickle ← Trained model
✓ README_v2.md             ← Documentation

All files created? → Proceed to Step 3
Missing files? → Check file listing command below
"""

# ======================================================================
# FILE LISTING COMMAND
# ======================================================================

"""
Run this in PowerShell to verify all files:

    Get-ChildItem -Recurse -Include "*.py", "*.pickle", "*.json"

Expected output should show all Python files and model files.
"""

# ======================================================================
# STEP 3: RUN THE APPLICATION
# ======================================================================

"""
Start the Streamlit application:

    streamlit run main_app.py

Expected output:
    
    You can now view your Streamlit app in your browser.
    
    Local URL: http://localhost:8501
    Network URL: http://192.168.x.x:8501

3a. Open the URL in your browser
3b. You should see:
    - Title: "🔍 Phishing Website Detector"
    - Input field for URL
    - Analysis button
    - Sidebar with information
"""

# ======================================================================
# STEP 4: TEST WITH EXAMPLE URLS
# ======================================================================

"""
Try these test URLs in the app:

LEGITIMATE SITES (Should show ✅ LEGITIMATE):
  → https://www.google.com
  → https://www.github.com
  → https://www.amazon.com
  → https://www.wikipedia.org

SUSPICIOUS EXAMPLES:
  → http://192.168.1.1/fake
  → https://user@domain.com
  → https://bit.ly/phishing
  → https://veryverylongdomainname@fake.com

HOW TO TEST:
1. Paste URL into input field
2. Click "🔎 Analyze" button
3. Review results:
   - Prediction (Legitimate/Phishing)
   - Confidence percentage
   - Feature breakdown
"""

# ======================================================================
# STEP 5: PYTHON PROGRAMMATIC TESTING
# ======================================================================

"""
Test the feature extraction directly in Python:

    from feature_extractor import FeatureExtractor
    from config import FeatureConfig
    
    url = "https://www.google.com"
    features = FeatureExtractor.extract(url)
    
    if features:
        print(f"Extracted {len(features)} features")
        for i, feature in enumerate(features):
            print(f"{FeatureConfig.FEATURE_NAMES[i]}: {feature}")

Expected output:
    Extracted 17 features
    IP Address in URL: 0
    @ Symbol Present: 0
    ... (15 more features)
"""

# ======================================================================
# STEP 6: TEST FEATURE EXTRACTION SCRIPT
# ======================================================================

"""
Run the feature extraction test:

    python feature_extractor.py

Expected output:
    ======================================================================
    FEATURE EXTRACTION TEST
    ======================================================================
    
    🔍 Analyzing: https://www.google.com
    
    Extracted 17 features successfully
    ✓ Feature extraction working
    
    ... (more test URLs)
"""

# ======================================================================
# STEP 7: VERIFY MODEL LOADING
# ======================================================================

"""
Test that the model loads correctly:

    import pickle
    
    with open('models/best_model.pickle', 'rb') as f:
        model = pickle.load(f)
    
    print(f"Model loaded: {type(model)}")
    print(f"Model name: {model.__class__.__name__}")

Expected output:
    Model loaded: <class 'sklearn.ensemble._forest.RandomForestClassifier'>
    Model name: RandomForestClassifier
"""

# ======================================================================
# STEP 8: CHECK CONFIGURATION
# ======================================================================

"""
Verify that config.py is loaded correctly:

    from config import AppConfig, FeatureConfig, UIConfig
    
    print(f"Model Path: {AppConfig.MODEL_PATH}")
    print(f"Features Count: {len(FeatureConfig.FEATURE_NAMES)}")
    print(f"Feature Names: {FeatureConfig.FEATURE_NAMES[:3]}")

Expected output:
    Model Path: models/best_model.pickle
    Features Count: 17
    Feature Names: ['IP Address in URL', '@ Symbol Present', 'URL Length']
"""

# ======================================================================
# STEP 9: TROUBLESHOOTING
# ======================================================================

"""
ISSUE: "ModuleNotFoundError: No module named 'streamlit'"
SOLUTION:
    pip install streamlit
    
    Then verify:
    python -c "import streamlit; print(streamlit.__version__)"

ISSUE: "FileNotFoundError: models/best_model.pickle"
SOLUTION:
    Check file exists:
    dir models
    
    If missing, create demo model:
    python setup_demo_model.py

ISSUE: "Port 8501 already in use"
SOLUTION:
    Use different port:
    streamlit run main_app.py --server.port 8502

ISSUE: Network timeout in feature extraction
SOLUTION:
    This is normal for web_traffic check
    App handles this gracefully with default values
    Check safe_web_traffic.py for details

ISSUE: "X has 16 features, but RandomForestClassifier is expecting 17"
SOLUTION:
    This should NOT happen with new code
    Verify FeatureExtractor.extract() returns exactly 17 features
    Run test:
    from feature_extractor import FeatureExtractor
    features = FeatureExtractor.extract("https://google.com")
    print(len(features))  # Should print 17
"""

# ======================================================================
# STEP 10: PERFORMANCE MONITORING
# ======================================================================

"""
Monitor the application performance:

1. Check log output in terminal
   - Should show "Model loaded successfully"
   - Feature extraction timing
   - Prediction results

2. Watch browser console for errors
   - Press F12 in browser
   - Look at Console tab
   - Should see no errors

3. Monitor terminal for warnings
   - Streamlit deprecation warnings (non-blocking)
   - Feature extraction warnings (if any)

4. Performance metrics
   - Feature extraction: <1 second
   - Model prediction: <100ms
   - Total response: <2 seconds
"""

# ======================================================================
# STEP 11: ADVANCED USAGE
# ======================================================================

"""
Using the library programmatically:

A. BATCH ANALYSIS:
    
    from feature_extractor import FeatureExtractor
    from config import FeatureConfig
    import pickle
    
    urls = [
        "https://google.com",
        "https://bit.ly/test",
        "https://192.168.1.1"
    ]
    
    with open('models/best_model.pickle', 'rb') as f:
        model = pickle.load(f)
    
    for url in urls:
        features = FeatureExtractor.extract(url)
        if features:
            pred = model.predict([features])[0]
            conf = model.predict_proba([features])[0]
            print(f"{url}: {'PHISHING' if pred == 1 else 'LEGITIMATE'} ({conf[pred]:.2%})")

B. ANALYZE FEATURES:
    
    from feature_extractor import FeatureAnalyzer
    
    analysis = FeatureAnalyzer.analyze(features)
    
    print(f"High Risk Features: {analysis['high_risk']}")
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"Risk Score: {analysis['risk_percentage']:.1f}%")

C. CUSTOM CONFIGURATION:
    
    In config.py, modify:
    - AppConfig.MODEL_PATH
    - UIConfig colors
    - FeatureConfig descriptions
"""

# ======================================================================
# STEP 12: PRODUCTION DEPLOYMENT
# ======================================================================

"""
To deploy to production:

1. Ensure all tests pass
   - Run through Steps 1-8
   - Check all URLs work
   - Verify model predictions

2. Update main_app.py:
   - Uncomment production logging
   - Add authentication (if needed)
   - Adjust UI as needed

3. Push to cloud:
   streamlit run main_app.py (works on Streamlit Cloud)

4. Monitor production:
   - Check error logs
   - Monitor response times
   - Track usage patterns
"""

# ======================================================================
# QUICK START SUMMARY
# ======================================================================

"""
TL;DR - Get running in 5 minutes:

1. cd "c:\Users\bramh\Downloads\Phishing-Website-Detection-by-Ml-Techniq\Phishing-Website"
2. python -m venv venv && venv\Scripts\activate
3. pip install -r requirements.txt
4. streamlit run main_app.py
5. Open http://localhost:8501 in browser
6. Enter any URL and click "🔎 Analyze"

Done! Your phishing detector is running! 🚀
"""

# ======================================================================
# ADDITIONAL RESOURCES
# ======================================================================

"""
Documentation:
  - README_v2.md       ← Full documentation
  - config.py          ← Configuration options
  - main_app.py        ← Application code with comments
  - feature_extractor.py ← Feature extraction with docstrings

Testing:
  - Run: python feature_extractor.py (for feature testing)
  - Run: streamlit run main_app.py (for web testing)

Configuration:
  - Edit: config.py (for settings)
  - Edit: main_app.py (for UI changes)

Troubleshooting:
  - Check terminal logs
  - Review error messages
  - Check config.py settings
"""

# ======================================================================
# END OF GUIDE
# ======================================================================

if __name__ == "__main__":
    print(__doc__)
    print("\n✅ Setup guide complete!")
    print("📖 See README_v2.md for more information")
    print("🚀 Ready to run: streamlit run main_app.py")
