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

@app.route('/api/generate-health-plan', methods=['POST'])
def generate_health_plan():
    """
    API endpoint for generating personalized 7-day health plan using Gemini AI
    """
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in your .env file.'
            }), 500
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Get request data
        data = request.get_json()
        user_data = data.get('userData', {})
        health_scores = data.get('healthScores', {})
        
        # Extract key information
        age = user_data.get('age', 'N/A')
        gender = user_data.get('gender', 'N/A')
        weight = user_data.get('weight', 'N/A')
        height = user_data.get('height', 'N/A')
        
        # Calculate BMI if available
        bmi = 'N/A'
        if weight != 'N/A' and height != 'N/A':
            try:
                bmi = round(float(weight) / ((float(height)/100) ** 2), 1)
            except:
                bmi = 'N/A'
        
        # Get blood pressure
        systolic = user_data.get('systolic_bp', 'N/A')
        diastolic = user_data.get('diastolic_bp', 'N/A')
        bp = f"{systolic}/{diastolic}" if systolic != 'N/A' and diastolic != 'N/A' else 'N/A'
        
        # Get other health metrics
        glucose = user_data.get('glucose', 'N/A')
        cholesterol = user_data.get('cholesterol', 'N/A')
        
        # Get lifestyle factors
        smoking = user_data.get('smokes', 'N/A')
        alcohol = user_data.get('alcohol_consumption', 'N/A')
        activity = user_data.get('physical_activity_frequency', 'N/A')
        
        # Get risk scores
        diabetes_risk = health_scores.get('diabetes_risk', 0)
        heart_risk = health_scores.get('heart_risk', 0)
        hypertension_risk = health_scores.get('hypertension_risk', 0)
        obesity_risk = health_scores.get('obesity_risk', 0)
        overall_score = health_scores.get('health_score', 0)
        
        # Build optimized prompt (token-efficient)
        prompt = f"""Create 7-day health plan for:
Age {age}, {gender}, BMI {bmi}, BP {bp}, Glucose {glucose}, Chol {cholesterol}
Smoking: {smoking}, Alcohol: {alcohol}, Activity: {activity}
Risks: DM {diabetes_risk:.0f}%, Heart {heart_risk:.0f}%, HTN {hypertension_risk:.0f}%, Obesity {obesity_risk:.0f}%
Overall Score: {overall_score:.0f}/100

Format: Day 1-7, each with:
- Morning/Afternoon/Evening actions
- Diet tips (specific foods)
- Exercise (10-15min, realistic)
- One measurable goal

Make it actionable, personalized, encouraging. Focus on highest risks."""
        
        # Try multiple Gemini models with fallback
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro",
            "models/gemini-1.5-flash",
            "models/gemini-pro"
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                print(f"🤖 Trying Gemini model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    print(f"✅ Successfully generated health plan using {model_name}")
                    return jsonify({
                        'success': True,
                        'plan': response.text,
                        'model_used': model_name
                    })
                else:
                    raise ValueError("Empty response from AI")
                    
            except Exception as e:
                last_error = str(e)
                print(f"⚠️  {model_name} failed: {e}")
                continue
        
        # All models failed
        return jsonify({
            'success': False,
            'error': f'Unable to generate health plan. All AI models failed. Last error: {last_error}'
        }), 500
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Google Generative AI library not installed. Run: pip install google-generativeai'
        }), 500
        
    except Exception as e:
        print(f"❌ Error generating health plan: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Failed to generate health plan: {str(e)}'
        }), 500

