from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# SQLite Datenbank im lokalen Verzeichnis
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'minigolf.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Datenmodell
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platz = db.Column(db.String(100))
    datum = db.Column(db.String(20))
    tracks = db.Column(db.Integer)
    players = db.Column(db.Text)  # JSON als String
    scores = db.Column(db.Text)   # JSON als String

# Hauptseite
@app.route('/')
def index():
    return render_template('index.html')

# Spiel speichern
@app.route('/save', methods=['POST'])
def save():
    data = request.json
    game = Game(
        platz=data.get('platz'),
        datum=data.get('datum'),
        tracks=data.get('tracks'),
        players=data.get('players'),
        scores=data.get('scores')
    )
    db.session.add(game)
    db.session.commit()
    return jsonify({"status": "success"}), 201

# Spiele abrufen (Historie)
@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.order_by(Game.id.desc()).all()
    result = []
    for g in games:
        result.append({
            "id": g.id,
            "platz": g.platz,
            "datum": g.datum,
            "tracks": g.tracks,
            "players": g.players,
            "scores": g.scores
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
