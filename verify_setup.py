"""
Setup Verification Script
Run this to verify your automation testing environment is set up correctly
Usage: python verify_setup.py
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🔍 Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False


def check_virtual_env():
    """Check if virtual environment is activated"""
    print("🔍 Checking virtual environment...", end=" ")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("✅ Virtual environment activated")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("   Run: .\\env\\Scripts\\Activate.ps1")
        return False


def check_required_packages():
    """Check if required packages are installed"""
    print("🔍 Checking required packages...", end=" ")
    required = ['pytest', 'playwright', 'faker']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        print("✅ All packages installed")
        return True
    else:
        print(f"❌ Missing: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        return False


def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    print("🔍 Checking Playwright browsers...", end=" ")
    try:
        result = subprocess.run(
            ['playwright', 'install', '--dry-run'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Playwright browsers installed")
            return True
        else:
            print("❌ Playwright browsers not found")
            print("   Run: playwright install chromium")
            return False
    except Exception as e:
        print(f"⚠️  Could not verify: {str(e)}")
        return False


def check_project_structure():
    """Check if all required directories exist"""
    print("🔍 Checking project structure...", end=" ")
    required_dirs = ['tests', 'pages', 'utils', 'reports']
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if not missing_dirs:
        print("✅ All directories exist")
        return True
    else:
        print(f"❌ Missing: {', '.join(missing_dirs)}")
        return False


def check_required_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...", end=" ")
    required_files = [
        'conftest.py',
        'pytest.ini',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    missing_files = []
    
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if not missing_files:
        print("✅ All files exist")
        return True
    else:
        print(f"❌ Missing: {', '.join(missing_files)}")
        return False


def check_env_file():
    """Check if .env file exists"""
    print("🔍 Checking .env file...", end=" ")
    if Path('.env').exists():
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Run: copy .env.example .env")
        return False


def check_pytest_plugins():
    """Check if pytest can find custom plugins"""
    print("🔍 Checking pytest plugins...", end=" ")
    try:
        result = subprocess.run(
            ['pytest', '--collect-only', '-q'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Pytest working correctly")
            return True
        else:
            print("⚠️  Pytest issue detected")
            return False
    except Exception as e:
        print(f"⚠️  Could not verify: {str(e)}")
        return False


def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("🧪 Automation Testing Setup Verification")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Required Packages", check_required_packages),
        ("Playwright Browsers", check_playwright_browsers),
        ("Project Structure", check_project_structure),
        ("Required Files", check_required_files),
        (".env File", check_env_file),
        ("Pytest Plugins", check_pytest_plugins),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"❌ Error checking {name}: {str(e)}")
            results.append(False)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\n🚀 You're ready to run tests!")
        print("\nQuick start:")
        print("  pytest -v              # Run all tests")
        print("  pytest -k login        # Run tests with 'login' in name")
        print("\n📊 View HTML report: reports/report.html")
    else:
        print(f"⚠️  Some checks failed. ({passed}/{total})")
        print("\n📋 Please fix the issues above and run this script again.")
    
    print("="*50 + "\n")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
