#!/usr/bin/env python3
"""
🚀 QUICK START SCRIPT - PHISHING DETECTOR v2.0
======================================================================

This script automates the setup and launch of the application.

Usage:
    python quick_start.py
"""

import sys
import subprocess
from pathlib import Path


def print_step(step_num: int, text: str) -> None:
    """Print a formatted step."""
    print(f"\n📍 STEP {step_num}: {text}")
    print("─" * 60)


def print_success(text: str) -> None:
    """Print success message."""
    print(f"✅ {text}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"❌ {text}")


def check_python() -> bool:
    """Check Python version."""
    print_step(1, "CHECKING PYTHON VERSION")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python version: {version_str}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, you have {version_str}")
        return False
    
    print_success(f"Python {version_str} OK")
    return True


def check_dependencies() -> bool:
    """Check if dependencies are installed."""
    print_step(2, "CHECKING DEPENDENCIES")
    
    required = {
        'streamlit': 'Streamlit (web interface)',
        'sklearn': 'scikit-learn (ML)',
        'pandas': 'pandas (data processing)',
        'numpy': 'NumPy (math)',
        'requests': 'requests (HTTP)',
    }
    
    missing = []
    
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            missing.append(module)
    
    if missing:
        print_error(f"Missing dependencies: {', '.join(missing)}")
        print("\nInstalling dependencies...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print_success("Dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install dependencies")
            print("Run manually: pip install -r requirements.txt")
            return False
    
    print_success("All dependencies installed")
    return True


def check_files() -> bool:
    """Check if all required files exist."""
    print_step(3, "CHECKING FILES")
    
    required_files = [
        'main_app.py',
        'config.py',
        'feature_extractor.py',
        'URLFeatureExtraction.py',
        'safe_web_traffic.py',
        'models/best_model.pickle',
        'requirements.txt',
    ]
    
    missing = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            missing.append(file_path)
    
    if missing:
        print_error(f"Missing files: {', '.join(missing)}")
        return False
    
    print_success("All files present")
    return True


def run_tests() -> bool:
    """Run automated tests."""
    print_step(4, "RUNNING TESTS")
    
    if not Path('test_app.py').exists():
        print("⚠️  Test file not found, skipping tests")
        return True
    
    try:
        subprocess.check_call([sys.executable, 'test_app.py'])
        return True
    except subprocess.CalledProcessError:
        print_error("Tests failed")
        return False


def launch_app() -> None:
    """Launch the Streamlit application."""
    print_step(5, "LAUNCHING APPLICATION")
    
    print("Starting Streamlit server...")
    print("\n" + "=" * 60)
    print("Your application will open in a web browser")
    print("Local URL: http://localhost:8501")
    print("=" * 60 + "\n")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'main_app.py'
        ])
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user")
    except Exception as e:
        print_error(f"Failed to start app: {e}")


def main() -> None:
    """Main entry point."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "  🔍 PHISHING DETECTOR - QUICK START".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    steps = [
        ("Python version check", check_python),
        ("Dependencies check", check_dependencies),
        ("Files check", check_files),
        ("Run tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                print("\n" + "!" * 60)
                print(f"Setup failed at: {step_name}")
                print("!" * 60)
                return
        except Exception as e:
            print_error(f"Error in {step_name}: {e}")
            return
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "  ✨ ALL CHECKS PASSED! ✨".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Launch app
    try:
        response = input("\n🚀 Launch application now? (y/n): ").lower()
        if response == 'y':
            launch_app()
        else:
            print("\n📖 To launch manually, run:")
            print("   streamlit run main_app.py")
    except KeyboardInterrupt:
        print("\n\nSetup cancelled")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
