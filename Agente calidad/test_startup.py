"""
Quick test script to verify the application structure
Run this after installing dependencies to ensure everything works
"""
import sys

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        from dotenv import load_dotenv
        import sqlite3
        import smtplib
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_main_module():
    """Test that main.py can be imported"""
    print("\nTesting main.py module...")
    try:
        import main
        print("✓ main.py imported successfully")
        print(f"✓ FastAPI app created: {main.app.title}")
        return True
    except Exception as e:
        print(f"✗ Error importing main.py: {e}")
        return False

def test_endpoints():
    """Test that all required endpoints exist"""
    print("\nTesting endpoints...")
    try:
        import main
        routes = [route.path for route in main.app.routes]
        
        required_endpoints = [
            "/health",
            "/tool/proveedor/{nombre}",
            "/tool/ranking",
            "/tool/alertas-pendientes",
            "/tool/registrar-lote",
            "/tool/enviar-alerta/{nombre}",
            "/seed"
        ]
        
        all_found = True
        for endpoint in required_endpoints:
            if endpoint in routes:
                print(f"✓ {endpoint}")
            else:
                print(f"✗ {endpoint} NOT FOUND")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"✗ Error checking endpoints: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Quality Control API - Startup Test")
    print("=" * 60)
    
    results = []
    results.append(test_imports())
    results.append(test_main_module())
    results.append(test_endpoints())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYou can now run the application with:")
        print("  uvicorn main:app --reload")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease install dependencies first:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

# Made with Bob
