import os
import re
import json
from PIL import Image
import pytesseract
import google.generativeai as genai
from typing import Dict, Optional

# Configure Tesseract path for Windows
# Common installation paths
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
]

for path in TESSERACT_PATHS:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

class NutritionAnalyzer:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize the nutrition analyzer with Gemini API"""
        # First try the provided key, then environment variable
        self.api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            print("⚠️  Warning: GEMINI_API_KEY not found. Nutrition analyzer may not work properly.")
            print("⚠️  Please set GEMINI_API_KEY in your .env file")
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Try different model names in order of preference
                model_names = [
                    'gemini-2.5-flash',
                    'gemini-1.5-pro',
                    'gemini-pro',
                    'models/gemini-1.5-flash',
                    'models/gemini-pro'
                ]
                
                self.model = None
                for model_name in model_names:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        print(f"✅ Gemini API initialized successfully with model: {model_name}")
                        break
                    except Exception as model_error:
                        continue
                
                if not self.model:
                    print(f"⚠️ Warning: Could not initialize any Gemini model")
                    
            except Exception as e:
                print(f"⚠️ Warning: Failed to initialize Gemini API: {e}")
                self.model = None
        else:
            print("⚠️ Warning: No Gemini API key provided. AI recommendations will be unavailable.")
            self.model = None
    
    def list_available_models(self):
        """List all available Gemini models"""
        try:
            models = genai.list_models()
            print("\n📋 Available Gemini Models:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"  - {model.name}")
            return [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from nutrition label image using OCR"""
        try:
            image = Image.open(image_path)
            # Preprocess image for better OCR
            image = image.convert('L')  # Convert to grayscale
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"❌ Error extracting text from image: {e}")
            return ""
    
    def parse_nutrition_data(self, text: str) -> Dict:
        """Parse extracted text to structured nutrition data"""
        nutrition_data = {
            "serving_size": None,
            "calories": None,
            "total_fat": None,
            "saturated_fat": None,
            "trans_fat": None,
            "cholesterol": None,
            "sodium": None,
            "total_carbohydrates": None,
            "dietary_fiber": None,
            "total_sugars": None,
            "added_sugars": None,
            "protein": None,
            "raw_text": text
        }
        
        # Patterns for extracting nutrition values
        patterns = {
            "calories": r'calories?\s*:?\s*(\d+)',
            "total_fat": r'total\s*fat\s*:?\s*(\d+\.?\d*)\s*g',
            "saturated_fat": r'saturated\s*fat\s*:?\s*(\d+\.?\d*)\s*g',
            "trans_fat": r'trans\s*fat\s*:?\s*(\d+\.?\d*)\s*g',
            "cholesterol": r'cholesterol\s*:?\s*(\d+\.?\d*)\s*mg',
            "sodium": r'sodium\s*:?\s*(\d+\.?\d*)\s*mg',
            "total_carbohydrates": r'total\s*carbohydrate\s*:?\s*(\d+\.?\d*)\s*g',
            "dietary_fiber": r'dietary\s*fiber\s*:?\s*(\d+\.?\d*)\s*g',
            "total_sugars": r'(?:total\s*)?sugars?\s*:?\s*(\d+\.?\d*)\s*g',
            "added_sugars": r'added\s*sugars?\s*:?\s*(\d+\.?\d*)\s*g',
            "protein": r'protein\s*:?\s*(\d+\.?\d*)\s*g',
            "serving_size": r'serving\s*size\s*:?\s*([\d.]+\s*\w+)'
        }
        
        text_lower = text.lower()
        for key, pattern in patterns.items():
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                try:
                    nutrition_data[key] = float(match.group(1)) if key != "serving_size" else match.group(1)
                except ValueError:
                    nutrition_data[key] = match.group(1)
        
        return nutrition_data
    
    def get_ai_recommendation(self, nutrition_data: Dict, health_assessment: Dict) -> Dict:
        """Get AI-powered recommendation using Gemini API"""
        if not self.model:
            return {
                "recommendation": "AI recommendations unavailable",
                "reason": "Gemini API key not configured",
                "safe_to_eat": None,
                "health_score": 0,
                "reasons": [],
                "concerns": [],
                "alternatives": "Please configure Gemini API key for AI recommendations"
            }
        
        try:
            # Prepare prompt for Gemini
            prompt = f"""
You are a health and nutrition expert. Analyze the following nutrition label data and user's health assessment to provide a recommendation.

**Nutrition Label Data:**
{json.dumps(nutrition_data, indent=2)}

**User's Health Assessment:**
- Overall Health Score: {health_assessment.get('overall_score', 'N/A')}/100
- Heart Disease Risk: {health_assessment.get('heart_risk', 'N/A')}%
- Diabetes Risk: {health_assessment.get('diabetes_risk', 'N/A')}%
- Hypertension Risk: {health_assessment.get('hypertension_risk', 'N/A')}%
- Obesity Risk: {health_assessment.get('obesity_risk', 'N/A')}%

Based on this information, provide:
1. A clear recommendation (Should eat / Should avoid / Can eat in moderation)
2. Specific reasons based on their health risks
3. Concerns about specific nutrients (sodium, sugar, saturated fat, etc.)
4. A health score for this product (0-100)

Format your response as JSON:
{{
    "recommendation": "Should eat / Should avoid / Can eat in moderation",
    "safe_to_eat": true/false,
    "health_score": 0-100,
    "reasons": ["reason 1", "reason 2", ...],
    "concerns": ["concern 1", "concern 2", ...],
    "alternatives": "Brief suggestion for healthier alternatives"
}}
"""
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                # Remove first line (```json or ```) and last line (```)
                response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text
            
            recommendation = json.loads(response_text)
            return recommendation
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing AI response as JSON: {e}")
            print(f"Raw response: {response_text}")
            return {
                "recommendation": "Error analyzing product",
                "reason": f"Failed to parse AI response: {str(e)}",
                "safe_to_eat": None,
                "health_score": 0,
                "reasons": [],
                "concerns": [],
                "alternatives": "Unable to analyze at this time"
            }
        except Exception as e:
            print(f"❌ Error getting AI recommendation: {e}")
            return {
                "recommendation": "Error analyzing product",
                "reason": str(e),
                "safe_to_eat": None,
                "health_score": 0,
                "reasons": [],
                "concerns": [],
                "alternatives": "Unable to analyze at this time"
            }
    
    def analyze_nutrition_label(self, image_path: str, health_assessment: Dict) -> Dict:
        """Complete analysis pipeline: OCR -> Parse -> AI Recommendation"""
        print("📸 Extracting text from nutrition label...")
        text = self.extract_text_from_image(image_path)
        
        if not text:
            return {
                "success": False,
                "error": "Could not extract text from image"
            }
        
        print("📊 Parsing nutrition data...")
        nutrition_data = self.parse_nutrition_data(text)
        
        print("🤖 Getting AI recommendation...")
        recommendation = self.get_ai_recommendation(nutrition_data, health_assessment)
        
        return {
            "success": True,
            "nutrition_data": nutrition_data,
            "recommendation": recommendation
        }

