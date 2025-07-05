from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import traceback

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    place = db.Column(db.String(100))
    track_count = db.Column(db.Integer)
    players = db.relationship('Player', backref='game', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    scores = db.relationship('Score', backref='player', lazy=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.Integer)
    score = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()

    try:
        new_game = Game(
            date=data['date'],
            place=data['place'],
            track_count=data['track_count']
        )
        db.session.add(new_game)
        db.session.commit()

        for player_data in data['players']:
            new_player = Player(
                name=player_data['name'],
                game_id=new_game.id
            )
            db.session.add(new_player)
            db.session.commit()

            for track, score in player_data['scores'].items():
                new_score = Score(
                    track=int(track),
                    score=int(score),
                    player_id=new_player.id
                )
                db.session.add(new_score)

        db.session.commit()

        # ✅ Weiterleitung zur Score-Seite
        return jsonify({
            'status': 'success',
            'redirect_url': f'/score/{new_game.id}'
        })
    
    except Exception as e:
        print(f"💥 Fehler beim Speichern: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Fehler beim Speichern: {str(e)}'
        }), 500

@app.route("/score/<int:game_id>")
def score_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template("score_detail.html", game=game)

@app.route("/history")
def history():
    games = Game.query.order_by(Game.id.desc()).all()
    return render_template("history.html", games=games)

@app.route("/game/<int:game_id>")
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template("game_detail.html", game=game)

@app.route("/initdb")
def initdb():
    with app.app_context():
        db.create_all()
    return "✅ Datenbank erstellt"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
