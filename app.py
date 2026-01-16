"""
Flask Web Application for Health Assessment System
Provides web interface for the integrated health assessment pipeline
"""
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import json
import traceback
from datetime import datetime
from pipeline import HealthAssessmentPipeline
from user_interface import UserInterface
from nutrition_analyzer import NutritionAnalyzer
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from whatsapp_routes import whatsapp_bp, init_whatsapp_handler
import requests

# Load environment variables FIRST
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'health_assessment_secret_key_2024')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the pipeline and nutrition analyzer globally
try:
    pipeline = HealthAssessmentPipeline(train_models=False)
    nutrition_analyzer = NutritionAnalyzer()
    print("✅ Pipeline and Nutrition Analyzer initialized successfully!")
    
    # Initialize WhatsApp handler with nutrition analyzer
    init_whatsapp_handler(nutrition_analyzer)
    
except Exception as e:
    print(f"❌ Error initializing: {e}")
    pipeline = None
    nutrition_analyzer = None

# Register WhatsApp blueprint
app.register_blueprint(whatsapp_bp, url_prefix='/whatsapp')

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page with health assessment form"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with system information"""
    return render_template('about.html')

@app.route('/quick-assessment')
def quick_assessment():
    """Quick assessment form page"""
    return render_template('quick-check.html')

@app.route('/assessment')
def assessment():
    """Full assessment form page"""
    return render_template('assessment.html')

@app.route('/sample-demo')
def sample_demo():
    """Sample demo page"""
    return render_template('demo.html')

@app.route('/api/assess', methods=['POST'])
def api_assess():
    """API endpoint for health assessment"""
    try:
        if not pipeline:
            return jsonify({
                'success': False,
                'error': 'Health assessment system not available. Please ensure all models are properly loaded.'
            }), 500
        
        # Get form data
        form_data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Convert numeric fields
        numeric_fields = [
            'age', 'height', 'weight', 'systolic_bp', 'diastolic_bp', 'glucose', 
            'cholesterol', 'ldl', 'hdl', 'triglycerides', 'resting_heart_rate', 
            'max_heart_rate', 'sleep_hours', 'vegetable_consumption_frequency',
            'num_main_meals', 'daily_water_consumption', 'pregnancies', 'insulin',
            'chest_pain_type', 'physical_activity_frequency', 'tech_usage_time',
            'skin_thickness', 'st_depression', 'slope_st_segment', 'num_major_vessels',
            'thalassemia', 'resting_ecg'
        ]
        
        user_data = {}
        for key, value in form_data.items():
            if key in numeric_fields:
                try:
                    user_data[key] = float(value) if value else None
                except (ValueError, TypeError):
                    user_data[key] = None
            else:
                user_data[key] = value if value else None
        
        # Remove None values to let the system use defaults
        user_data = {k: v for k, v in user_data.items() if v is not None and v != ''}
        
        print(f"Processing assessment for user data: {list(user_data.keys())}")
        
        # Run assessment
        report = pipeline.assess_and_report(user_data)
        
        # Store results in session for results page
        session['assessment_results'] = {
            'report': report,
            'user_data': user_data,
            'timestamp': datetime.now().isoformat()
        }
        
        # NEW: Check if user wants to link WhatsApp profile
        whatsapp_number = user_data.get('whatsapp_number')
        if whatsapp_number:
            # Extract health summary for WhatsApp profile
            health_summary = {
                'age': user_data.get('age', 35),
                'has_diabetes': report.get('diabetes_risk', 0) > 50,
                'has_hypertension': report.get('hypertension_risk', 0) > 50,
                'has_heart_disease': report.get('heart_risk', 0) > 50,
                'bmi': 'overweight' if user_data.get('weight', 70) / ((user_data.get('height', 170)/100)**2) > 25 else 'normal'
            }
            
            # Update WhatsApp profile via API
            try:
                requests.post('http://localhost:5000/whatsapp/update-profile', json={
                    'phone_number': whatsapp_number,
                    'health_data': health_summary
                })
                print(f"✅ Updated WhatsApp profile for {whatsapp_number}")
            except Exception as e:
                print(f"⚠️  Could not update WhatsApp profile: {e}")
        
        print(f"✅ Assessment completed successfully")
        print(f"Report type: {type(report)}")
        print(f"Stored in session: {bool(session.get('assessment_results'))}")
        
        return jsonify({
            'success': True,
            'report': report,
            'redirect_url': '/results'
        })
        
    except Exception as e:
        print(f"❌ Error during assessment: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Assessment failed: {str(e)}'
        }), 500

@app.route('/api/sample-assessment')
def api_sample_assessment():
    """API endpoint for sample patient assessment"""
    try:
        if not pipeline:
            return jsonify({
                'success': False,
                'error': 'Health assessment system not available.'
            }), 500
        
        # Sample patient data (same as in main.py)
        sample_data = {
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
        
        report = pipeline.assess_and_report(sample_data)
        
        return jsonify({
            'success': True,
            'report': report,
            'sample_data': sample_data
        })
        
    except Exception as e:
        print(f"Error during sample assessment: {e}")
        return jsonify({
            'success': False,
            'error': f'Sample assessment failed: {str(e)}'
        }), 500

@app.route('/nutrition-scanner')
def nutrition_scanner():
    """Nutrition label scanner page"""
    return render_template('nutrition-scanner.html')

@app.route('/api/analyze-nutrition', methods=['POST'])
def api_analyze_nutrition():
    """API endpoint for nutrition label analysis"""
    try:
        if not nutrition_analyzer:
            return jsonify({
                'success': False,
                'error': 'Nutrition analyzer not available'
            }), 500
        
        # Check if file was uploaded
        if 'nutrition_image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['nutrition_image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload an image file.'
            }), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get user's health assessment from session
        health_data = session.get('assessment_results', {})
        if not health_data or 'report' not in health_data:
            # Use default values if no assessment available
            health_assessment = {
                'overall_score': 50,
                'heart_risk': 25,
                'diabetes_risk': 25,
                'hypertension_risk': 25,
                'obesity_risk': 25
            }
        else:
            # Extract risk data from report
            report = health_data.get('report', {})
            individual_risks = report.get('individual_risks', {})
            
            health_assessment = {
                'overall_score': report.get('health_score', 50),
                'heart_risk': individual_risks.get('heart_disease', {}).get('score', 25),
                'diabetes_risk': individual_risks.get('diabetes', {}).get('score', 25),
                'hypertension_risk': individual_risks.get('hypertension', {}).get('score', 25),
                'obesity_risk': individual_risks.get('obesity', {}).get('score', 25)
            }
        
        print(f"🔍 Using health assessment: {health_assessment}")
        
        # Analyze nutrition label
        result = nutrition_analyzer.analyze_nutrition_label(filepath, health_assessment)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error analyzing nutrition label: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/results')
def results():
    """Results page - displays after assessment"""
    # Get assessment results from session
    assessment_results = session.get('assessment_results')
    
    print(f"Results page accessed - Has data: {bool(assessment_results)}")
    
    if not assessment_results or 'report' not in assessment_results:
        print("❌ No assessment data found in session")
        return render_template('results.html', has_results=False)
    
    # Extract the report from the session data
    report = assessment_results['report']
    print(f"✅ Rendering results with data: health_score={report.get('health_score', 'N/A')}")
    
    return render_template('results.html', 
                         has_results=True, 
                         assessment_data=report)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("🌐 Starting Health Assessment Web Application...")
    print("📱 Open your browser and navigate to: http://localhost:5000")
    print("⚕️  Remember: This is for educational purposes only!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)