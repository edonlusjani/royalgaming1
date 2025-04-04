from flask import Flask, jsonify, send_from_directory, abort, send_file
from flask_cors import CORS
from ftplib import FTP
import os
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS so your frontend can access this API from a different domain

# FTP credentials
FTP_HOST = "91.187.123.126"
FTP_PORT = 2323
FTP_USER = "Administrator"
FTP_PASS = "Pass!@12.VivaKitgo"

# Sample market data
markets = {
  "Stip": [
    {"name": "Маркет 1", "pdf_link": "Merki_1.pdf"},
    {"name": "Маркет 4", "pdf_link": "Merki_4.pdf"},
    {"name": "Маркет 6", "pdf_link": "Merki_6.pdf"},
    {"name": "Маркет 24", "pdf_link": "Merki_24.pdf"},
    {"name": "Маркет 25", "pdf_link": "Merki_25.pdf"},
    {"name": "Маркет 40", "pdf_link": "Merki_40.pdf"},
    {"name": "Маркет 41", "pdf_link": "Merki_41.pdf"},
    {"name": "Маркет 42", "pdf_link": "Merki_42.pdf"},
    {"name": "Маркет 43", "pdf_link": "Merki_43.pdf"},
    {"name": "Маркет 44", "pdf_link": "Merki_44.pdf"},
    {"name": "Маркет 46", "pdf_link": "Merki_46.pdf"},
    {"name": "Маркет 52", "pdf_link": "Merki_52.pdf"},
    {"name": "Маркет 59", "pdf_link": "Merki_59.pdf"},
    {"name": "Маркет 60", "pdf_link": "Merki_60.pdf"},
    {"name": "Маркет 63", "pdf_link": "Merki_63.pdf"},
    {"name": "Маркет 66", "pdf_link": "Merki_66.pdf"},
    {"name": "Маркет 78", "pdf_link": "Merki_78.pdf"},
    {"name": "Маркет 80", "pdf_link": "Merki_80.pdf"}
  ],
  "Pehcevo": [
    {"name": "Маркет 2", "pdf_link": "Merki_2.pdf"}
  ],
  "Strumica": [
    {"name": "Маркет 3", "pdf_link": "Merki_3.pdf"},
    {"name": "Маркет 17", "pdf_link": "Merki_17.pdf"},
    {"name": "Маркет 21", "pdf_link": "Merki_21.pdf"},
    {"name": "Маркет 33", "pdf_link": "Merki_33.pdf"},
    {"name": "Маркет 36", "pdf_link": "Merki_36.pdf"},
    {"name": "Маркет 37", "pdf_link": "Merki_37.pdf"},
    {"name": "Маркет 38", "pdf_link": "Merki_38.pdf"},
    {"name": "Маркет 62", "pdf_link": "Merki_62.pdf"}
  ],
  "Radovis": [
    {"name": "Маркет 5", "pdf_link": "Merki_5.pdf"},
    {"name": "Маркет 7", "pdf_link": "Merki_7.pdf"},
    {"name": "Маркет 10", "pdf_link": "Merki_10.pdf"},
    {"name": "Маркет 32", "pdf_link": "Merki_32.pdf"}
  ],
  "Gevgelija": [
    {"name": "Маркет 11", "pdf_link": "Merki_11.pdf"},
    {"name": "Маркет 28", "pdf_link": "Merki_28.pdf"}
  ],
  "Kocani": [
    {"name": "Маркет 12", "pdf_link": "Merki_12.pdf"},
    {"name": "Маркет 29", "pdf_link": "Merki_29.pdf"},
    {"name": "Маркет 30", "pdf_link": "Merki_30.pdf"},
    {"name": "Маркет 31", "pdf_link": "Merki_31.pdf"},
    {"name": "Маркет 34", "pdf_link": "Merki_34.pdf"},
    {"name": "Маркет 77", "pdf_link": "Merki_77.pdf"}
  ],
  "Delcevo": [
    {"name": "Маркет 13", "pdf_link": "Merki_13.pdf"},
    {"name": "Маркет 14", "pdf_link": "Merki_14.pdf"},
    {"name": "Маркет 15", "pdf_link": "Merki_15.pdf"},
    {"name": "Маркет 16", "pdf_link": "Merki_16.pdf"},
    {"name": "Маркет 19", "pdf_link": "Merki_19.pdf"}
  ],
  "M.Kamenica": [
    {"name": "Маркет 18", "pdf_link": "Merki_18.pdf"}
  ],
  "Berovo": [
    {"name": "Маркет 20", "pdf_link": "Merki_20.pdf"},
    {"name": "Маркет 26", "pdf_link": "Merki_26.pdf"},
    {"name": "Маркет 72", "pdf_link": "Merki_72.pdf"}
  ],
  "Negotino": [
    {"name": "Маркет 22", "pdf_link": "Merki_22.pdf"}
  ],
  "Kumanovo": [
    {"name": "Маркет 23", "pdf_link": "Merki_23.pdf"},
    {"name": "Маркет 55", "pdf_link": "Merki_55.pdf"},
    {"name": "Маркет 65", "pdf_link": "Merki_65.pdf"}
  ],
  "Kavadarci": [
    {"name": "Маркет 27", "pdf_link": "Merki_27.pdf"}
  ],
  "Bosilovo/Strumica": [
    {"name": "Маркет 33", "pdf_link": "Merki_33.pdf"}
  ],
  "Zrnovci/Kocani": [
    {"name": "Маркет 34", "pdf_link": "Merki_34.pdf"}
  ],
  "Novo Selo": [
    {"name": "Маркет 39", "pdf_link": "Merki_39.pdf"}
  ],
  "Veles": [
    {"name": "Маркет 64", "pdf_link": "Merki_64.pdf"}
  ],
  "Skopje": [
    {"name": "Маркет 67", "pdf_link": "Merki_67.pdf"},
    {"name": "Маркет 68", "pdf_link": "Merki_68.pdf"},
    {"name": "Маркет 69", "pdf_link": "Merki_69.pdf"},
    {"name": "Маркет 70", "pdf_link": "Merki_70.pdf"},
    {"name": "Маркет 75", "pdf_link": "Merki_75.pdf"},
    {"name": "Маркет 76", "pdf_link": "Merki_76.pdf"}
  ],
  "Probistip": [
    {"name": "Маркет 58", "pdf_link": "Merki_58.pdf"},
    {"name": "Маркет 71", "pdf_link": "Merki_71.pdf"},
    {"name": "Маркет 73", "pdf_link": "Merki_73.pdf"}
  ]
}

@app.route('/markets', methods=['GET'])
def get_markets():
    """
    Returns a JSON array of markets.
    """
    return jsonify(markets)

# Function to retrieve the PDF file from the FTP server
def retrieve_pdf_from_ftp(filename):
    ftp = FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    
    # Store the file in memory instead of writing to disk
    pdf_file = BytesIO()
    
    try:
        ftp.retrbinary(f"RETR {filename}", pdf_file.write)
        pdf_file.seek(0)  # Rewind the file to the beginning
        return pdf_file
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None
    finally:
        ftp.quit()

@app.route('/pdf/<path:filename>', methods=['GET'])
def serve_pdf(filename):
    """
    Serves a PDF file from the FTP server.
    """
    pdf_file = retrieve_pdf_from_ftp(filename)
    if pdf_file:
        return send_file(pdf_file, as_attachment=True, download_name=filename, mimetype='application/pdf')
    else:
        abort(404, description="Resource not found")

if __name__ == '__main__':
    app.run(debug=True)
