from flask import Flask, request, send_file, jsonify
import PyPDF2
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "PDF Extraction Service is running!"

@app.route('/extract', methods=['POST'])
def extract_pages():
    try:
        data = request.json
        pdf_url = data['url']
        start_page = int(data['start_page'])
        end_page = int(data['end_page'])
        
        response = requests.get(pdf_url, timeout=60)
        pdf_file = BytesIO(response.content)
        
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        for page_num in range(start_page - 1, end_page):
            if page_num < len(pdf_reader.pages):
                pdf_writer.add_page(pdf_reader.pages[page_num])
        
        output = BytesIO()
        pdf_writer.write(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='extracted.pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