@app.route('/api/download-health-plan-pdf', methods=['POST'])
def download_health_plan_pdf():
    """
    API endpoint for downloading health plan as formatted PDF
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
        from reportlab.lib.colors import HexColor, black, white
        from reportlab.graphics.shapes import Drawing, Line
        from io import BytesIO
        from flask import send_file
        import re
        
        # Get plan text from request
        data = request.get_json()
        plan_text = data.get('planText', '')
        user_name = data.get('userName', 'User')
        
        if not plan_text:
            return jsonify({
                'success': False,
                'error': 'No health plan text provided'
            }), 400
        
        # Get user assessment data from session - with defaults
        assessment_results = session.get('assessment_results', {})
        user_data = assessment_results.get('user_data', {})
        health_scores = assessment_results.get('scores', {})
        
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=0.5*inch,
            bottomMargin=0.6*inch
        )
        
        # Define professional hospital-style colors
        HEADER_BG = HexColor('#003d5b')      # Dark medical blue
        ACCENT_BLUE = HexColor('#0066cc')    # Professional blue
        SECTION_BG = HexColor('#f0f4f8')     # Light gray-blue
        TEXT_PRIMARY = HexColor('#1a1a1a')   # Almost black
        TEXT_SECONDARY = HexColor('#4a5568') # Gray
        BORDER_COLOR = HexColor('#cbd5e0')   # Light border
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Hospital Header Style
        hospital_header_style = ParagraphStyle(
            'HospitalHeader',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=HEADER_BG,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=26
        )
        
        # Document Title Style
        doc_title_style = ParagraphStyle(
            'DocumentTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=white,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            backColor=HEADER_BG,
            borderPadding=12,
            leading=20
        )
        
        # Section Header Style (Medical Report Style)
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading1'],
            fontSize=13,
            textColor=white,
            spaceAfter=12,
            spaceBefore=16,
            fontName='Helvetica-Bold',
            backColor=ACCENT_BLUE,
            borderPadding=(8, 8, 8, 12),
            leftIndent=0,
            leading=16
        )
        
        # Subsection Style
        subsection_style = ParagraphStyle(
            'Subsection',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=ACCENT_BLUE,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=(0, 0, 6, 0),
            borderColor=ACCENT_BLUE,
            leftIndent=0
        )
        
        # Sub-subsection Style
        subsubsection_style = ParagraphStyle(
            'SubSubsection',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=TEXT_PRIMARY,
            spaceAfter=6,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            leftIndent=10
        )
        
        # Body text style
        body_style = ParagraphStyle(
            'MedicalBody',
            parent=styles['BodyText'],
            fontSize=10,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            textColor=TEXT_PRIMARY,
            fontName='Helvetica'
        )
        
        # Bullet style
        bullet_style = ParagraphStyle(
            'MedicalBullet',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14,
            leftIndent=25,
            spaceAfter=5,
            textColor=TEXT_PRIMARY,
            bulletIndent=15,
            fontName='Helvetica'
        )
        
        # Info box style
        info_style = ParagraphStyle(
            'InfoBox',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=TEXT_SECONDARY,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leftIndent=5,
            rightIndent=5
        )
        
        # Build PDF content
        story = []
        
        # ===== HOSPITAL HEADER SECTION =====
        story.append(Paragraph("HEALTH ASSESSMENT CENTER", hospital_header_style))
        story.append(Paragraph(
            "<font size=9 color='#4a5568'>AI-Powered Personalized Health Management System</font>",
            ParagraphStyle('Tagline', parent=styles['Normal'], alignment=TA_CENTER, spaceAfter=8)
        ))
        
        # Horizontal line
        line_drawing = Drawing(7*inch, 10)
        line_drawing.add(Line(0, 5, 7*inch, 5, strokeColor=HEADER_BG, strokeWidth=2))
        story.append(line_drawing)
        story.append(Spacer(1, 0.12*inch))
        
        # Document Title Box
        story.append(Paragraph("PERSONALIZED HEALTH PLAN REPORT", doc_title_style))
        story.append(Spacer(1, 0.15*inch))
        
        # ===== PATIENT INFORMATION TABLE =====
        from datetime import datetime
        current_date = datetime.now()
        
        patient_data = [
            ['Patient Information', '', '', ''],
            ['Name:', user_name, 'Report Date:', current_date.strftime('%B %d, %Y')],
            ['Age:', f"{user_data.get('age', 'N/A')} years", 'Report ID:', f"HP-{current_date.strftime('%Y%m%d-%H%M')}"],
            ['Gender:', user_data.get('gender', 'N/A').title(), 'Generated:', current_date.strftime('%I:%M %p')]
        ]
        
        patient_table = Table(patient_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        patient_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), SECTION_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_BG),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_PRIMARY),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ===== HEALTH SCORES SUMMARY TABLE =====
        if health_scores:
            story.append(Paragraph("HEALTH ASSESSMENT SUMMARY", section_header_style))
            
            scores_data = [['Health Category', 'Score', 'Status']]
            
            for category, score in health_scores.items():
                if isinstance(score, (int, float)):
                    score_val = round(score, 1)
                    if score_val >= 80:
                        status = 'Excellent'
                        status_color = HexColor('#10b981')
                    elif score_val >= 60:
                        status = 'Good'
                        status_color = HexColor('#3b82f6')
                    elif score_val >= 40:
                        status = 'Fair'
                        status_color = HexColor('#f59e0b')
                    else:
                        status = 'Needs Attention'
                        status_color = HexColor('#ef4444')
                    
                    scores_data.append([
                        category.replace('_', ' ').title(),
                        f"{score_val}%",
                        status
                    ])
            
            if len(scores_data) > 1:
                scores_table = Table(scores_data, colWidths=[3*inch, 1.5*inch, 2.5*inch])
                scores_table.setStyle(TableStyle([
                    # Header
                    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_BLUE),
                    ('TEXTCOLOR', (0, 0), (-1, 0), white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    
                    # Data
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
                    ('FONTNAME', (1, 1), (-1, -1), 'Helvetica-Bold'),
                    ('ALIGN', (1, 1), (2, -1), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                    
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, SECTION_BG]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                
                story.append(scores_table)
                story.append(Spacer(1, 0.25*inch))
        
        # ===== HEALTH PLAN CONTENT =====
        story.append(Paragraph("DETAILED HEALTH PLAN", section_header_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Process the markdown text
        lines = plan_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.08*inch))
                continue
            
            # Main heading (# )
            if line.startswith('# ') and not line.startswith('## '):
                text = line.replace('# ', '').strip()
                story.append(Spacer(1, 0.12*inch))
                story.append(Paragraph(text.upper(), section_header_style))
                
            # Subheading (## )
            elif line.startswith('## ') and not line.startswith('### '):
                text = line.replace('## ', '').strip()
                story.append(Paragraph(text, subsection_style))
                
            # Sub-subheading (### )
            elif line.startswith('### '):
                text = line.replace('### ', '').strip()
                story.append(Paragraph(f"▸ {text}", subsubsection_style))
                
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                text = line.replace('- ', '').replace('* ', '').strip()
                # Convert markdown bold to HTML
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                story.append(Paragraph(f"• {text}", bullet_style))
                
            # Regular text
            else:
                # Convert markdown bold to HTML
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                story.append(Paragraph(text, body_style))
        
        # ===== FOOTER SECTION =====
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer box
        disclaimer_data = [[
            Paragraph(
                "<b>⚠️ MEDICAL DISCLAIMER</b><br/>"
                "This health plan is generated by an AI-powered system for informational and educational purposes only. "
                "It is not intended to replace professional medical advice, diagnosis, or treatment. "
                "Always seek the advice of your physician or other qualified health provider with any questions you may have "
                "regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of "
                "information provided in this report.",
                ParagraphStyle(
                    'DisclaimerText',
                    parent=styles['Normal'],
                    fontSize=7,
                    leading=10,
                    textColor=TEXT_SECONDARY,
                    alignment=TA_JUSTIFY
                )
            )
        ]]
        
        disclaimer_table = Table(disclaimer_data, colWidths=[7*inch])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#fff3cd')),
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#ffc107')),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(disclaimer_table)
        
        # Report footer
        story.append(Spacer(1, 0.15*inch))
        footer_line = Drawing(7*inch, 10)
        footer_line.add(Line(0, 5, 7*inch, 5, strokeColor=BORDER_COLOR, strokeWidth=1))
        story.append(footer_line)
        story.append(Spacer(1, 0.08*inch))
        story.append(Paragraph(
            f"<font size=7 color='#718096'>Report Generated: {current_date.strftime('%B %d, %Y at %I:%M %p')} | "
            f"Health Assessment Center © {current_date.year} | Confidential Medical Document</font>",
            ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=7, textColor=TEXT_SECONDARY)
        ))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        buffer.seek(0)
        
        # Send file
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Health_Plan_Report_{current_date.strftime("%Y%m%d_%H%M")}.pdf'
        )
        
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'ReportLab library not installed. Run: pip install reportlab'
        }), 500
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Failed to generate PDF: {str(e)}'
        }), 500

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

@app.route('/login')
def login():    
    """Login page"""
    return render_template('login.html')

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