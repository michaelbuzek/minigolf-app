
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    print("Eingehende Spieldaten:", data)
    return {"status": "success"}

if __name__ == "__main__":
    app.run(debug=True)
