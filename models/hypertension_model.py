"""
Hypertension Prediction Model
Features: Age, BMI, Cholesterol, Systolic_BP, Diastolic_BP, Smoking_Status, Alcohol_Intake, 
          Physical_Activity_Level, Family_History, Diabetes, Stress_Level, Salt_Intake, 
          Sleep_Duration, Heart_Rate, LDL, HDL, Triglycerides, Glucose, Gender, etc.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os


class HypertensionModel:
    def __init__(self, model_path='saved_models/hypertension_model.pkl'):
        self.model = None
        self.model_path = model_path
        self.encoded_columns = None  # Store column names after encoding
        self.feature_names = None
        
    def train(self, data_path):
        """Train the hypertension prediction model"""
        # Load dataset
        df = pd.read_csv(data_path)
        
        # Define features and target
        X = df.drop('Hypertension', axis=1)
        y = df['Hypertension']
        
        # Encode categorical features
        X = pd.get_dummies(X, drop_first=True)
        y = y.astype('category').cat.codes
        
        # Store encoded column names
        self.encoded_columns = X.columns.tolist()
        
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
        
        print(f"Hypertension Model Training Accuracy: {accuracy:.4f}")
        
        # Save model
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        model_data = {
            'model': self.model,
            'encoded_columns': self.encoded_columns
        }
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Hypertension model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.encoded_columns = model_data['encoded_columns']
            print("Hypertension model loaded successfully")
            return True
        else:
            print(f"No saved model found at {self.model_path}")
            return False
    
    def predict(self, features):
        """
        Predict hypertension risk
        
        Args:
            features (dict): Dictionary with keys like:
                - Age, BMI, Cholesterol, Systolic_BP, Diastolic_BP, 
                  Smoking_Status, Alcohol_Intake, Physical_Activity_Level,
                  Family_History, Diabetes, Stress_Level, Salt_Intake,
                  Sleep_Duration, Heart_Rate, LDL, HDL, Triglycerides,
                  Glucose, Gender, etc.
        
        Returns:
            tuple: (prediction, probability)
                - prediction: 0 (no risk) or 1 (at risk)
                - probability: risk probability (0-1)
        """
        if self.model is None:
            if not self.load_model():
                raise Exception("Model not trained or loaded")
        
        # Create DataFrame from features
        feature_df = pd.DataFrame([features])
        
        # Encode categorical features
        feature_df = pd.get_dummies(feature_df, drop_first=True)
        
        # Align columns with training data
        for col in self.encoded_columns:
            if col not in feature_df.columns:
                feature_df[col] = 0
        
        # Keep only columns that were in training
        feature_df = feature_df[self.encoded_columns]
        
        # Predict
        prediction = self.model.predict(feature_df)[0]
        probability = self.model.predict_proba(feature_df)[0][1]
        
        return prediction, probability
    
    def get_risk_score(self, features):
        """Get risk score as percentage (0-100)"""
        _, probability = self.predict(features)
        return probability * 100


if __name__ == "__main__":
    # Train the model
    model = HypertensionModel()
    dataset_path = "../dataset/hypertension_dataset.csv"
    model.train(dataset_path)
