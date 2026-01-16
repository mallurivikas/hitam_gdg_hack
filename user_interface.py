"""
User Interface - Interactive CLI for collecting health information
"""


class UserInterface:
    """
    Interactive command-line interface for collecting user health data
    """
    
    def __init__(self):
        self.user_data = {}
    
    def _get_input(self, prompt, default=None, input_type=str, validation=None):
        """
        Get validated input from user
        
        Args:
            prompt (str): Question to ask user
            default: Default value if user presses Enter
            input_type: Type to convert input to (int, float, str)
            validation: Function to validate input
        
        Returns:
            Validated user input
        """
        while True:
            try:
                default_str = f" (default: {default})" if default is not None else ""
                user_input = input(f"{prompt}{default_str}: ").strip()
                
                # Use default if no input
                if not user_input and default is not None:
                    return default
                
                # Convert to appropriate type
                if input_type == int:
                    value = int(user_input)
                elif input_type == float:
                    value = float(user_input)
                else:
                    value = user_input
                
                # Validate if validation function provided
                if validation and not validation(value):
                    print("❌ Invalid input. Please try again.")
                    continue
                
                return value
            
            except ValueError:
                print(f"❌ Please enter a valid {input_type.__name__}")
            except KeyboardInterrupt:
                print("\n\n⚠️  Input cancelled by user.")
                raise
    
    def _get_yes_no(self, prompt, default='no'):
        """Get yes/no input from user"""
        response = self._get_input(f"{prompt} (yes/no)", default=default)
        return response.lower() in ['yes', 'y', '1', 'true']
    
    def _get_choice(self, prompt, choices, default=None):
        """Get choice from list of options"""
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            default_marker = " ← default" if choice == default else ""
            print(f"  {i}. {choice}{default_marker}")
        
        while True:
            try:
                choice_input = input(f"Enter choice (1-{len(choices)}): ").strip()
                
                if not choice_input and default:
                    return default
                
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    return choices[choice_num - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def collect_basic_info(self):
        """Collect basic demographic information"""
        print("\n" + "="*80)
        print("                    👤 BASIC INFORMATION")
        print("="*80)
        
        self.user_data['age'] = self._get_input(
            "Age (years)", 
            default=30, 
            input_type=int,
            validation=lambda x: 1 <= x <= 120
        )
        
        self.user_data['gender'] = self._get_choice(
            "Gender",
            choices=['Male', 'Female', 'Other'],
            default='Male'
        )
        
        self.user_data['height'] = self._get_input(
            "Height (cm)",
            default=170,
            input_type=float,
            validation=lambda x: 50 <= x <= 250
        )
        
        self.user_data['weight'] = self._get_input(
            "Weight (kg)",
            default=70,
            input_type=float,
            validation=lambda x: 20 <= x <= 300
        )
        
        # Calculate and display BMI
        bmi = self.user_data['weight'] / ((self.user_data['height'] / 100) ** 2)
        print(f"\n📊 Calculated BMI: {bmi:.1f}")
        
        if self.user_data['gender'].lower() == 'female':
            self.user_data['pregnancies'] = self._get_input(
                "Number of pregnancies",
                default=0,
                input_type=int,
                validation=lambda x: x >= 0
            )
        else:
            self.user_data['pregnancies'] = 0
    
    def collect_vital_signs(self):
        """Collect vital signs and measurements"""
        print("\n" + "="*80)
        print("                    💓 VITAL SIGNS")
        print("="*80)
        
        self.user_data['systolic_bp'] = self._get_input(
            "Systolic Blood Pressure (mm Hg)",
            default=120,
            input_type=int,
            validation=lambda x: 70 <= x <= 200
        )
        
        self.user_data['diastolic_bp'] = self._get_input(
            "Diastolic Blood Pressure (mm Hg)",
            default=80,
            input_type=int,
            validation=lambda x: 40 <= x <= 130
        )
        
        self.user_data['resting_heart_rate'] = self._get_input(
            "Resting Heart Rate (bpm)",
            default=70,
            input_type=int,
            validation=lambda x: 40 <= x <= 150
        )
        
        self.user_data['max_heart_rate'] = self._get_input(
            "Maximum Heart Rate during exercise (bpm)",
            default=150,
            input_type=int,
            validation=lambda x: 60 <= x <= 220
        )
    
    def collect_blood_tests(self):
        """Collect blood test results"""
        print("\n" + "="*80)
        print("                    🩸 BLOOD TEST RESULTS")
        print("="*80)
        print("(If you don't have recent blood test results, you can use default values)")
        
        self.user_data['glucose'] = self._get_input(
            "Fasting Blood Glucose (mg/dL)",
            default=100,
            input_type=float,
            validation=lambda x: 50 <= x <= 400
        )
        
        self.user_data['cholesterol'] = self._get_input(
            "Total Cholesterol (mg/dL)",
            default=200,
            input_type=float,
            validation=lambda x: 100 <= x <= 500
        )
        
        self.user_data['ldl'] = self._get_input(
            "LDL Cholesterol (mg/dL)",
            default=100,
            input_type=float,
            validation=lambda x: 40 <= x <= 300
        )
        
        self.user_data['hdl'] = self._get_input(
            "HDL Cholesterol (mg/dL)",
            default=50,
            input_type=float,
            validation=lambda x: 20 <= x <= 100
        )
        
        self.user_data['triglycerides'] = self._get_input(
            "Triglycerides (mg/dL)",
            default=150,
            input_type=float,
            validation=lambda x: 50 <= x <= 500
        )
        
        self.user_data['insulin'] = self._get_input(
            "Insulin level (mu U/ml)",
            default=80,
            input_type=float,
            validation=lambda x: 0 <= x <= 300
        )
    
    def collect_lifestyle(self):
        """Collect lifestyle information"""
        print("\n" + "="*80)
        print("                    🏃 LIFESTYLE HABITS")
        print("="*80)
        
        self.user_data['smoking_status'] = self._get_choice(
            "Smoking Status",
            choices=['Never', 'Former', 'Current'],
            default='Never'
        )
        
        self.user_data['alcohol_intake'] = self._get_choice(
            "Alcohol Intake",
            choices=['None', 'Moderate', 'Heavy'],
            default='None'
        )
        
        self.user_data['physical_activity'] = self._get_choice(
            "Physical Activity Level",
            choices=['Low', 'Moderate', 'High'],
            default='Moderate'
        )
        
        self.user_data['sleep_hours'] = self._get_input(
            "Average sleep duration (hours per night)",
            default=7,
            input_type=float,
            validation=lambda x: 0 <= x <= 24
        )
        
        self.user_data['stress_level'] = self._get_choice(
            "Stress Level",
            choices=['Low', 'Moderate', 'High'],
            default='Moderate'
        )
        
        self.user_data['salt_intake'] = self._get_choice(
            "Salt Intake",
            choices=['Low', 'Moderate', 'High'],
            default='Moderate'
        )
    
    def collect_diet_habits(self):
        """Collect diet and eating habits"""
        print("\n" + "="*80)
        print("                    🍽️ DIET HABITS")
        print("="*80)
        
        self.user_data['vegetable_consumption_frequency'] = self._get_input(
            "Vegetable consumption frequency (1=rarely, 2=sometimes, 3=always)",
            default=2,
            input_type=int,
            validation=lambda x: 1 <= x <= 3
        )
        
        self.user_data['num_main_meals'] = self._get_input(
            "Number of main meals per day",
            default=3,
            input_type=int,
            validation=lambda x: 1 <= x <= 6
        )
        
        self.user_data['daily_water_consumption'] = self._get_input(
            "Daily water consumption (liters)",
            default=2,
            input_type=float,
            validation=lambda x: 0 <= x <= 10
        )
        
        self.user_data['frequent_high_caloric_food'] = 'yes' if self._get_yes_no(
            "Do you frequently consume high caloric food?"
        ) else 'no'
        
        self.user_data['food_between_meals'] = self._get_choice(
            "Food consumption between meals",
            choices=['no', 'Sometimes', 'Frequently', 'Always'],
            default='Sometimes'
        )
        
        self.user_data['calorie_monitoring'] = 'yes' if self._get_yes_no(
            "Do you monitor your calorie consumption?"
        ) else 'no'
    
    def collect_medical_history(self):
        """Collect medical and family history"""
        print("\n" + "="*80)
        print("                    🏥 MEDICAL & FAMILY HISTORY")
        print("="*80)
        
        self.user_data['family_history_diabetes'] = 'yes' if self._get_yes_no(
            "Family history of diabetes?"
        ) else 'no'
        
        self.user_data['family_history_hypertension'] = 'Yes' if self._get_yes_no(
            "Family history of hypertension?"
        ) else 'No'
        
        self.user_data['family_history_overweight'] = 'yes' if self._get_yes_no(
            "Family history of overweight/obesity?"
        ) else 'no'
        
        self.user_data['has_diabetes'] = 'Yes' if self._get_yes_no(
            "Have you been diagnosed with diabetes?"
        ) else 'No'
    
    def collect_additional_info(self):
        """Collect additional health information"""
        print("\n" + "="*80)
        print("                    ℹ️ ADDITIONAL INFORMATION")
        print("="*80)
        
        self.user_data['chest_pain_type'] = self._get_input(
            "Chest pain type (0=none, 1=typical angina, 2=atypical, 3=non-anginal)",
            default=0,
            input_type=int,
            validation=lambda x: 0 <= x <= 3
        )
        
        self.user_data['exercise_induced_angina'] = 'yes' if self._get_yes_no(
            "Experience chest pain during exercise?"
        ) else 'no'
        
        self.user_data['physical_activity_frequency'] = self._get_input(
            "Physical activity frequency per week (0-7 days)",
            default=3,
            input_type=int,
            validation=lambda x: 0 <= x <= 7
        )
        
        self.user_data['tech_usage_time'] = self._get_input(
            "Technology usage time per day (hours)",
            default=2,
            input_type=float,
            validation=lambda x: 0 <= x <= 24
        )
        
        self.user_data['transportation_mode'] = self._get_choice(
            "Primary mode of transportation",
            choices=['Walking', 'Bike', 'Public_Transportation', 'Automobile', 'Motorbike'],
            default='Public_Transportation'
        )
        
        self.user_data['smokes'] = 'yes' if self.user_data.get('smoking_status', 'Never') == 'Current' else 'no'
        
        # Additional default values for features not collected
        self.user_data['skin_thickness'] = 20
        self.user_data['st_depression'] = 0
        self.user_data['slope_st_segment'] = 1
        self.user_data['num_major_vessels'] = 0
        self.user_data['thalassemia'] = 2
        self.user_data['resting_ecg'] = 0
    
    def collect_all(self):
        """
        Collect all health information from user
        
        Returns:
            dict: Complete user health data
        """
        print("\n" + "="*80)
        print("          🏥 COMPREHENSIVE HEALTH ASSESSMENT - DATA COLLECTION 🏥")
        print("="*80)
        print("\nWelcome! This assessment will collect information about your health.")
        print("Please answer the following questions as accurately as possible.")
        print("You can press Enter to use default values where applicable.")
        print("\n⚠️  Note: This is not a medical diagnosis. Consult healthcare professionals.")
        
        try:
            self.collect_basic_info()
            self.collect_vital_signs()
            self.collect_blood_tests()
            self.collect_lifestyle()
            self.collect_diet_habits()
            self.collect_medical_history()
            self.collect_additional_info()
            
            print("\n" + "="*80)
            print("✅ Data collection complete! Processing your health assessment...")
            print("="*80)
            
            return self.user_data
        
        except KeyboardInterrupt:
            print("\n\n❌ Assessment cancelled by user.")
            return None
    
    def quick_collect(self):
        """
        Quick data collection with minimal questions
        
        Returns:
            dict: Basic user health data
        """
        print("\n" + "="*80)
        print("          🏥 QUICK HEALTH ASSESSMENT")
        print("="*80)
        print("\nThis is a simplified assessment. For comprehensive results, use full assessment.")
        
        try:
            # Essential information only
            self.user_data['age'] = self._get_input("Age", default=30, input_type=int)
            self.user_data['gender'] = self._get_choice("Gender", ['Male', 'Female'], 'Male')
            self.user_data['height'] = self._get_input("Height (cm)", default=170, input_type=float)
            self.user_data['weight'] = self._get_input("Weight (kg)", default=70, input_type=float)
            self.user_data['systolic_bp'] = self._get_input("Blood Pressure (systolic)", default=120, input_type=int)
            self.user_data['diastolic_bp'] = self._get_input("Blood Pressure (diastolic)", default=80, input_type=int)
            self.user_data['glucose'] = self._get_input("Blood Glucose (mg/dL)", default=100, input_type=float)
            self.user_data['cholesterol'] = self._get_input("Cholesterol (mg/dL)", default=200, input_type=float)
            
            # Set defaults for other fields
            self._set_defaults()
            
            return self.user_data
        
        except KeyboardInterrupt:
            print("\n\n❌ Assessment cancelled.")
            return None
    
    def _set_defaults(self):
        """Set default values for fields not collected in quick mode"""
        defaults = {
            'pregnancies': 0,
            'resting_heart_rate': 70,
            'max_heart_rate': 150,
            'ldl': 100,
            'hdl': 50,
            'triglycerides': 150,
            'insulin': 80,
            'smoking_status': 'Never',
            'alcohol_intake': 'None',
            'physical_activity': 'Moderate',
            'sleep_hours': 7,
            'stress_level': 'Moderate',
            'salt_intake': 'Moderate',
            'vegetable_consumption_frequency': 2,
            'num_main_meals': 3,
            'daily_water_consumption': 2,
            'frequent_high_caloric_food': 'no',
            'food_between_meals': 'Sometimes',
            'calorie_monitoring': 'no',
            'family_history_diabetes': 'no',
            'family_history_hypertension': 'No',
            'family_history_overweight': 'no',
            'has_diabetes': 'No',
            'chest_pain_type': 0,
            'exercise_induced_angina': 'no',
            'physical_activity_frequency': 3,
            'tech_usage_time': 2,
            'transportation_mode': 'Public_Transportation',
            'smokes': 'no',
            'skin_thickness': 20,
            'st_depression': 0,
            'slope_st_segment': 1,
            'num_major_vessels': 0,
            'thalassemia': 2,
            'resting_ecg': 0
        }
        
        for key, value in defaults.items():
            if key not in self.user_data:
                self.user_data[key] = value


if __name__ == "__main__":
    # Test the user interface
    ui = UserInterface()
    
    print("\nTest Mode: Choose assessment type")
    print("1. Full Assessment")
    print("2. Quick Assessment")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        data = ui.collect_all()
    else:
        data = ui.quick_collect()
    
    if data:
        print("\n✅ Collected Data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
