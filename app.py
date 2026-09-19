from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)

# Google Sheets Setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open("Lead Capture Database").sheet1
    print("Google Sheets setup successfully!")
except Exception as e:
    print(f"Google Sheets Setup Error: {e}")
    sheet = None

@app.route('/submit', methods=['POST'])
def submit():
    if not sheet:
        return jsonify({"status": "error", "message": "Google Sheets not connected"}), 500

    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        # Append row to Google Sheet
        sheet.append_row([name, email, phone])
        return jsonify({"status": "success", "message": "Data saved successfully!"}), 200
    except Exception as e:
        print(f"Error saving to sheet: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
