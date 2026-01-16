"""
Obesity Classification Model
Features: Gender, Age, Height, Weight, family_history_with_overweight, FAVC, FCVC, NCP, 
          CAEC, SMOKE, CH2O, SCC, FAF, TUE, CALC, MTRANS
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os


class ObesityModel:
    def __init__(self, model_path='saved_models/obesity_model.pkl'):
        self.model = None
        self.model_path = model_path
        self.encoded_columns = None  # Store column names after encoding
        self.feature_names = None
        
    def train(self, data_path):
        """Train the obesity classification model"""
        # Load dataset
        df = pd.read_csv(data_path)
        
        # Define features and target
        X = df.drop('NObeyesdad', axis=1)
        y = df['NObeyesdad']
        
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
        
        print(f"Obesity Model Training Accuracy: {accuracy:.4f}")
        
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
        print(f"Obesity model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.encoded_columns = model_data['encoded_columns']
            print("Obesity model loaded successfully")
            return True
        else:
            print(f"No saved model found at {self.model_path}")
            return False
    
    def predict(self, features):
        """
        Predict obesity classification
        
        Args:
            features (dict): Dictionary with keys:
                - Gender, Age, Height, Weight, family_history_with_overweight,
                  FAVC, FCVC, NCP, CAEC, SMOKE, CH2O, SCC, FAF, TUE, CALC, MTRANS
        
        Returns:
            tuple: (prediction, probability)
                - prediction: obesity class (0-6)
                - probability: max class probability (0-1)
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
        probabilities = self.model.predict_proba(feature_df)[0]
        max_probability = probabilities[prediction]
        
        return prediction, max_probability
    
    def get_risk_score(self, features):
        """
        Get obesity risk score as percentage (0-100)
        Uses BMI calculation as primary indicator with model as secondary signal
        """
        # Calculate BMI from features (Height is in meters, Weight in kg)
        height = features.get('Height', 1.7)  # meters
        weight = features.get('Weight', 70)   # kg
        bmi = weight / (height ** 2)
        
        # BMI-based risk classification (WHO standards)
        # This ensures accurate risk scores regardless of model uncertainty
        if bmi < 18.5:
            # Underweight
            bmi_risk = 25  # Health risk but not obesity-related
        elif bmi < 25:
            # Normal weight
            bmi_risk = 5  # Very low obesity risk
        elif bmi < 27:
            # Overweight Level I
            bmi_risk = 35
        elif bmi < 30:
            # Overweight Level II
            bmi_risk = 50
        elif bmi < 35:
            # Obesity Type I (Class I)
            bmi_risk = 70
        elif bmi < 40:
            # Obesity Type II (Class II)
            bmi_risk = 85
        else:
            # Obesity Type III (Class III) - Morbid obesity
            bmi_risk = 95
        
        # Get model prediction for additional context
        prediction, probability = self.predict(features)
        
        # Model-based risk mapping
        class_risk_mapping = {
            0: 25,  # Insufficient weight (health concern)
            1: 5,   # Normal weight (low risk)
            2: 35,  # Overweight Level I
            3: 50,  # Overweight Level II
            4: 70,  # Obesity Type I
            5: 85,  # Obesity Type II
            6: 95   # Obesity Type III
        }
        model_risk = class_risk_mapping.get(prediction, 50)
        
        # Use weighted average: 80% BMI (objective), 20% model (lifestyle factors)
        # BMI is the primary indicator, model provides lifestyle context
        final_risk = (bmi_risk * 0.80) + (model_risk * 0.20)
        
        return round(final_risk, 2)


if __name__ == "__main__":
    # Train the model
    model = ObesityModel()
    dataset_path = "../dataset/obesity.csv"
    model.train(dataset_path)
