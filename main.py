"""
Main Application - Integrated Health Assessment System
Entry point for the complete health assessment pipeline
"""
import sys
from pipeline import HealthAssessmentPipeline
from user_interface import UserInterface


def print_welcome():
    """Print welcome banner"""
    print("\n" + "="*80)
    print("""
    ██╗  ██╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗     █████╗ ██╗
    ██║  ██║██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║    ██╔══██╗██║
    ███████║█████╗  ███████║██║     ██║   ███████║    ███████║██║
    ██╔══██║██╔══╝  ██╔══██║██║     ██║   ██╔══██║    ██╔══██║██║
    ██║  ██║███████╗██║  ██║███████╗██║   ██║  ██║    ██║  ██║██║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝
    
          INTEGRATED HEALTH ASSESSMENT SYSTEM v1.0
          Comprehensive AI-Powered Health Risk Analysis
    """)
    print("="*80)
    print("\n🔬 Analyzing: Diabetes | Heart Disease | Hypertension | Obesity")
    print("⚕️  Disclaimer: This is an AI assessment tool, not a medical diagnosis.")
    print("   Always consult qualified healthcare professionals for medical advice.\n")
    print("="*80)


def print_menu():
    """Print main menu options"""
    print("\n" + "="*80)
    print("                           MAIN MENU")
    print("="*80)
    print("\n  1. 🏥 Full Health Assessment (Comprehensive)")
    print("  2. ⚡ Quick Health Assessment (Essential metrics only)")
    print("  3. 📊 Use Sample Patient Data (Demo)")
    print("  4. 🔧 Retrain All Models")
    print("  5. ℹ️  About This System")
    print("  6. 🚪 Exit")
    print("\n" + "="*80)


def get_sample_patient_data():
    """Return sample patient data for demonstration"""
    return {
        'age': 52,
        'gender': 'Male',
        'height': 178,
        'weight': 92,
        'systolic_bp': 142,
        'diastolic_bp': 92,
        'glucose': 126,
        'cholesterol': 245,
        'ldl': 155,
        'hdl': 42,
        'triglycerides': 195,
        'resting_heart_rate': 78,
        'max_heart_rate': 145,
        'smoking_status': 'Former',
        'alcohol_intake': 'Moderate',
        'physical_activity': 'Low',
        'sleep_hours': 5.5,
        'stress_level': 'High',
        'salt_intake': 'High',
        'vegetable_consumption_frequency': 1,
        'num_main_meals': 2,
        'daily_water_consumption': 1.5,
        'frequent_high_caloric_food': 'yes',
        'food_between_meals': 'Frequently',
        'calorie_monitoring': 'no',
        'family_history_diabetes': 'yes',
        'family_history_hypertension': 'Yes',
        'family_history_overweight': 'yes',
        'has_diabetes': 'No',
        'pregnancies': 0,
        'insulin': 95,
        'chest_pain_type': 1,
        'exercise_induced_angina': 'yes',
        'physical_activity_frequency': 1,
        'tech_usage_time': 4,
        'transportation_mode': 'Automobile',
        'smokes': 'no',
        'skin_thickness': 25,
        'st_depression': 1.2,
        'slope_st_segment': 2,
        'num_major_vessels': 1,
        'thalassemia': 3,
        'resting_ecg': 1
    }


def print_about():
    """Print information about the system"""
    print("\n" + "="*80)
    print("                    ABOUT THIS SYSTEM")
    print("="*80)
    print("""
📋 SYSTEM OVERVIEW:
   This Integrated Health Assessment System uses machine learning to analyze
   multiple health risk factors and provide a comprehensive health score.

🤖 MODELS:
   • Diabetes Risk Model (Random Forest Classifier)
   • Heart Disease Risk Model (Random Forest Classifier)
   • Hypertension Risk Model (Random Forest Classifier)
   • Obesity Classification Model (Random Forest Classifier)

⚖️  SCORING METHODOLOGY:
   Individual risk scores are combined using weighted averages:
   - Heart Disease:  35% (most critical)
   - Diabetes:       25% (high impact)
   - Hypertension:   25% (significant risk)
   - Obesity:        15% (manageable)
   
   Health Score = 100 - Composite Risk Score

📊 OUTPUT:
   • Individual risk scores for each condition (0-100%)
   • Composite risk level (Low/Moderate/High/Critical)
   • Overall health score (0-100) with letter grade
   • Personalized health recommendations
   • Exportable health report

⚕️  MEDICAL DISCLAIMER:
   This tool is for informational and educational purposes only. It does not
   provide medical advice, diagnosis, or treatment. Always seek the advice of
   qualified health professionals for any medical conditions or concerns.

🔒 DATA PRIVACY:
   All data is processed locally. No information is stored or transmitted.

📅 Version: 1.0
👨‍💻 Built for: GDG HACK Project
""")
    print("="*80)


