from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    # In a real-world case, you'd handle the audio file here.
    print("Received an audio file")
    return "Audio received"

if __name__ == "__main__":
    app.run(debug=True, port = 5001)