from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#open home page 
@app.route('/')
def home():
    return render_template('index.html')

#moving to about page
@app.route('/about')
def about():
    return render_template('about.html')

#moving to registration page 
@app.route('/reg')
def reg():
    return render_template('reg.html')

#moving to getStarted page
@app.route('/getStarted')
def getStarted():
    return render_template('getStarted.html')

#moving to doctors page
@app.route('/doctors')
def doc():
    return render_template('doc.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({
                "success": True,
                "message": f"File uploaded successfully: {filename}",
                "file_path": f"/static/uploads/{filename}"  # إضافة مسار الملف للرد
            })
        except Exception as e:
            return jsonify({"error": f"Error saving file: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/results')
def results():
    image_path = request.args.get('image')  # الحصول على مسار الصورة من الـ URL
    return render_template('results.html', image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
