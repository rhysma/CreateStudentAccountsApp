from flask import Flask, request, render_template

app = Flask(__name__)

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
        # Here you would typically process the file or save it for processing
        file.save('uploaded_file.csv')
        return 'File successfully uploaded'
    else:
        return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)
