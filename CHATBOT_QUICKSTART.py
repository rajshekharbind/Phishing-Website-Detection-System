#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Start - Chatbot Setup & Testing
Helps users configure and test the phishing detection chatbot

Usage:
    python CHATBOT_QUICKSTART.py
"""

import os
import sys
from pathlib import Path

def print_header():
    """Print welcome header."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🤖 PHISHING DETECTION CHATBOT - QUICK START GUIDE       ║
║                                                              ║
║    Advanced AI-powered cybersecurity assistant             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking Dependencies...")
    print("-" * 60)
    
    required_packages = {
        'streamlit': 'Streamlit',
        'requests': 'Requests',
        'transformers': 'Transformers',
        'huggingface_hub': 'Hugging Face Hub'
    }
    
    missing = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {name:<25} ✓ Installed")
        except ImportError:
            print(f"  ✗ {name:<25} ✗ Missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n📥 Install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def check_api_key():
    """Check for Hugging Face API key configuration."""
    print("\n🔑 Checking API Key Configuration...")
    print("-" * 60)
    
    # Check environment variable
    env_key = os.environ.get('HF_API_KEY')
    if env_key:
        print("  ✓ Found HF_API_KEY in environment variables")
        return True
    
    # Check secrets.toml
    secrets_path = Path('.streamlit/secrets.toml')
    if secrets_path.exists():
        with open(secrets_path, 'r') as f:
            content = f.read()
            if 'HF_API_KEY' in content and 'hf_' in content:
                print("  ✓ Found HF_API_KEY in .streamlit/secrets.toml")
                return True
    
    print("  ✗ No API key configuration found")
    print("\n📋 How to get a Hugging Face API key:")
    print("   1. Go to https://huggingface.co/settings/tokens")
    print("   2. Click 'New token'")
    print("   3. Create a READ token")
    print("   4. Copy the token")
    
    print("\n🔧 How to configure the API key:")
    print("\n   Option A - Environment Variable (Recommended):")
    print("   Windows PowerShell: $env:HF_API_KEY = 'hf_...'")
    print("   Windows CMD:        set HF_API_KEY=hf_...")
    print("   Linux/Mac:          export HF_API_KEY='hf_...'")
    
    print("\n   Option B - Local Configuration:")
    print("   Edit .streamlit/secrets.toml")
    print("   Add: HF_API_KEY = 'hf_...'")
    
    print("\n   Option C - Streamlit Cloud:")
    print("   Go to your app settings → Secrets tab")
    print("   Add HF_API_KEY with your token")
    
    return False

def show_setup_options():
    """Show setup configuration options."""
    print("\n⚙️  Setup Options")
    print("-" * 60)
    print("""
    1. Environment Variable (Recommended)
       - Set globally in your system
       - Works across all Python projects
       - More secure
    
    2. .streamlit/secrets.toml (Local Development)
       - Project-specific configuration
       - Easy for testing
       - Not recommended for sensitive data
    
    3. Streamlit Cloud Secrets (Production)
       - Secure cloud deployment
       - No local secrets file
       - Recommended for production
    """)

def test_chatbot_import():
    """Test if chatbot module can be imported."""
    print("\n🧪 Testing Chatbot Module...")
    print("-" * 60)
    
    try:
        from chatbot import PhishingChatbot
        print("  ✓ Chatbot module imported successfully")
        
        # Try to initialize chatbot
        bot = PhishingChatbot()
        print("  ✓ Chatbot initialized successfully")
        
        # Test fallback response
        response = bot._get_fallback_response("what is phishing")
        if response:
            print("  ✓ Fallback responses working")
        else:
            print("  ✗ Fallback responses not working")
            return False
        
        print("\n✅ Chatbot module test passed!")
        return True
        
    except ImportError as e:
        print(f"  ✗ Failed to import chatbot module: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error initializing chatbot: {e}")
        return False

def show_next_steps():
    """Show next steps to run the application."""
    print("\n📋 Next Steps")
    print("-" * 60)
    print("""
    1. Configure API Key (see options above)
    
    2. Run the Streamlit Application:
       streamlit run main_app.py
    
    3. Open in Browser:
       http://localhost:8501
    
    4. Select '💬 Chat Assistant' Tab
    
    5. Start Asking Questions!
    
    Example Questions:
    ✓ What is phishing?
    ✓ How do I detect a phishing URL?
    ✓ What features do you analyze?
    ✓ How do I stay safe online?
    ✓ What's the difference between HTTP and HTTPS?
    """)

def show_troubleshooting():
    """Show troubleshooting guide."""
    print("\n⚠️  Troubleshooting")
    print("-" * 60)
    print("""
    Problem: "API key not configured"
    Solution: Set HF_API_KEY environment variable or add to secrets.toml
    
    Problem: "Rate limiting error"
    Solution: Free API has limits. Wait or upgrade to paid plan
    
    Problem: "Slow responses"
    Solution: Normal for free tier. API processing takes 2-5 seconds
    
    Problem: "Module not found"
    Solution: pip install -r requirements.txt
    
    Problem: "Chat not loading"
    Solution: Check browser console, refresh page, clear cache
    
    For more help, see CHATBOT_SETUP.md
    """)

def main():
    """Main setup flow."""
    print_header()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check API key
    api_ok = check_api_key()
    
    if not api_ok:
        print("\n⚠️  No API key found. The chatbot will use offline fallback responses.")
        print("   To enable full AI responses, configure an API key.")
    
    # Show options
    show_setup_options()
    
    # Test import
    test_ok = test_chatbot_import()
    
    if not test_ok:
        print("\n❌ Chatbot module test failed. Check the errors above.")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()
    
    # Troubleshooting
    show_troubleshooting()
    
    print("\n" + "=" * 60)
    print("✅ Setup verification complete!")
    print("=" * 60)
    print("\n🚀 Ready to run: streamlit run main_app.py\n")

if __name__ == "__main__":
    main()
