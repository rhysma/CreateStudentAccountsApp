from flask import Flask, request, render_template, jsonify
import csv
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, 'temp_uploaded_file.csv')
        file.save(filepath)
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                normalized_headers = [header.strip().lower() for header in headers]
                if normalized_headers != ['firstname', 'lastname', 'username', 'password']:
                    return 'Invalid CSV format. Please ensure the headers are firstname, lastname, username, password.'
                for row in reader:
                    create_user_account(row[2], row[3], row[0], row[1])  # username, password, firstname, lastname
        except Exception as e:
            return f'An error occurred: {e}'
        
        return 'File successfully uploaded and users created'
    else:
        return 'Invalid file type'

def create_user_account(username, password, firstname, lastname):
    command = [
        'powershell.exe',
        '-Command',
        'scripts\\createusers.ps1',
        '-username', username,
        '-password', password,
        '-firstname', firstname,
        '-lastname', lastname
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Error creating user {username}: {process.stderr}")
    return process.returncode == 0, process.stdout if process.returncode == 0 else process.stderr

if __name__ == '__main__':
    app.run(debug=True)
