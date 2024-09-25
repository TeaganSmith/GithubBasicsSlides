from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure upload folder and allowed file types
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Mock function to simulate contract information extraction
def extract_contract_info(pdf_path):
    # In practice, you would parse the PDF and extract contract info
    return {
        "contract_id": 12345,
        "property_address": "123 Elm Street",
        "seller": "John Doe",
        "buyer": "Jane Smith",
        "price": 350000,
        "status": "Pending"
    }

# Mock function to simulate contract update with new offer values
def update_contract_info(contract_info, new_offer):
    contract_info['price'] = new_offer
    contract_info['status'] = "Offer Updated"
    return contract_info

# Endpoint to upload a PDF file and extract contract information
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract contract information from the PDF (mocked)
        contract_info = extract_contract_info(file_path)
        return jsonify({"message": "File uploaded and processed", "contract_info": contract_info}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400
