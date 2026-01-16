from flask import Blueprint, request, jsonify
from whatsapp_handler import WhatsAppHandler
from functools import wraps

whatsapp_bp = Blueprint('whatsapp', __name__)

# Initialize handler without nutrition_analyzer first (will be set by app)
handler = WhatsAppHandler()

def init_whatsapp_handler(nutrition_analyzer):
    """Initialize WhatsApp handler with nutrition analyzer"""
    global handler
    handler.nutrition_analyzer = nutrition_analyzer
    print("✅ WhatsApp handler initialized with nutrition analyzer")

def validate_twilio_request(f):
    """Validate that request is from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # In production, validate Twilio signature
        # from twilio.request_validator import RequestValidator
        # validator = RequestValidator(auth_token)
        # if not validator.validate(request.url, request.form, request.headers.get('X-Twilio-Signature', '')):
        #     return 'Invalid request', 403
        return f(*args, **kwargs)
    return decorated_function

@whatsapp_bp.route('/webhook', methods=['POST'])
@validate_twilio_request
def whatsapp_webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get message details
        from_number = request.form.get('From')
        message_body = request.form.get('Body', '')
        media_url = request.form.get('MediaUrl0')  # First image attachment
        
        # Log ALL incoming data
        print(f"\n{'='*60}")
        print(f"📥 WEBHOOK RECEIVED")
        print(f"{'='*60}")
        print(f"From: {from_number}")
        print(f"Message: {message_body[:100] if message_body else '(no text)'}")
        print(f"Media URL: {media_url if media_url else '(no media)'}")
        print(f"All form data: {dict(request.form)}")
        print(f"{'='*60}\n")
        
        # Process message
        response = handler.handle_incoming_message(from_number, message_body, media_url)
        
        # Log the TwiML response being sent
        print(f"\n{'='*60}")
        print(f"📤 TWIML RESPONSE")
        print(f"{'='*60}")
        print(response)
        print(f"{'='*60}\n")
        
        return response, 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ WEBHOOK ERROR")
        print(f"{'='*60}")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        
        from twilio.twiml.messaging_response import MessagingResponse
        resp = MessagingResponse()
        resp.message("Sorry, something went wrong. Please try again.")
        return str(resp), 200, {'Content-Type': 'text/xml'}

@whatsapp_bp.route('/status', methods=['POST'])
def message_status():
    """Handle message status callbacks"""
    message_sid = request.form.get('MessageSid')
    message_status = request.form.get('MessageStatus')
    
    # Log status (in production, update database)
    print(f"Message {message_sid} status: {message_status}")
    
    return '', 200

@whatsapp_bp.route('/send', methods=['POST'])
def send_whatsapp_message():
    """API endpoint to send WhatsApp messages programmatically"""
    try:
        data = request.json
        to_number = data.get('to')
        message = data.get('message')
        media_url = data.get('media_url')
        
        if not to_number or not message:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Ensure number has whatsapp: prefix
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        message_sid = handler.send_message(to_number, message, media_url)
        
        return jsonify({
            'success': True,
            'message_sid': message_sid
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@whatsapp_bp.route('/test', methods=['GET'])
def test_whatsapp():
    """Test endpoint to verify WhatsApp integration"""
    client_status = "Connected ✅" if handler.client else "Not Connected ❌"
    
    return jsonify({
        'status': 'WhatsApp integration active',
        'twilio_client': client_status,
        'account_sid': handler.account_sid[:10] + '...' if handler.account_sid else 'Not set',
        'whatsapp_number': handler.whatsapp_number,
        'webhook_url': request.host_url + 'whatsapp/webhook',
        'instructions': {
            'setup': 'Configure this webhook URL in Twilio Console',
            'test': 'Send "hi" to your Twilio WhatsApp number',
            'scan': 'Send a photo of a nutrition label'
        }
    })

@whatsapp_bp.route('/update-profile', methods=['POST'])
def update_user_profile():
    """API endpoint to update user health profile from web assessment"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        health_data = data.get('health_data')
        
        if not phone_number or not health_data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Ensure number has whatsapp: prefix
        if not phone_number.startswith('whatsapp:'):
            phone_number = f'whatsapp:{phone_number}'
        
        # Update user's health profile
        handler.update_user_health_profile(phone_number, health_data)
        
        # Optionally send confirmation message
        confirmation_msg = f"""✅ *Health Profile Updated!*\n\nYour WhatsApp nutrition scanner now has your latest health data.\n\nSend a photo of any nutrition label to get personalized recommendations! 📸"""
        
        handler.send_message(phone_number, confirmation_msg)
        
        return jsonify({
            'success': True,
            'message': 'Health profile updated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
