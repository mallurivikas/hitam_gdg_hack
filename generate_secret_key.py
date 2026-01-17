"""
Generate a secure Flask secret key for deployment
Run this script and copy the output to your Render environment variables
"""
import secrets

def generate_secret_key():
    """Generate a cryptographically secure secret key"""
    key = secrets.token_hex(32)
    return key

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔐 FLASK SECRET KEY GENERATOR")
    print("="*70)
    print("\n📋 Copy the key below to your Render environment variables:\n")
    print(f"FLASK_SECRET_KEY={generate_secret_key()}")
    print("\n" + "="*70)
    print("⚠️  Keep this key secret! Never commit it to version control.")
    print("✅ This key is suitable for production use.")
    print("="*70 + "\n")
