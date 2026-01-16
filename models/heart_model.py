"""
Heart Disease Prediction Model
Features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os


class HeartModel:
    def __init__(self, model_path='saved_models/heart_model.pkl'):
        self.model = None
        self.model_path = model_path
        self.feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
                              'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
    def train(self, data_path):
        """Train the heart disease prediction model"""
        # Load dataset
        df = pd.read_csv(data_path)
        
        # Define features and target
        X = df.drop('target', axis=1)
        y = df['target']
        
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
        
        print(f"Heart Model Training Accuracy: {accuracy:.4f}")
        
        # Save model
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Heart model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("Heart model loaded successfully")
            return True
        else:
            print(f"No saved model found at {self.model_path}")
            return False
    
    def predict(self, features):
        """
        Predict heart disease risk
        
        Args:
            features (dict): Dictionary with keys:
                - age, sex, cp, trestbps, chol, fbs, restecg, 
                  thalach, exang, oldpeak, slope, ca, thal
        
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
            features.get('age', 0),
            features.get('sex', 0),
            features.get('cp', 0),
            features.get('trestbps', 0),
            features.get('chol', 0),
            features.get('fbs', 0),
            features.get('restecg', 0),
            features.get('thalach', 0),
            features.get('exang', 0),
            features.get('oldpeak', 0),
            features.get('slope', 0),
            features.get('ca', 0),
            features.get('thal', 0)
        ]])
        
        # Predict
        prediction = self.model.predict(feature_array)[0]
        probability = self.model.predict_proba(feature_array)[0][1]
        
        return prediction, probability
    
    def get_risk_score(self, features):
        """
        Get risk score as percentage (0-100)
        Uses a hybrid approach: ML model + clinical risk factors
        """
        # Get ML model prediction
        _, probability = self.predict(features)
        ml_risk = probability * 100
        
        # Calculate clinical risk score based on available general health data
        # This provides a more reliable baseline when specialized cardiac features are unavailable
        risk_factors = 0
        max_factors = 0
        
        # Age risk (major factor)
        age = features.get('age', 0)
        max_factors += 20
        if age >= 65:
            risk_factors += 20
        elif age >= 55:
            risk_factors += 15
        elif age >= 45:
            risk_factors += 10
        elif age >= 35:
            risk_factors += 5
        # Ages under 35 add 0 risk
        
        # Blood pressure risk (major factor)
        bp = features.get('trestbps', 120)
        max_factors += 20
        if bp >= 180:
            risk_factors += 20
        elif bp >= 160:
            risk_factors += 15
        elif bp >= 140:
            risk_factors += 10
        elif bp >= 130:
            risk_factors += 5
        elif bp >= 120:
            risk_factors += 2
        # BP under 120 adds 0 risk
        
        # Cholesterol risk (major factor)
        chol = features.get('chol', 200)
        max_factors += 20
        if chol >= 280:
            risk_factors += 20
        elif chol >= 240:
            risk_factors += 15
        elif chol >= 220:
            risk_factors += 10
        elif chol >= 200:
            risk_factors += 5
        elif chol >= 180:
            risk_factors += 2
        # Cholesterol under 180 adds 0 risk
        
        # Max heart rate (inverse - lower is worse for given age)
        max_hr = features.get('thalach', 150)
        age = features.get('age', 30)
        expected_max_hr = 220 - age
        max_factors += 15
        if max_hr < expected_max_hr * 0.65:  # Very low exercise capacity
            risk_factors += 15
        elif max_hr < expected_max_hr * 0.75:
            risk_factors += 10
        elif max_hr < expected_max_hr * 0.85:
            risk_factors += 5
        elif max_hr < expected_max_hr * 0.90:
            risk_factors += 2
        # Max HR >= 90% of expected adds 0 risk
        
        # Fasting blood sugar
        max_factors += 10
        if features.get('fbs', 0) == 1:  # Glucose > 120
            risk_factors += 10
        
        # Chest pain type (if available and not default)
        cp = features.get('cp', -1)
        if cp >= 0:  # Only count if explicitly provided
            max_factors += 15
            if cp == 0:  # Typical angina
                risk_factors += 15
            elif cp == 1:  # Atypical angina
                risk_factors += 10
            elif cp == 2:  # Non-anginal pain
                risk_factors += 5
        
        # Calculate clinical risk percentage
        clinical_risk = (risk_factors / max_factors * 100) if max_factors > 0 else 50
        
        # Weighted average: 30% ML model, 70% clinical factors
        # Clinical factors weighted more heavily because ML model is unreliable
        # without specialized cardiac test features
        final_risk = (ml_risk * 0.30) + (clinical_risk * 0.70)
        
        return round(final_risk, 2)


if __name__ == "__main__":
    # Train the model
    model = HeartModel()
    dataset_path = "../dataset/heart.csv"
    model.train(dataset_path)
