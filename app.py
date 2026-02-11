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
        
        # Télécharge avec headers pour éviter les blocages
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(pdf_url, timeout=120, headers=headers, stream=True)
        response.raise_for_status()
        
        # Lit le PDF en mémoire
        pdf_content = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        pdf_writer = PyPDF2.PdfWriter()
        
        # Extrait les pages
        for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        
        # Génère le PDF de sortie
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
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
