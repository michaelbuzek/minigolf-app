from flask import Flask, render_template, request, redirect
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

@app.route("/score_input", methods=["POST"])
def score_input():
    try:
        place = request.form["place"]
        date = request.form["date"]
        track_count = int(request.form["tracks"])
        player_count = int(request.form["players"])

        players = []
        for i in range(player_count):
            name = request.form.get(f"player_{i}")
            if name:
                players.append(name)

        return render_template("score_input.html", place=place, date=date, track_count=track_count, players=players)
    except Exception as e:
        print("💥 Fehler bei der Weiterleitung zur Score-Eingabe:", e)
        traceback.print_exc()
        return "Fehler beim Vorbereiten des Score-Inputs", 500

@app.route("/save", methods=["POST"])
def save():
    try:
        place = request.form["place"]
        date = request.form["date"]
        track_count = int(request.form["track_count"])
        player_count = int(request.form["player_count"])

        game = Game(date=date, place=place, track_count=track_count)
        db.session.add(game)

        for i in range(player_count):
            name = request.form[f"player_{i}"]
            player = Player(name=name, order=i, game=game)
            db.session.add(player)

            for t in range(1, track_count + 1):
                value = request.form.get(f"score_{i}_{t}", "0")
                try:
                    val = int(value)
                except ValueError:
                    val = 0
                score = Score(track_number=t, value=val, player=player)
                db.session.add(score)

        db.session.commit()
        return redirect("/history")
    except Exception as e:
        print("💥 Fehler beim Speichern:", e)
        traceback.print_exc()
        return "Fehler beim Speichern", 500

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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
