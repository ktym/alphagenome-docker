import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.runtime_version")

from flask import Flask, request, render_template, send_file
import os
import tempfile
import uuid
from api import analysis

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    sequence = request.form.get("sequence")
    organs = request.form.getlist("organs")
    outputs = request.form.getlist("outputs")

    if not sequence:
        return "No sequence provided", 400

    # Use temp file to store the input sequence
    temp_dir = tempfile.mkdtemp()
    fasta_path = os.path.join(temp_dir, f"input_{uuid.uuid4().hex}.fa")
    with open(fasta_path, "w") as f:
        f.write(">input\n")
        f.write(sequence)

    # Run analysis
    try:
        img_path, logs = analysis(fasta_path, organs, outputs)
    except Exception as e:
        return f"Error: {str(e)}", 500

    # Serve result with embedded image
    img_filename = os.path.basename(img_path)
    return f"<h3>Result:</h3><pre>{logs}</pre><img src='/static/{img_filename}' style='max-width:100%'>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