def main():
    """Main application entry point"""
    print_welcome()
    
    # Initialize pipeline (will load or train models)
    try:
        print("\n🔄 Initializing system...")
        pipeline = HealthAssessmentPipeline(train_models=False)
    except Exception as e:
        print(f"\n❌ Error initializing pipeline: {e}")
        print("Please ensure all dataset files are in the 'dataset' directory.")
        return
    
    # Main application loop
    while True:
        print_menu()
        
        try:
            choice = input("\n👉 Enter your choice (1-6): ").strip()
            
            if choice == '1':
                # Full health assessment
                print("\n📝 Starting Full Health Assessment...")
                ui = UserInterface()
                user_data = ui.collect_all()
                
                if user_data:
                    print("\n" + "="*80)
                    print("Processing your health assessment...")
                    print("="*80)
                    
                    report = pipeline.assess_and_report(user_data)
                    
                    # Ask to export report
                    export = input("\n💾 Would you like to export this report to a file? (yes/no): ").strip().lower()
                    if export in ['yes', 'y']:
                        filename = input("Enter filename (default: health_report.txt): ").strip()
                        if not filename:
                            filename = "health_report.txt"
                        pipeline.export_report_to_file(report, filename)
                        print(f"✅ Report saved to {filename}")
                
                input("\n Press Enter to continue...")
            
            elif choice == '2':
                # Quick health assessment
                print("\n⚡ Starting Quick Health Assessment...")
                ui = UserInterface()
                user_data = ui.quick_collect()
                
                if user_data:
                    report = pipeline.assess_and_report(user_data)
                    
                    export = input("\n💾 Export report to file? (yes/no): ").strip().lower()
                    if export in ['yes', 'y']:
                        filename = input("Filename (default: health_report.txt): ").strip() or "health_report.txt"
                        pipeline.export_report_to_file(report, filename)
                
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                # Use sample data
                print("\n📊 Using Sample Patient Data (52-year-old male with elevated risk factors)...")
                sample_data = get_sample_patient_data()
                
                print("\n Sample Patient Profile:")
                print(f"   Age: {sample_data['age']}, Gender: {sample_data['gender']}")
                print(f"   Height: {sample_data['height']} cm, Weight: {sample_data['weight']} kg")
                print(f"   BP: {sample_data['systolic_bp']}/{sample_data['diastolic_bp']} mm Hg")
                print(f"   Glucose: {sample_data['glucose']} mg/dL, Cholesterol: {sample_data['cholesterol']} mg/dL")
                
                proceed = input("\n Continue with assessment? (yes/no): ").strip().lower()
                if proceed in ['yes', 'y']:
                    report = pipeline.assess_and_report(sample_data)
                    
                    export = input("\n💾 Export report? (yes/no): ").strip().lower()
                    if export in ['yes', 'y']:
                        pipeline.export_report_to_file(report, "sample_patient_report.txt")
                
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                # Retrain models
                print("\n🔧 Retraining All Models...")
                confirm = input("⚠️  This will retrain all models from scratch. Continue? (yes/no): ").strip().lower()
                
                if confirm in ['yes', 'y']:
                    try:
                        pipeline = HealthAssessmentPipeline(train_models=True)
                        print("\n✅ All models retrained successfully!")
                    except Exception as e:
                        print(f"\n❌ Error during retraining: {e}")
                
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                # About
                print_about()
                input("\nPress Enter to continue...")
            
            elif choice == '6':
                # Exit
                print("\n" + "="*80)
                print("Thank you for using the Integrated Health Assessment System!")
                print("Stay healthy! 🏥💪")
                print("="*80 + "\n")
                break
            
            else:
                print("\n❌ Invalid choice. Please enter a number between 1 and 6.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user.")
            exit_confirm = input("Do you want to exit? (yes/no): ").strip().lower()
            if exit_confirm in ['yes', 'y']:
                print("\nGoodbye! 👋")
                break
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or contact support if the issue persists.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("The application will now exit.")
        sys.exit(1)
