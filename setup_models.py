"""
One-time script to train and save ML models on Render
Run this manually after first deployment
"""
import os
import sys

def setup_models():
    """Train all ML models and save them"""
    print("=" * 70)
    print("🏋️ TRAINING ML MODELS - ONE TIME SETUP")
    print("=" * 70)
    print("\n⏱️  This will take 2-3 minutes...")
    print("⚠️  Only needs to be done ONCE!")
    print("📁 Models will be saved to saved_models/\n")
    
    try:
        from train_all_models import main
        print("🚀 Starting model training...\n")
        main()
        print("\n" + "=" * 70)
        print("✅ MODEL TRAINING COMPLETE!")
        print("=" * 70)
        print("\n📊 Your health assessment system is now ready!")
        print("🔄 Restart your Render service for changes to take effect.")
        print("\nℹ️  Models are saved to persistent disk and will survive restarts.\n")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Check if models already exist
    if os.path.exists('saved_models') and len(os.listdir('saved_models')) >= 4:
        print("\n✅ Models already exist!")
        response = input("Do you want to retrain? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Skipping training.")
            sys.exit(0)
    
    setup_models()
