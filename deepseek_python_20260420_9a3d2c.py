from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def translate_system(text, target_lang, source_lang='auto'):
    try:
        from urllib.parse import quote
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={quote(text)}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if target_lang == 'detect':
                return result[2]
            return ''.join(sentence[0] for sentence in result[0])
        return text
    except:
        return text

@app.route('/', methods=['GET', 'POST'])
def main():
    user_text = request.args.get('text') or request.form.get('text')
    if not user_text:
        return jsonify({"error": "Please provide 'text' parameter"})
    
    try:
        detected_lang = translate_system(user_text, 'detect')
        worm_url = "https://sii3.top/api/error/wormgpt.php"
        api_key = "DarkAI-WormGPT-9A775B691774FAD5F4E66700"
        
        response = requests.post(worm_url, data={'key': api_key, 'text': user_text}, timeout=30)
        worm_data = response.json()
        english_reply = worm_data.get('response', 'No response from API')
        
        final_reply = english_reply
        if detected_lang != 'en':
            final_reply = translate_system(english_reply, detected_lang, 'en')
        
        return jsonify({
            "reply": final_reply,
            "dev": "https://t.me/i_mmx",
            "ch": "https://t.me/ULTRA_CODE_1"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)