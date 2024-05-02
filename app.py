import csv
import os
from flask import Flask, request, render_template

app = Flask(__name__)

# Specify the directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist

@app.route('/')
def index():
    return render_template('index.htm')

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
                # Normalize header case to lowercase and strip whitespace before comparison
                normalized_headers = [header.strip().lower() for header in headers]
                if normalized_headers != ['firstname', 'lastname', 'username', 'password']:
                    return 'Invalid CSV format. Please ensure the headers are firstname, lastname, username, password.'
        except UnicodeDecodeError:
            # Try a different encoding if UTF-8 failed
            try:
                with open(filepath, newline='', encoding='iso-8859-1') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)
                    normalized_headers = [header.strip().lower() for header in headers]
                    if normalized_headers != ['firstname', 'lastname', 'username', 'password']:
                        return 'Invalid CSV format. Please ensure the headers are firstname, lastname, username, password.'
            except Exception as e:
                return f'An error occurred with ISO-8859-1 encoding: {e}'
        except Exception as e:
            return f'An error occurred: {e}'
        
        return 'File successfully uploaded and validated'
    else:
        return 'Invalid file type'
if __name__ == '__main__':
    app.run(debug=True)
