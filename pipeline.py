"""
Health Assessment Pipeline - Integrates all models and generates comprehensive health reports
"""
import sys
import os

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from models.diabetes_model import DiabetesModel
from models.heart_model import HeartModel
from models.hypertension_model import HypertensionModel
from models.obesity_model import ObesityModel
from feature_mapper import FeatureMapper
from health_scorer import HealthScorer


class HealthAssessmentPipeline:
    """
    Main pipeline that orchestrates the entire health assessment process
    """
    
    def __init__(self, train_models=False):
        """
        Initialize the pipeline
        
        Args:
            train_models (bool): If True, train all models. If False, load existing models.
        """
        print("🏥 Initializing Health Assessment Pipeline...")
        
        # Initialize models
        self.diabetes_model = DiabetesModel()
        self.heart_model = HeartModel()
        self.hypertension_model = HypertensionModel()
        self.obesity_model = ObesityModel()
        
        # Initialize feature mapper and scorer
        self.feature_mapper = FeatureMapper()
        self.health_scorer = HealthScorer()
        
        # Train or load models
        if train_models:
            self._train_all_models()
        else:
            self._load_all_models()
        
        print("✅ Pipeline initialized successfully!\n")
    
    def _train_all_models(self):
        """Train all models with their respective datasets"""
        print("\n🔄 Training all models...")
        
        dataset_dir = "dataset"
        
        try:
            print("\n1️⃣ Training Diabetes Model...")
            self.diabetes_model.train(os.path.join(dataset_dir, "diabetes.csv"))
            
            print("\n2️⃣ Training Heart Disease Model...")
            self.heart_model.train(os.path.join(dataset_dir, "heart.csv"))
            
            print("\n3️⃣ Training Hypertension Model...")
            self.hypertension_model.train(os.path.join(dataset_dir, "hypertension_dataset.csv"))
            
            print("\n4️⃣ Training Obesity Model...")
            self.obesity_model.train(os.path.join(dataset_dir, "obesity.csv"))
            
            print("\n✅ All models trained and saved successfully!")
        
        except Exception as e:
            print(f"\n❌ Error during training: {e}")
            raise
    
    def _load_all_models(self):
        """Load all pre-trained models"""
        print("📂 Loading pre-trained models...")
        
        try:
            models_loaded = []
            models_to_train = []
            
            # Try loading each model with error handling
            try:
                if self.diabetes_model.load_model():
                    models_loaded.append("Diabetes")
                else:
                    models_to_train.append(("Diabetes", self.diabetes_model, "diabetes.csv"))
            except Exception as e:
                print(f"⚠️  Diabetes model load failed: {e}")
                models_to_train.append(("Diabetes", self.diabetes_model, "diabetes.csv"))
            
            try:
                if self.heart_model.load_model():
                    models_loaded.append("Heart")
                else:
                    models_to_train.append(("Heart", self.heart_model, "heart.csv"))
            except Exception as e:
                print(f"⚠️  Heart model load failed: {e}")
                models_to_train.append(("Heart", self.heart_model, "heart.csv"))
            
            try:
                if self.hypertension_model.load_model():
                    models_loaded.append("Hypertension")
                else:
                    models_to_train.append(("Hypertension", self.hypertension_model, "hypertension_dataset.csv"))
            except Exception as e:
                print(f"⚠️  Hypertension model load failed (corrupted file): {e}")
                models_to_train.append(("Hypertension", self.hypertension_model, "hypertension_dataset.csv"))
            
            try:
                if self.obesity_model.load_model():
                    models_loaded.append("Obesity")
                else:
                    models_to_train.append(("Obesity", self.obesity_model, "obesity.csv"))
            except Exception as e:
                print(f"⚠️  Obesity model load failed: {e}")
                models_to_train.append(("Obesity", self.obesity_model, "obesity.csv"))
            
            # Report loaded models
            if models_loaded:
                print(f"✅ Loaded models: {', '.join(models_loaded)}")
            
            # Train missing models
            if models_to_train:
                print(f"\n⚠️  Missing/corrupted models: {', '.join([m[0] for m in models_to_train])}")
                print("🔄 Training models (first time only - takes 2-3 minutes)...\n")
                
                dataset_dir = "dataset"
                for name, model, dataset_file in models_to_train:
                    print(f"🔨 Training {name} Model...")
                    try:
                        import time
                        start = time.time()
                        model.train(os.path.join(dataset_dir, dataset_file))
                        duration = time.time() - start
                        print(f"✅ {name} Model trained in {duration:.1f}s!")
                    except Exception as e:
                        print(f"❌ Failed to train {name} Model: {e}")
                        import traceback
                        traceback.print_exc()
                        raise
                
                print("\n✅ All models ready!")
        
        except Exception as e:
            print(f"\n❌ Critical error during model initialization: {e}")
            raise
    
    def assess_health(self, user_data, verbose=True):
        """
        Perform comprehensive health assessment
        
        Args:
            user_data (dict): User health information
            verbose (bool): If True, print detailed progress
        
        Returns:
            dict: Complete health assessment report
        """
        if verbose:
            print("\n" + "="*80)
            print("🔍 ANALYZING HEALTH DATA...")
            print("="*80)
        
        # Step 1: Map user data to model-specific features
        if verbose:
            print("\n📋 Step 1: Processing input data and extracting features...")
        
        features = self.feature_mapper.get_all_features(user_data)
        
        # Step 2: Get predictions from each model
        if verbose:
            print("🤖 Step 2: Running predictions across all health models...")
        
        risk_scores = {}
        
        try:
            # Diabetes prediction
            if verbose:
                print("   ├─ Analyzing diabetes risk...")
            risk_scores['diabetes'] = self.diabetes_model.get_risk_score(features['diabetes'])
            
            # Heart disease prediction
            if verbose:
                print("   ├─ Analyzing heart disease risk...")
            risk_scores['heart'] = self.heart_model.get_risk_score(features['heart'])
            
            # Hypertension prediction
            if verbose:
                print("   ├─ Analyzing hypertension risk...")
            risk_scores['hypertension'] = self.hypertension_model.get_risk_score(features['hypertension'])
            
            # Obesity prediction
            if verbose:
                print("   └─ Analyzing obesity risk...")
            risk_scores['obesity'] = self.obesity_model.get_risk_score(features['obesity'])
        
        except Exception as e:
            print(f"\n❌ Error during prediction: {e}")
            raise
        
        # Step 3: Calculate composite health score
        if verbose:
            print("\n📊 Step 3: Calculating composite health score...")
        
        health_report = self.health_scorer.generate_health_report(risk_scores)
        
        # Step 4: Add user data to report
        health_report['user_data'] = user_data
        health_report['feature_sets'] = features
        
        if verbose:
            print("✅ Assessment complete!\n")
        
        return health_report
    
    def print_report(self, health_report):
        """
        Print formatted health assessment report
        
        Args:
            health_report (dict): Health report from assess_health()
        """
        self.health_scorer.print_health_report(health_report)
    
    def assess_and_report(self, user_data):
        """
        Convenience method: Assess health and print report
        
        Args:
            user_data (dict): User health information
        
        Returns:
            dict: Health assessment report
        """
        report = self.assess_health(user_data, verbose=True)
        self.print_report(report)
        return report
    
    def batch_assess(self, users_data_list):
        """
        Assess health for multiple users
        
        Args:
            users_data_list (list): List of user data dictionaries
        
        Returns:
            list: List of health reports
        """
        print(f"\n🔄 Processing batch assessment for {len(users_data_list)} users...")
        
        reports = []
        for i, user_data in enumerate(users_data_list, 1):
            print(f"\n{'='*80}")
            print(f"Processing User {i}/{len(users_data_list)}")
            print(f"{'='*80}")
            
            report = self.assess_health(user_data, verbose=False)
            reports.append(report)
            
            print(f"✅ User {i} assessment complete. Health Score: {report['health_score']:.1f}/100")
        
        return reports
    
    def export_report_to_file(self, health_report, filename="health_report.txt"):
        """
        Export health report to text file
        
        Args:
            health_report (dict): Health report from assess_health()
            filename (str): Output filename
        """
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("           COMPREHENSIVE HEALTH ASSESSMENT REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"OVERALL HEALTH SCORE: {health_report['health_score']:.1f}/100\n")
            f.write(f"HEALTH GRADE: {health_report['health_grade']}\n")
            f.write(f"COMPOSITE RISK: {health_report['composite_risk']:.1f}%\n")
            f.write(f"RISK LEVEL: {health_report['risk_level'].upper()}\n\n")
            
            f.write("-"*80 + "\n")
            f.write("INDIVIDUAL RISK SCORES:\n")
            f.write("-"*80 + "\n")
            
            risks = health_report['individual_risks']
            f.write(f"Heart Disease:  {risks['heart_disease']['score']:.1f}% ({risks['heart_disease']['level']})\n")
            f.write(f"Diabetes:       {risks['diabetes']['score']:.1f}% ({risks['diabetes']['level']})\n")
            f.write(f"Hypertension:   {risks['hypertension']['score']:.1f}% ({risks['hypertension']['level']})\n")
            f.write(f"Obesity:        {risks['obesity']['score']:.1f}% ({risks['obesity']['level']})\n\n")
            
            f.write("-"*80 + "\n")
            f.write("RECOMMENDATIONS:\n")
            f.write("-"*80 + "\n")
            for rec in health_report['recommendations']:
                f.write(f"{rec}\n")
            
            f.write("\n" + "="*80 + "\n")
        
        print(f"📄 Report exported to {filename}")


if __name__ == "__main__":
    # Example usage
    print("="*80)
    print("           HEALTH ASSESSMENT PIPELINE - TEST RUN")
    print("="*80)
    
    # Initialize pipeline (will train models if not found)
    pipeline = HealthAssessmentPipeline(train_models=False)
    
    # Sample user data
    test_user = {
        'age': 45,
        'gender': 'Male',
        'height': 175,
        'weight': 85,
        'systolic_bp': 135,
        'diastolic_bp': 88,
        'glucose': 115,
        'cholesterol': 225,
        'ldl': 140,
        'hdl': 45,
        'triglycerides': 180,
        'resting_heart_rate': 75,
        'max_heart_rate': 160,
        'smoking_status': 'Former',
        'alcohol_intake': 'Moderate',
        'physical_activity': 'Low',
        'sleep_hours': 6,
        'stress_level': 'High',
        'family_history_diabetes': 'yes',
        'family_history_hypertension': 'yes',
        'pregnancies': 0,
        'insulin': 85
    }
    
    # Run assessment
    report = pipeline.assess_and_report(test_user)
    
    # Export report
    pipeline.export_report_to_file(report, "sample_health_report.txt")
