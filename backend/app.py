from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

md = MarkItDown()

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    f = request.files['file']

    original_name = secure_filename(f.filename or "")
    _, ext = os.path.splitext(original_name)
    ext = ext.lower() if ext else ".tmp"  

    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=ext)
        os.close(fd)  
        
        f.save(tmp_path)
        result = md.convert(tmp_path)

        return jsonify({'markdown': result.text_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok, service is healthy'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

