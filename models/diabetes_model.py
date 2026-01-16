"""
Diabetes Prediction Model
Features: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os


class DiabetesModel:
    def __init__(self, model_path='saved_models/diabetes_model.pkl'):
        self.model = None
        self.model_path = model_path
        self.feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                              'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
    def train(self, data_path):
        """Train the diabetes prediction model"""
        # Load dataset
        df = pd.read_csv(data_path)
        
        # Define features and target
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Diabetes Model Training Accuracy: {accuracy:.4f}")
        
        # Save model
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Diabetes model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("Diabetes model loaded successfully")
            return True
        else:
            print(f"No saved model found at {self.model_path}")
            return False
    
    def predict(self, features):
        """
        Predict diabetes risk
        
        Args:
            features (dict): Dictionary with keys:
                - Pregnancies, Glucose, BloodPressure, SkinThickness, 
                  Insulin, BMI, DiabetesPedigreeFunction, Age
        
        Returns:
            tuple: (prediction, probability)
                - prediction: 0 (no risk) or 1 (at risk)
                - probability: risk probability (0-1)
        """
        if self.model is None:
            if not self.load_model():
                raise Exception("Model not trained or loaded")
        
        # Create feature array in correct order
        feature_array = np.array([[
            features.get('Pregnancies', 0),
            features.get('Glucose', 0),
            features.get('BloodPressure', 0),
            features.get('SkinThickness', 0),
            features.get('Insulin', 0),
            features.get('BMI', 0),
            features.get('DiabetesPedigreeFunction', 0.5),
            features.get('Age', 0)
        ]])
        
        # Predict
        prediction = self.model.predict(feature_array)[0]
        probability = self.model.predict_proba(feature_array)[0][1]
        
        return prediction, probability
    
    def get_risk_score(self, features):
        """Get risk score as percentage (0-100)"""
        _, probability = self.predict(features)
        return probability * 100


if __name__ == "__main__":
    # Train the model
    model = DiabetesModel()
    dataset_path = "../dataset/diabetes.csv"
    model.train(dataset_path)
