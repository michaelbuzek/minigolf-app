from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Game, Player, Score
import os
import traceback

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json()

        game = Game(date=data['date'], place=data['place'], track_count=int(data['track_count']))
        db.session.add(game)

        for idx, player in enumerate(data['players']):
            p = Player(name=player['name'], order=idx, game=game)
            db.session.add(p)
            for track, value in player['scores'].items():
                try:
                    score_value = int(value)
                except (ValueError, TypeError):
                    score_value = 0
                s = Score(track_number=int(track), value=score_value, player=p)
                db.session.add(s)

        db.session.commit()
        return {"status": "success"}

    except Exception as e:
        print("💥 Fehler beim Speichern:", e)
        traceback.print_exc()
        return {"status": "error", "message": str(e)}, 500

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
