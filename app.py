from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.json
    messages = data.get('messages', [])
    
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""تو یه تحلیلگر فوتبال حرفه‌ای هستی به اسم «فوتبال‌یار». 
فارسی صحبت می‌کنی و جواب‌هات کوتاه، دقیق و جذابه.
تخصصت روی جام جهانی ۲۰۲۶ و فوتبال جهانیه.
فقط درباره فوتبال صحبت می‌کنی.
جواب‌ها رو با ایموجی جذاب کن.""",
        messages=messages
    )
    
    return jsonify({'reply': response.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
