"""
Feature Mapper - Maps user inputs to model-specific features
Handles data preprocessing and feature engineering for all models
"""


class FeatureMapper:
    """
    Maps user-provided health data to features required by each model.
    Handles missing values with reasonable defaults and performs feature derivation.
    """
    
    def __init__(self):
        # Define required features for each model
        self.diabetes_features = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        
        self.heart_features = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        self.hypertension_features = [
            'Age', 'BMI', 'Cholesterol', 'Systolic_BP', 'Diastolic_BP',
            'Smoking_Status', 'Alcohol_Intake', 'Physical_Activity_Level',
            'Family_History', 'Diabetes', 'Stress_Level', 'Salt_Intake',
            'Sleep_Duration', 'Heart_Rate', 'LDL', 'HDL', 'Triglycerides',
            'Glucose', 'Gender'
        ]
        
        self.obesity_features = [
            'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
            'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',
            'CALC', 'MTRANS'
        ]
    
    def calculate_bmi(self, height_cm, weight_kg):
        """Calculate BMI from height (cm) and weight (kg)"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    def map_to_diabetes_features(self, user_data):
        """
        Map user data to diabetes model features
        
        Args:
            user_data (dict): User health information
        
        Returns:
            dict: Features formatted for diabetes model
        """
        features = {
            'Pregnancies': user_data.get('pregnancies', 0),
            'Glucose': user_data.get('glucose', user_data.get('fasting_glucose', 100)),
            'BloodPressure': user_data.get('blood_pressure', 
                                          user_data.get('systolic_bp', 80)),
            'SkinThickness': user_data.get('skin_thickness', 20),
            'Insulin': user_data.get('insulin', 80),
            'BMI': user_data.get('bmi', 
                                 self.calculate_bmi(user_data.get('height', 170),
                                                   user_data.get('weight', 70))),
            'DiabetesPedigreeFunction': user_data.get('diabetes_pedigree', 
                                                      0.5 if user_data.get('family_history_diabetes', 'no').lower() == 'yes' else 0.2),
            'Age': user_data.get('age', 30)
        }
        return features
    
    def map_to_heart_features(self, user_data):
        """
        Map user data to heart disease model features
        
        Args:
            user_data (dict): User health information
        
        Returns:
            dict: Features formatted for heart model
        """
        # Gender mapping: Male=1, Female=0
        sex = 1 if user_data.get('gender', 'male').lower() in ['male', 'm', '1'] else 0
        
        features = {
            'age': user_data.get('age', 30),
            'sex': sex,
            'cp': user_data.get('chest_pain_type', 0),  # 0-3: chest pain type
            'trestbps': user_data.get('systolic_bp', user_data.get('resting_bp', 120)),
            'chol': user_data.get('cholesterol', 200),
            'fbs': 1 if user_data.get('fasting_glucose', 100) > 120 else 0,
            'restecg': user_data.get('resting_ecg', 0),  # 0-2
            'thalach': user_data.get('max_heart_rate', 150),
            'exang': 1 if user_data.get('exercise_induced_angina', 'no').lower() == 'yes' else 0,
            'oldpeak': user_data.get('st_depression', 0),
            'slope': user_data.get('slope_st_segment', 1),  # 0-2
            'ca': user_data.get('num_major_vessels', 0),  # 0-3
            'thal': user_data.get('thalassemia', 2)  # 1-3
        }
        return features
    
    def map_to_hypertension_features(self, user_data):
        """
        Map user data to hypertension model features
        
        Args:
            user_data (dict): User health information
        
        Returns:
            dict: Features formatted for hypertension model
        """
        features = {
            'Age': user_data.get('age', 30),
            'BMI': user_data.get('bmi',
                                 self.calculate_bmi(user_data.get('height', 170),
                                                   user_data.get('weight', 70))),
            'Cholesterol': user_data.get('cholesterol', 200),
            'Systolic_BP': user_data.get('systolic_bp', 120),
            'Diastolic_BP': user_data.get('diastolic_bp', 80),
            'Smoking_Status': user_data.get('smoking_status', 'Never'),
            'Alcohol_Intake': user_data.get('alcohol_intake', 'None'),
            'Physical_Activity_Level': user_data.get('physical_activity', 'Moderate'),
            'Family_History': user_data.get('family_history_hypertension', 'No'),
            'Diabetes': user_data.get('has_diabetes', 'No'),
            'Stress_Level': user_data.get('stress_level', 'Moderate'),
            'Salt_Intake': user_data.get('salt_intake', 'Moderate'),
            'Sleep_Duration': user_data.get('sleep_hours', 7),
            'Heart_Rate': user_data.get('resting_heart_rate', 70),
            'LDL': user_data.get('ldl', 100),
            'HDL': user_data.get('hdl', 50),
            'Triglycerides': user_data.get('triglycerides', 150),
            'Glucose': user_data.get('glucose', user_data.get('fasting_glucose', 100)),
            'Gender': user_data.get('gender', 'Male')
        }
        return features
    
    def map_to_obesity_features(self, user_data):
        """
        Map user data to obesity model features
        
        Args:
            user_data (dict): User health information
        
        Returns:
            dict: Features formatted for obesity model
        """
        features = {
            'Gender': user_data.get('gender', 'Male'),
            'Age': user_data.get('age', 30),
            'Height': user_data.get('height', 170) / 100,  # Convert cm to meters
            'Weight': user_data.get('weight', 70),
            'family_history_with_overweight': user_data.get('family_history_overweight', 'no'),
            'FAVC': user_data.get('frequent_high_caloric_food', 'no'),
            'FCVC': user_data.get('vegetable_consumption_frequency', 2),  # 1-3
            'NCP': user_data.get('num_main_meals', 3),  # 1-4
            'CAEC': user_data.get('food_between_meals', 'Sometimes'),
            'SMOKE': user_data.get('smokes', 'no'),
            'CH2O': user_data.get('daily_water_consumption', 2),  # liters
            'SCC': user_data.get('calorie_monitoring', 'no'),
            'FAF': user_data.get('physical_activity_frequency', 1),  # 0-3
            'TUE': user_data.get('tech_usage_time', 1),  # hours
            'CALC': user_data.get('alcohol_consumption', 'no'),
            'MTRANS': user_data.get('transportation_mode', 'Public_Transportation')
        }
        return features
    
    def get_all_features(self, user_data):
        """
        Generate feature sets for all models from user data
        
        Args:
            user_data (dict): Comprehensive user health information
        
        Returns:
            dict: Dictionary containing feature sets for all models
        """
        return {
            'diabetes': self.map_to_diabetes_features(user_data),
            'heart': self.map_to_heart_features(user_data),
            'hypertension': self.map_to_hypertension_features(user_data),
            'obesity': self.map_to_obesity_features(user_data)
        }
    
    def get_required_inputs(self):
        """
        Get list of all inputs needed from user
        
        Returns:
            dict: Categorized required inputs with descriptions
        """
        return {
            'basic_info': {
                'age': 'Age in years',
                'gender': 'Gender (Male/Female)',
                'height': 'Height in cm',
                'weight': 'Weight in kg'
            },
            'vital_signs': {
                'systolic_bp': 'Systolic Blood Pressure (mm Hg)',
                'diastolic_bp': 'Diastolic Blood Pressure (mm Hg)',
                'resting_heart_rate': 'Resting Heart Rate (bpm)',
                'max_heart_rate': 'Maximum Heart Rate during exercise (bpm)'
            },
            'blood_tests': {
                'glucose': 'Fasting Blood Glucose (mg/dL)',
                'cholesterol': 'Total Cholesterol (mg/dL)',
                'ldl': 'LDL Cholesterol (mg/dL)',
                'hdl': 'HDL Cholesterol (mg/dL)',
                'triglycerides': 'Triglycerides (mg/dL)',
                'insulin': 'Insulin level (mu U/ml)'
            },
            'lifestyle': {
                'smoking_status': 'Smoking Status (Never/Former/Current)',
                'alcohol_intake': 'Alcohol Intake (None/Moderate/Heavy)',
                'physical_activity': 'Physical Activity Level (Low/Moderate/High)',
                'sleep_hours': 'Average sleep duration (hours)',
                'stress_level': 'Stress Level (Low/Moderate/High)',
                'salt_intake': 'Salt Intake (Low/Moderate/High)'
            },
            'medical_history': {
                'family_history_diabetes': 'Family history of diabetes (yes/no)',
                'family_history_hypertension': 'Family history of hypertension (yes/no)',
                'family_history_overweight': 'Family history of overweight (yes/no)',
                'pregnancies': 'Number of pregnancies (if female)'
            },
            'diet_habits': {
                'vegetable_consumption_frequency': 'Vegetable consumption frequency (1-3)',
                'num_main_meals': 'Number of main meals per day (1-4)',
                'daily_water_consumption': 'Daily water consumption (liters)',
                'frequent_high_caloric_food': 'Frequent consumption of high caloric food (yes/no)'
            }
        }


if __name__ == "__main__":
    # Test feature mapping
    mapper = FeatureMapper()
    
    # Sample user data
    test_user = {
        'age': 45,
        'gender': 'Male',
        'height': 175,
        'weight': 85,
        'systolic_bp': 130,
        'diastolic_bp': 85,
        'glucose': 110,
        'cholesterol': 220,
        'smoking_status': 'Former',
        'physical_activity': 'Moderate',
        'family_history_diabetes': 'yes'
    }
    
    features = mapper.get_all_features(test_user)
    
    print("Feature Mapping Test:")
    print("\nDiabetes Features:", features['diabetes'])
    print("\nHeart Features:", features['heart'])
    print("\nHypertension Features:", features['hypertension'])
    print("\nObesity Features:", features['obesity'])
