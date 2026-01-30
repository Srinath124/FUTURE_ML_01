"""
Verification script to check if the repository is properly set up.
Run this after cloning the repository to ensure all dependencies and files are in place.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.8+)")
        return False

def check_dependencies():
    """Check if all required packages are installed."""
    print("\nChecking dependencies...")
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn',
        'sklearn', 'statsmodels', 'jupyter'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_directory_structure():
    """Check if all required directories and files exist."""
    print("\nChecking directory structure...")
    
    base_dir = Path.cwd()
    required_structure = {
        'src/__init__.py': 'Source code initialization',
        'src/data_preprocessing.py': 'Data preprocessing module',
        'src/feature_engineering.py': 'Feature engineering module',
        'src/models.py': 'Models module',
        'src/visualization.py': 'Visualization module',
        'data/processed/daily_sales_simple.csv': 'Simple time series data',
        'data/processed/daily_sales_features.csv': 'Feature-engineered data',
        'notebooks/01_data_exploration.ipynb': 'Notebook 1',
        'notebooks/02_data_preparation.ipynb': 'Notebook 2',
        'notebooks/03_forecasting_models.ipynb': 'Notebook 3',
        'notebooks/04_business_insights.ipynb': 'Notebook 4',
        'notebooks/05_visualization.ipynb': 'Notebook 5',
        'requirements.txt': 'Dependencies file',
        'README.md': 'Documentation'
    }
    
    missing = []
    for file_path, description in required_structure.items():
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} ({description})")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} required files/directories")
        return False
    return True

def check_imports():
    """Check if custom modules can be imported."""
    print("\nChecking custom module imports...")
    
    # Add src to path
    sys.path.insert(0, str(Path.cwd() / 'src'))
    
    modules_to_test = [
        ('data_preprocessing', ['load_data', 'clean_data']),
        ('feature_engineering', ['create_time_features']),
        ('models', ['BaselineForecaster', 'ARIMAForecaster', 'MLForecaster']),
        ('visualization', ['plot_forecast'])
    ]
    
    all_ok = True
    for module_name, expected_items in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"✅ {module_name}")
            
            # Check for expected functions/classes
            for item in expected_items:
                if not hasattr(module, item):
                    print(f"   ⚠️  Missing: {item}")
                    all_ok = False
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            all_ok = False
    
    return all_ok

def check_data_files():
    """Check if data files are accessible and valid."""
    print("\nChecking data files...")
    
    try:
        import pandas as pd
        
        # Check simple data
        simple_path = Path.cwd() / 'data' / 'processed' / 'daily_sales_simple.csv'
        df_simple = pd.read_csv(simple_path)
        print(f"✅ daily_sales_simple.csv ({len(df_simple)} rows, {len(df_simple.columns)} columns)")
        
        # Check features data
        features_path = Path.cwd() / 'data' / 'processed' / 'daily_sales_features.csv'
        df_features = pd.read_csv(features_path)
        print(f"✅ daily_sales_features.csv ({len(df_features)} rows, {len(df_features.columns)} columns)")
        
        return True
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False

def main():
    """Run all verification checks."""
    print("="*60)
    print("SALES FORECASTING REPOSITORY VERIFICATION")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Custom Imports", check_imports),
        ("Data Files", check_data_files)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    all_passed = all(result for _, result in results)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("="*60)
    if all_passed:
        print("✅ All checks passed! Repository is ready to use.")
        print("\nNext steps:")
        print("1. Start Jupyter: jupyter notebook")
        print("2. Run notebooks in order: 01 → 02 → 03 → 04 → 05")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Ensure you're in the project root directory")
        print("- Check if all files were properly cloned from Git")
        return 1

if __name__ == "__main__":
    exit(main())
