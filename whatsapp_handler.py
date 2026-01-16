from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from PIL import Image
from io import BytesIO
import json
from datetime import datetime
import google.generativeai as genai
import threading

class WhatsAppHandler:
    def __init__(self, nutrition_analyzer=None):
        # Load Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        # Store nutrition analyzer reference
        self.nutrition_analyzer = nutrition_analyzer
        
        # Initialize Twilio client
        try:
            self.client = Client(self.account_sid, self.auth_token)
            print("✅ WhatsApp Handler initialized with Twilio client")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Twilio client: {e}")
            self.client = None
        
        # Initialize Gemini API with model fallback
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
            else:
                print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
                # Fallback for development only
                genai.configure(api_key='AIzaSyCWQSac27hLEb4FjvROmkCWYCLwUH55oKQ')
            
            # Try different model names
            model_names = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            self.gemini_model = None
            
            for model_name in model_names:
                try:
                    self.gemini_model = genai.GenerativeModel(model_name)
                    print(f"✅ Gemini API initialized with model: {model_name}")
                    break
                except Exception as e:
                    continue
            
            if not self.gemini_model:
                print(f"⚠️  Warning: Could not initialize any Gemini model")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Gemini: {e}")
            self.gemini_model = None
        
        # Store user health profiles (in production, use database)
        self.user_health_profiles = {}
    
    def handle_incoming_message(self, from_number, message_body, media_url=None):
        """Handle incoming WhatsApp messages - Returns immediate response"""
        resp = MessagingResponse()
        msg = resp.message()
        
        # Check if it's an image
        if media_url:
            # Send immediate acknowledgment
            msg.body("⏳ Analyzing your nutrition label...\n\nThis may take 10-30 seconds. Please wait! 🤖")
            
            # Process image in background thread
            thread = threading.Thread(
                target=self.process_image_async,
                args=(from_number, media_url)
            )
            thread.daemon = True
            thread.start()
            print(f"🚀 Started background processing for {from_number}")
        else:
            # Handle text commands
            command = message_body.strip().lower()
            
            if command in ['hi', 'hello', 'start', 'help']:
                msg.body(self.get_welcome_message())
            elif command == 'scan':
                msg.body("📸 Please send a photo of the nutrition label you want to analyze.")
            elif command == 'assess':
                msg.body(self.get_assessment_instructions())
            elif command == 'profile':
                profile_info = self.show_user_profile(from_number)
                msg.body(profile_info)
            else:
                msg.body(self.get_help_message())
        
        return str(resp)
    
    def process_image_async(self, from_number, media_url):
        """Process image in background and send result via Twilio API"""
        try:
            print(f"📸 Background processing started for {from_number}")
            
            # Get user's health profile
            user_health_data = self.get_user_health_profile(from_number)
            
            # Process the image with health data
            result = self.process_nutrition_image(media_url, user_health_data)
            response_text = self.format_nutrition_results(result, user_health_data)
            
            # Send result via Twilio API (not TwiML)
            self.send_message_direct(from_number, response_text)
            print(f"✅ Analysis result sent to {from_number}")
            
        except Exception as e:
            print(f"❌ Error in background processing: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Send error message
            error_msg = "❌ Sorry, I couldn't analyze that image.\n\nPlease send a clear photo of a nutrition label and try again."
            try:
                self.send_message_direct(from_number, error_msg)
            except:
                print("❌ Could not send error message to user")
    
    def send_message_direct(self, to_number, message_body, media_url=None):
        """Send a WhatsApp message directly via Twilio API"""
        if not self.client:
            raise Exception("Twilio client not initialized. Check credentials.")
        
        try:
            print(f"📤 Sending message to {to_number}")
            if media_url:
                message = self.client.messages.create(
                    from_=self.whatsapp_number,
                    body=message_body,
                    media_url=[media_url],
                    to=to_number
                )
            else:
                message = self.client.messages.create(
                    from_=self.whatsapp_number,
                    body=message_body,
                    to=to_number
                )
            print(f"✅ Message sent: {message.sid}")
            return message.sid
        except Exception as e:
            print(f"❌ Failed to send message: {str(e)}")
            raise Exception(f"Failed to send message: {str(e)}")
    
    def get_user_health_profile(self, phone_number):
        """Get stored health profile for user"""
        if phone_number in self.user_health_profiles:
            profile = self.user_health_profiles[phone_number]
            # Check if profile is recent (within 30 days)
            age_days = (datetime.now() - profile['timestamp']).days
            if age_days <= 30:
                print(f"✅ Using stored health profile for {phone_number} (age: {age_days} days)")
                return profile['health_data']
            else:
                print(f"⚠️  Health profile expired for {phone_number}")
        
        # Return default profile if none exists
        print(f"ℹ️  Using default health profile for {phone_number}")
        return {
            'age': 35,
            'has_diabetes': False,
            'has_hypertension': False,
            'has_heart_disease': False,
            'bmi': 'normal'
        }
    
    def update_user_health_profile(self, phone_number, health_data):
        """Update stored health profile for user"""
        self.user_health_profiles[phone_number] = {
            'timestamp': datetime.now(),
            'health_data': health_data
        }
        print(f"✅ Updated health profile for {phone_number}")
    
    def show_user_profile(self, phone_number):
        """Show user their stored health profile"""
        if phone_number not in self.user_health_profiles:
            return """ℹ️ *No Health Profile Found*

You haven't completed a health assessment yet.

📋 Complete your assessment at:
https://c6cdafb92796.ngrok-free.app

This will personalize your nutrition recommendations!"""
        
        profile = self.user_health_profiles[phone_number]
        data = profile['health_data']
        age = (datetime.now() - profile['timestamp']).days
        
        response = f"""👤 *Your Health Profile*

📅 Last Updated: {age} days ago

📊 Profile Data:
• Age: {data.get('age', 'N/A')}
• BMI Status: {data.get('bmi', 'N/A')}
• Diabetes: {'Yes' if data.get('has_diabetes') else 'No'}
• Hypertension: {'Yes' if data.get('has_hypertension') else 'No'}
• Heart Disease: {'Yes' if data.get('has_heart_disease') else 'No'}

Update your profile anytime at:
https://c6cdafb92796.ngrok-free.app"""
        
        return response
    
    def process_nutrition_image(self, media_url, user_health_data=None):
        """Download and process nutrition label image"""
        try:
            # Download image
            print(f"📥 Downloading image from: {media_url}")
            response = requests.get(media_url, auth=(self.account_sid, self.auth_token))
            image = Image.open(BytesIO(response.content))
            
            # Save temporarily
            temp_path = f'temp_nutrition_{datetime.now().timestamp()}.jpg'
            image.save(temp_path)
            print(f"💾 Saved temp image: {temp_path}")
            
            # Use nutrition analyzer to extract nutrition data
            if self.nutrition_analyzer:
                print("🔍 Extracting nutrition data with OCR...")
                default_health = {'overall_score': 50, 'heart_risk': 25, 'diabetes_risk': 25, 'hypertension_risk': 25, 'obesity_risk': 25}
                full_result = self.nutrition_analyzer.analyze_nutrition_label(temp_path, default_health)
                nutrition_data = full_result.get('nutrition_data', {})
                print(f"✅ OCR extraction complete")
            else:
                print("⚠️  No nutrition analyzer available")
                nutrition_data = {}
            
            # Generate concise recommendation using Gemini
            if self.gemini_model and nutrition_data:
                print("🤖 Generating concise recommendation with Gemini...")
                result = self.generate_gemini_recommendation(nutrition_data, user_health_data)
            else:
                result = {'success': False, 'error': 'Could not analyze nutrition label'}
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print("🗑️  Cleaned up temp file")
            
            return result
            
        except Exception as e:
            print(f"❌ Error in process_nutrition_image: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Clean up on error
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            
            raise e
    
    def generate_gemini_recommendation(self, nutrition_data, user_health_data):
        """Use Gemini to generate concise, personalized recommendation"""
        try:
            # Build context for Gemini
            health_context = f"""
User Health Profile:
- Age: {user_health_data.get('age', 'Unknown')}
- Diabetes: {'Yes' if user_health_data.get('has_diabetes') else 'No'}
- Hypertension: {'Yes' if user_health_data.get('has_hypertension') else 'No'}
- Heart Disease: {'Yes' if user_health_data.get('has_heart_disease') else 'No'}
- BMI Status: {user_health_data.get('bmi', 'Normal')}

Nutrition Label Data:
- Calories: {nutrition_data.get('calories', 'N/A')} kcal
- Total Fat: {nutrition_data.get('total_fat', 'N/A')}g
- Saturated Fat: {nutrition_data.get('saturated_fat', 'N/A')}g
- Cholesterol: {nutrition_data.get('cholesterol', 'N/A')}mg
- Sodium: {nutrition_data.get('sodium', 'N/A')}mg
- Total Carbs: {nutrition_data.get('total_carbohydrates', 'N/A')}g
- Sugars: {nutrition_data.get('total_sugars', 'N/A')}g
- Protein: {nutrition_data.get('protein', 'N/A')}g
"""

            prompt = f"""{health_context}

Based on the user's health profile and the nutrition label data above, provide a VERY SHORT WhatsApp message (max 3-4 lines) with:

1. Clear recommendation: ✅ SAFE TO EAT / ⚠️ EAT OCCASIONALLY / ❌ AVOID
2. ONE key reason why (specific to their health)
3. Keep it conversational and under 200 characters total

Format example:
"✅ SAFE TO EAT
Good protein source. Watch sodium if you have hypertension."

OR

"❌ AVOID
High sugar (25g) - risky for diabetes. Choose sugar-free alternatives."

Be specific, actionable, and brief. No long explanations."""

            response = self.gemini_model.generate_content(prompt)
            recommendation_text = response.text.strip()
            
            print(f"✅ Gemini recommendation generated: {len(recommendation_text)} chars")
            
            return {
                'success': True,
                'recommendation': recommendation_text,
                'nutrition_data': nutrition_data
            }
            
        except Exception as e:
            print(f"❌ Error generating Gemini recommendation: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def format_nutrition_results(self, result, user_health_data):
        """Format nutrition analysis results for WhatsApp - VERY CONCISE"""
        if not result.get('success'):
            return "❌ Could not analyze the nutrition label. Please try again with a clearer image."
        
        # Get Gemini's concise recommendation
        recommendation = result.get('recommendation', 'Analysis complete.')
        
        # Add minimal nutrition facts
        nutrition = result.get('nutrition_data', {})
        nutrition_summary = []
        
        if nutrition.get('calories'):
            nutrition_summary.append(f"{nutrition['calories']}cal")
        if nutrition.get('sodium'):
            nutrition_summary.append(f"{nutrition['sodium']}mg sodium")
        if nutrition.get('total_sugars'):
            nutrition_summary.append(f"{nutrition['total_sugars']}g sugar")
        
        # Build ultra-concise response
        response = f"🔍 *ANALYSIS*\n\n{recommendation}"
        
        if nutrition_summary:
            response += f"\n\n📊 {' | '.join(nutrition_summary[:3])}"
        
        # Add footer
        response += "\n\n" + "─" * 25
        response += "\n📱 Full details: https://c6cdafb92796.ngrok-free.app/nutrition-scanner"
        response += "\n\nSend another photo or 'help'"
        
        return response
    
    def get_welcome_message(self):
        """Get welcome message"""
        return """👋 *Welcome to Health AI!*

I can help you analyze nutrition labels instantly!

*How to use:*
📸 Send me a photo of any food product's nutrition label
⚡ Get instant personalized recommendations

*Commands:*
• 'scan' - Instructions for scanning
• 'assess' - Start health assessment
• 'help' - Show this message

Send a photo to get started! 🚀"""
    
    def get_assessment_instructions(self):
        """Get health assessment instructions"""
        return """📋 *Health Assessment*

For a comprehensive health analysis, please visit our web app:

🌐 https://c6cdafb92796.ngrok-free.app

The assessment takes 5-10 minutes and provides:
• Heart disease risk
• Diabetes risk
• Hypertension risk
• Obesity risk
• Personalized recommendations

Or send a nutrition label photo for instant food analysis! 📸"""
    
    def get_help_message(self):
        """Get help message"""
        return """ℹ️ *Health AI Help*

*Commands:*
• 📸 Send photo - Analyze nutrition label
• 'profile' - View your health profile
• 'assess' - Complete health assessment
• 'help' - Show this message

*Tips:*
• Clear, well-lit photos work best
• Complete health assessment for personalized recommendations

What would you like to do? 🤔"""
    
    def send_message(self, to_number, message_body, media_url=None):
        """Alias for send_message_direct for backward compatibility"""
        return self.send_message_direct(to_number, message_body, media_url)