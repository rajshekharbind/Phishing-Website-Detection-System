#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Installation Script
Verifies that all required packages are installed and working
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'xgboost': 'XGBoost',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'urllib3': 'URLlib3'
    }
    
    print("=" * 60)
    print("Testing Installation - Phishing Website Detection")
    print("=" * 60)
    print("\nTesting package imports...\n")
    
    failed = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:25} - OK")
        except ImportError:
            print(f"✗ {name:25} - FAILED")
            failed.append(name)
    
    print("\n" + "=" * 60)
    
    if failed:
        print(f"\n⚠ Installation incomplete. Missing packages:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All packages installed successfully!")
        print("\nYou're ready to start:")
        print("1. Run: jupyter notebook")
        print("2. Open 'URL Feature Extraction.ipynb'")
        print("3. Then run 'Phishing Website Detection_Models & Training.ipynb'")
        return True

def main():
    """Main execution"""
    success = test_imports()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
