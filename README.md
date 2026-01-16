# 🏥 Integrated Health Assessment System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-Powered Comprehensive Health Risk Analysis Platform with WhatsApp Integration**

An intelligent health assessment system that integrates **4 machine learning models** to evaluate multiple health risks and provide a comprehensive health score with personalized recommendations. Features include web interface, WhatsApp integration, and nutrition label scanning using OCR and AI.

---

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [API Endpoints](#-api-endpoints)
- [WhatsApp Integration](#-whatsapp-integration)
- [Testing](#-testing)
- [Configuration](#-configuration)
- [Medical Disclaimer](#-medical-disclaimer)
- [Contributing](#-contributing)

---

## 🌟 Features

### ✅ Multi-Model Health Assessment
- **Diabetes Risk Prediction** - Analyzes glucose levels, BMI, family history
- **Heart Disease Risk Prediction** - Evaluates cardiovascular health markers
- **Hypertension Risk Prediction** - Assesses blood pressure and lifestyle factors
- **Obesity Classification** - Determines obesity level based on multiple parameters

### ✅ Intelligent Scoring System
- **Individual Risk Scores** for each condition (0-100%)
- **Weighted Composite Risk** (Heart: 35%, Diabetes: 25%, Hypertension: 25%, Obesity: 15%)
- **Overall Health Score** (0-100 with letter grades A+ to F)
- **Risk Level Classification** (Low, Moderate, High, Critical)

### ✅ Multiple Interfaces
- **Web Application** - Modern, responsive Flask-based UI
- **CLI Interface** - Interactive command-line interface
- **WhatsApp Bot** - Send messages and nutrition labels via WhatsApp
- **REST API** - Programmatic access to health assessments

### ✅ Nutrition Analysis
- **OCR-Powered Label Scanning** - Extract nutrition info from photos (Tesseract)
- **AI-Powered Analysis** - Gemini AI provides detailed health insights
- **Instant Recommendations** - Personalized advice based on nutrition content

### ✅ Additional Features
- **Exportable Reports** in text format
- **Detailed Risk Breakdown** for each condition
- **Actionable Health Recommendations**
- **Fully Offline Operation** (except WhatsApp/AI features)

---

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/mallurivikas/hitam_gdg_hack
cd gdg-hack

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```env
# Gemini AI API Key (Get from: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key

# Twilio Credentials (Get from: https://console.twilio.com/)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Flask Secret Key (Generate: python -c "import secrets; print(secrets.token_hex(32))")
FLASK_SECRET_KEY=your_secure_random_key
```

### 3. Install Tesseract OCR (for nutrition scanning)

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR`
- Add to PATH if needed

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 4. Run the Application

**Web Application:**
```bash
python app.py
# Open http://localhost:5000 in your browser
```

**CLI Interface:**
```bash
python main.py
```

---

## 📁 Project Structure

```
GDG HACK/
├── app.py                         # Flask web application
├── main.py                        # CLI application entry point
├── pipeline.py                    # Health assessment pipeline orchestrator
├── user_interface.py              # Interactive CLI data collection
├── feature_mapper.py              # Maps user inputs to model features
├── health_scorer.py               # Health scoring and reporting logic
├── whatsapp_handler.py            # WhatsApp message handling
├── whatsapp_routes.py             # WhatsApp webhook routes
├── nutrition_analyzer.py          # OCR and AI nutrition analysis
├── train_all_models.py            # Train all ML models
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (create this)
│
├── models/                        # ML models package
│   ├── __init__.py
│   ├── diabetes_model.py          # Diabetes prediction (8 features, ~76% accuracy)
│   ├── heart_model.py             # Heart disease prediction (13 features, ~85% accuracy)
│   ├── hypertension_model.py      # Hypertension prediction (22 features, ~95% accuracy)
│   └── obesity_model.py           # Obesity classification (16 features, ~96% accuracy)
│
├── dataset/                       # Training datasets
│   ├── diabetes.csv
│   ├── heart.csv
│   ├── hypertension_dataset.csv
│   └── obesity.csv
│
├── saved_models/                  # Trained model files (auto-generated)
│   ├── diabetes_model.pkl
│   ├── heart_model.pkl
│   ├── hypertension_model.pkl
│   └── obesity_model.pkl
│
├── templates/                     # HTML templates
│   ├── index.html
│   ├── assessment.html
│   ├── results.html
│   ├── nutrition-scanner.html
│   └── ...
│
├── static/                        # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
└── uploads/                       # Temporary file uploads
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Tesseract OCR (for nutrition scanning)

### Dependencies

```bash
pip install -r requirements.txt
```

**Key packages:**
- `flask` - Web framework
- `scikit-learn` - Machine learning models
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `google-generativeai` - Gemini AI integration
- `twilio` - WhatsApp integration
- `pytesseract` - OCR for nutrition labels
- `python-dotenv` - Environment variable management

### First-Time Setup

Train the models (takes 2-3 minutes):

```bash
python train_all_models.py
```

Or let them train automatically on first run.

---

## 💻 Usage

### Web Interface

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open http://localhost:5000
   - Navigate through the intuitive web interface

3. **Features available:**
   - Full Health Assessment
   - Quick Health Check
   - Nutrition Label Scanner
   - View Results and Recommendations

### CLI Interface

```bash
python main.py
```

**Menu Options:**
1. **Full Health Assessment** - Comprehensive evaluation (5-10 min)
2. **Quick Health Assessment** - Essential metrics only (2-3 min)
3. **Sample Patient Demo** - See system in action
4. **Retrain All Models** - Refresh ML models
5. **Exit**

### Programmatic Usage

```python
from pipeline import HealthAssessmentPipeline

# Initialize pipeline
pipeline = HealthAssessmentPipeline()

# User data
user_data = {
    'age': 45,
    'gender': 'Male',
    'height': 175,
    'weight': 85,
    'systolic_bp': 130,
    'diastolic_bp': 85,
    'glucose': 110,
    'cholesterol': 220
}

# Get assessment
report = pipeline.assess_and_report(user_data)

# Export report
pipeline.export_report_to_file(report, "health_report.txt")
```

---

## 🏗️ Architecture

### System Flow

```
User Input (Web/CLI/WhatsApp)
    ↓
Feature Mapper (normalize and map features)
    ↓
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Diabetes   │    Heart    │ Hypertension│   Obesity   │
│    Model    │    Model    │    Model    │    Model    │
│ (RF, 8 ft)  │ (RF, 13 ft) │ (RF, 22 ft) │ (RF, 16 ft) │
└─────────────┴─────────────┴─────────────┴─────────────┘
    ↓           ↓            ↓             ↓
Risk Score   Risk Score   Risk Score   Risk Score
   (0-100%)    (0-100%)    (0-100%)     (0-100%)
    ↓
Health Scorer (weighted combination)
    ↓
┌────────────────────────────────────────┐
│  Composite Risk & Health Score         │
│  + Risk Level Classification           │
│  + Personalized Recommendations        │
└────────────────────────────────────────┘
    ↓
Comprehensive Health Report
```

### Weighted Scoring Algorithm

```python
Composite Risk = (
    Heart Risk      × 35% +  # Most critical
    Diabetes Risk   × 25% +  # High impact
    Hypertension    × 25% +  # Significant risk
    Obesity Risk    × 15%    # Manageable
)

Health Score = 100 - Composite Risk
```

### Risk Classification

| Risk Score | Level      | Health Grade | Action Required |
|-----------|------------|--------------|-----------------|
| 0-30%     | Low        | A+, A        | Maintain habits |
| 30-50%    | Moderate   | B, C         | Lifestyle changes |
| 50-70%    | High       | D            | Medical consultation |
| 70-85%    | Very High  | F            | Urgent care needed |
| 85-100%   | Critical   | F            | Immediate medical attention |

---

## 🌐 API Endpoints

### Health Assessment

**POST** `/api/assess`
```json
{
  "age": 45,
  "gender": "Male",
  "height": 175,
  "weight": 85,
  "systolic_bp": 130,
  "diastolic_bp": 85,
  "glucose": 110,
  "cholesterol": 220
}
```

**Response:**
```json
{
  "health_score": 68.5,
  "grade": "C",
  "composite_risk": 31.5,
  "risk_level": "Moderate",
  "risks": {
    "diabetes": 35.2,
    "heart": 42.8,
    "hypertension": 28.1,
    "obesity": 22.5
  },
  "recommendations": [...]
}
```

### Nutrition Analysis

**POST** `/api/analyze-nutrition`
- Content-Type: `multipart/form-data`
- Field: `image` (nutrition label photo)

**Response:**
```json
{
  "extracted_text": "...",
  "analysis": "AI-powered nutrition analysis...",
  "recommendations": "..."
}
```

---

## 📱 WhatsApp Integration

### Setup

1. **Create Twilio Account:**
   - Visit https://www.twilio.com/try-twilio
   - Get WhatsApp Sandbox credentials

2. **Configure Webhook:**
   - For development, use ngrok:
     ```bash
     ngrok http 5000
     ```
   - Set webhook URL in Twilio Console:
     ```
     https://your-ngrok-url.ngrok-free.app/whatsapp/webhook
     ```

3. **Update .env file:**
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```

### Usage

**Text Commands:**
- `hi` or `hello` - Welcome message
- `scan` - Instructions for scanning nutrition labels
- `assess` - Link to health assessment
- `help` - Show all commands

**Photo Messages:**
- Send nutrition label photo → Receive instant AI analysis

### Testing

1. Join Twilio sandbox (send join code to sandbox number)
2. Send "hi" to test connection
3. Send a photo of a nutrition label to test scanning

---

## 🧪 Testing

### Quick Test (30 seconds)

```bash
python main.py
# Choose option 3: Sample Patient Demo
```

### Full Test Suite

Create `test_pipeline.py`:

```python
from pipeline import HealthAssessmentPipeline

pipeline = HealthAssessmentPipeline()

# Test healthy individual
healthy_data = {
    'age': 30, 'gender': 'Female', 'height': 165, 'weight': 60,
    'systolic_bp': 115, 'diastolic_bp': 75, 'glucose': 90,
    'cholesterol': 170, 'smoking_status': 'Never',
    'physical_activity': 'High'
}

# Test at-risk individual
atrisk_data = {
    'age': 55, 'gender': 'Male', 'height': 175, 'weight': 95,
    'systolic_bp': 150, 'diastolic_bp': 95, 'glucose': 135,
    'cholesterol': 260, 'smoking_status': 'Current',
    'physical_activity': 'Low'
}

# Run tests
report1 = pipeline.assess_and_report(healthy_data)
report2 = pipeline.assess_and_report(atrisk_data)

print(f"Healthy: {report1['health_score']}/100 (Expected: 70-90+)")
print(f"At-risk: {report2['health_score']}/100 (Expected: 20-50)")
```

Run:
```bash
python test_pipeline.py
```

### Test Checklist

- [ ] Models train successfully
- [ ] Web application loads
- [ ] CLI interface works
- [ ] Health assessment completes
- [ ] Nutrition scanning works (with Tesseract)
- [ ] WhatsApp integration active
- [ ] Reports export correctly

---

## ⚙️ Configuration

### Environment Variables

**Required for full functionality:**

```env
# AI Features
GEMINI_API_KEY=your_key_here           # For nutrition analysis

# WhatsApp Integration
TWILIO_ACCOUNT_SID=ACxxxxx             # Twilio credentials
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Web Application
FLASK_SECRET_KEY=generate_secure_key   # For session management
```

**Generate Flask Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Model Weights

Edit `health_scorer.py` to customize risk weights:

```python
self.weights = {
    'heart': 0.35,        # Cardiovascular
    'diabetes': 0.25,     # Metabolic
    'hypertension': 0.25, # Blood pressure
    'obesity': 0.15       # Weight management
}
```

### Tesseract Path

If Tesseract is not in PATH, set in `nutrition_analyzer.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## 🎯 Input Requirements

### Essential (Quick Mode)
- Age, Gender, Height, Weight
- Blood Pressure (Systolic/Diastolic)
- Blood Glucose, Cholesterol

### Additional (Full Mode)
- Blood tests: Insulin, LDL, HDL, Triglycerides
- Vital signs: Heart rate, max heart rate
- Lifestyle: Smoking, alcohol, activity, sleep, stress
- Diet: Meal frequency, water intake, vegetable consumption
- Medical history: Family history, previous conditions

### Sample Values

**Healthy Range:**
- BMI: 18.5-24.9
- Blood Pressure: 120/80 mm Hg
- Glucose: 70-100 mg/dL (fasting)
- Total Cholesterol: 125-200 mg/dL
- HDL: 40-60 mg/dL
- LDL: <100 mg/dL

---

## 📊 Model Performance

| Model          | Algorithm | Features | Accuracy |
|----------------|-----------|----------|----------|
| Diabetes       | Random Forest | 8      | ~76%     |
| Heart Disease  | Random Forest | 13     | ~85%     |
| Hypertension   | Random Forest | 22     | ~95%     |
| Obesity        | Random Forest | 16     | ~96%     |

*All models use Random Forest Classifiers with 100 trees*

---

## 🔧 Troubleshooting

### Models Not Found
**Solution:** Run `python train_all_models.py` or let them train automatically on first run.

### Tesseract Not Found
**Solution:** Install Tesseract and add to PATH, or set path manually in code.

### WhatsApp Not Working
**Solution:** 
1. Verify ngrok is running: `ngrok http 5000`
2. Check webhook URL in Twilio Console
3. Ensure Flask app is running
4. Verify credentials in `.env`

### Import Errors
**Solution:** `pip install -r requirements.txt`

### Port Already in Use
**Solution:** Change port in `app.py`: `app.run(port=5001)`

---

## ⚕️ Medical Disclaimer

**IMPORTANT:** This system is for **educational and informational purposes only**.

- ❌ NOT a substitute for professional medical advice
- ❌ NOT validated for clinical use
- ❌ Results should NOT be used for medical decisions

**Always consult qualified healthcare professionals** for:
- Medical diagnoses
- Treatment decisions
- Health concerns
- Interpretation of results

---

## 🛡️ Data Privacy & Security

- ✅ All health assessments processed **locally**
- ✅ **No data** transmitted or stored externally (except WhatsApp/AI features)
- ✅ **No database** - data exists only during session
- ✅ User data cleared after assessment
- ⚠️ WhatsApp messages handled by Twilio
- ⚠️ Nutrition analysis uses Gemini AI API

---

## 🔮 Future Enhancements

- [ ] User authentication and profiles
- [ ] Historical tracking and trends
- [ ] Data visualization dashboard
- [ ] PDF report generation
- [ ] Additional health models (mental health, sleep quality)
- [ ] Multi-language support
- [ ] Mobile app (React Native/Flutter)
- [ ] Integration with wearable devices

---

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Contact & Support

**GDG HACK Project**

For questions, issues, or contributions:
- Create an issue in the repository
- Contact: [Your Contact Information]

---

## 🙏 Acknowledgments

- **Datasets:** Public health datasets for model training
- **Built with:** Python, Flask, scikit-learn, pandas, numpy
- **APIs:** Google Gemini AI, Twilio WhatsApp API, Tesseract OCR
- **Inspired by:** Modern preventive healthcare initiatives

---

## 📈 Project Statistics

- **Total Lines of Code:** ~3,500+
- **Number of Files:** 15+ Python files
- **ML Models:** 4 trained models
- **API Endpoints:** 10+
- **Features:** 59+ input parameters
- **Supported Interfaces:** Web, CLI, WhatsApp

---
