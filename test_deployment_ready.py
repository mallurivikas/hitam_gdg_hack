"""
Pre-Deployment Test Script
Run this before deploying to Render to catch issues early
"""
import os
import sys
import importlib.util

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: NOT FOUND")
        return False

def check_requirements():
    """Verify requirements.txt is valid"""
    print_header("CHECKING REQUIREMENTS.TXT")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements = f.read()
    
    # Check for problematic packages
    issues = []
    if 'pywin32' in requirements:
        issues.append("pywin32 (Windows-only, will break on Linux)")
    
    if issues:
        print(f"❌ Found problematic packages:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ requirements.txt looks good!")
        return True

def check_deployment_files():
    """Check all deployment files exist"""
    print_header("CHECKING DEPLOYMENT FILES")
    
    files = [
        ('runtime.txt', 'Python version file'),
        ('Procfile', 'Gunicorn start command'),
        ('gunicorn_config.py', 'Gunicorn configuration'),
        ('render.yaml', 'Render service definition'),
        ('app.py', 'Flask application'),
    ]
    
    all_exist = True
    for filepath, description in files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_environment():
    """Check environment configuration"""
    print_header("CHECKING ENVIRONMENT")
    
    # Check if .env exists (should not be committed)
    if os.path.exists('.env'):
        print("⚠️  .env file exists - make sure it's in .gitignore!")
        with open('.gitignore', 'r', encoding='utf-8') as f:
            if '.env' in f.read():
                print("✅ .env is in .gitignore")
            else:
                print("❌ .env is NOT in .gitignore - add it!")
                return False
    else:
        print("✅ No .env file found (good for deployment)")
    
    # Check if .env.example exists
    if os.path.exists('.env.example'):
        print("✅ .env.example found (good for documentation)")
    
    return True

def check_app_configuration():
    """Check app.py configuration"""
    print_header("CHECKING APP.PY CONFIGURATION")
    
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        return False
    
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    checks = []
    
    # Check for PORT environment variable
    if "os.environ.get('PORT'" in app_content or 'os.getenv("PORT"' in app_content:
        print("✅ Port is read from environment variable")
        checks.append(True)
    else:
        print("❌ Port should be read from environment (PORT)")
        checks.append(False)
    
    # Check for debug mode configuration
    if "FLASK_ENV" in app_content or "debug=False" in app_content:
        print("✅ Debug mode is properly configured")
        checks.append(True)
    else:
        print("⚠️  Debug mode configuration unclear")
        checks.append(False)
    
    # Check for hard-coded port
    if "port=5000" in app_content and "os.environ" not in app_content.split("port=5000")[0].split('\n')[-1]:
        print("⚠️  Found hard-coded port=5000 (may be okay as fallback)")
    
    return all(checks)

def check_imports():
    """Check if key modules can be imported"""
    print_header("CHECKING KEY IMPORTS")
    
    modules_to_check = [
        'flask',
        'gunicorn',
        'sklearn',
        'pandas',
        'numpy',
    ]
    
    all_imported = True
    for module_name in modules_to_check:
        try:
            if module_name == 'sklearn':
                module_name = 'sklearn'  # scikit-learn imports as sklearn
            __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"❌ {module_name} - NOT INSTALLED")
            all_imported = False
    
    return all_imported

def check_models():
    """Check if model files exist"""
    print_header("CHECKING ML MODELS")
    
    model_dir = 'saved_models'
    if not os.path.exists(model_dir):
        print(f"⚠️  {model_dir}/ directory not found")
        print("   Models will need to be trained on first run")
        return True
    
    expected_models = [
        'diabetes_model.pkl',
        'heart_model.pkl',
        'hypertension_model.pkl',
        'obesity_model.pkl',
    ]
    
    found_any = False
    for model_file in expected_models:
        model_path = os.path.join(model_dir, model_file)
        if os.path.exists(model_path):
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"✅ {model_file} ({size_mb:.2f} MB)")
            found_any = True
        else:
            print(f"⚠️  {model_file} not found")
    
    if not found_any:
        print("\n⚠️  No model files found. They will be trained on deployment.")
        print("   Consider training locally and committing models if < 100MB")
    
    return True

def run_all_tests():
    """Run all pre-deployment tests"""
    print("\n" + "🚀" * 35)
    print("   PRE-DEPLOYMENT TEST SUITE")
    print("   Testing before Render deployment")
    print("🚀" * 35)
    
    tests = [
        ("Deployment Files", check_deployment_files),
        ("Requirements", check_requirements),
        ("Environment", check_environment),
        ("App Configuration", check_app_configuration),
        ("Python Imports", check_imports),
        ("ML Models", check_models),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error running {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print_header("TEST SUMMARY")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Ready for deployment!")
        print("\nNext steps:")
        print("1. Run: python generate_secret_key.py")
        print("2. Commit: git add . && git commit -m 'Ready for deployment'")
        print("3. Push: git push origin main")
        print("4. Deploy on Render!")
    else:
        print("⚠️  Some tests failed. Please fix issues before deploying.")
        print("Check the output above for specific problems.")
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
