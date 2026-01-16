"""
Train All Health Prediction Models
Run this script to train all models and save them to the saved_models directory
"""
from models.diabetes_model import DiabetesModel
from models.heart_model import HeartModel
from models.hypertension_model import HypertensionModel
from models.obesity_model import ObesityModel
import os

def train_all_models():
    """Train all health prediction models"""
    print("=" * 60)
    print("Training All Health Prediction Models")
    print("=" * 60)
    
    # Create saved_models directory if it doesn't exist
    os.makedirs('saved_models', exist_ok=True)
    
    # Train Diabetes Model
    print("\n1. Training Diabetes Model...")
    diabetes_model = DiabetesModel()
    diabetes_accuracy = diabetes_model.train('dataset/diabetes.csv')
    print(f"✅ Diabetes Model trained with accuracy: {diabetes_accuracy:.4f}")
    
    # Train Heart Disease Model
    print("\n2. Training Heart Disease Model...")
    heart_model = HeartModel()
    heart_accuracy = heart_model.train('dataset/heart.csv')
    print(f"✅ Heart Disease Model trained with accuracy: {heart_accuracy:.4f}")
    
    # Train Hypertension Model
    print("\n3. Training Hypertension Model...")
    hypertension_model = HypertensionModel()
    hypertension_accuracy = hypertension_model.train('dataset/hypertension_dataset.csv')
    print(f"✅ Hypertension Model trained with accuracy: {hypertension_accuracy:.4f}")
    
    # Train Obesity Model
    print("\n4. Training Obesity Model...")
    obesity_model = ObesityModel()
    obesity_accuracy = obesity_model.train('dataset/obesity.csv')
    print(f"✅ Obesity Model trained with accuracy: {obesity_accuracy:.4f}")
    
    print("\n" + "=" * 60)
    print("✅ All models trained successfully!")
    print("=" * 60)
    print("\nModel Summary:")
    print(f"  - Diabetes Model: {diabetes_accuracy:.2%} accuracy")
    print(f"  - Heart Disease Model: {heart_accuracy:.2%} accuracy")
    print(f"  - Hypertension Model: {hypertension_accuracy:.2%} accuracy")
    print(f"  - Obesity Model: {obesity_accuracy:.2%} accuracy")
    print("\nModels saved to: saved_models/")

if __name__ == "__main__":
    train_all_models()
