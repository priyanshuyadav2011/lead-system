from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from datetime import datetime

app = Flask(__name__)
CORS(app)

try:
    gc = gspread.service_account(filename='credentials.json')
    sheet = gc.open("Lead Capture Database").sheet1 
except Exception as e:
    print("Google Sheets Setup Error:", e)

@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Timestamp ke saath bhej rahe hain taaki har column match ho
        sheet.append_row([timestamp, name, email, phone])
        print(f"Data Added: {name}, {email}, {phone}")
        return jsonify({'status': 'success', 'message': 'Data added to Google Sheet!'})
    except Exception as e:
        print("Error saving to sheet:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)