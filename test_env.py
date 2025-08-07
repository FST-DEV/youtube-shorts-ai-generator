#!/usr/bin/env python3
"""
Simple script to test if .env file is being loaded correctly
"""
import os

print("🧪 Testing Environment Variables...")
print("=" * 50)

# Try to load .env file
try:
    from dotenv import load_dotenv
    result = load_dotenv()
    print(f"✅ dotenv.load_dotenv() returned: {result}")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists in current directory")
        with open('.env', 'r') as f:
            lines = f.readlines()
            print(f"✅ .env file has {len(lines)} lines")
    else:
        print("❌ .env file NOT found in current directory")
        print(f"📁 Current directory: {os.getcwd()}")
        
except ImportError:
    print("❌ python-dotenv not installed!")
    print("Run: pip install python-dotenv")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

print("\n📋 Environment Variables Check:")
print("-" * 30)

# Check each variable
variables = [
    'HUGGING_FACE_TOKEN',
    'SENDER_EMAIL', 
    'SENDER_APP_PASSWORD',
    'RECIPIENT_EMAILS',
    'RECIPIENT_EMAIL'
]

for var in variables:
    value = os.getenv(var)
    if value:
        # Hide sensitive data
        if 'TOKEN' in var or 'PASSWORD' in var:
            display_value = f"{value[:8]}..." if len(value) > 8 else "***"
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")
    else:
        print(f"❌ {var}: Not set")

print(f"\n📁 Current working directory: {os.getcwd()}")
print("📄 Files in current directory:")
for file in os.listdir('.'):
    if file.startswith('.env') or file.endswith('.py'):
        print(f"   - {file}")

print("\n" + "=" * 50)
print("If variables show as 'Not set', check your .env file format!")