from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Game, Player, Score
import os

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
    data = request.get_json()

    game = Game(date=data['date'], place=data['place'], track_count=data['track_count'])
    db.session.add(game)

    for idx, player in enumerate(data['players']):
        p = Player(name=player['name'], order=idx, game=game)
        db.session.add(p)
        for track, value in player['scores'].items():
            s = Score(track_number=int(track), value=int(value), player=p)
            db.session.add(s)

    db.session.commit()
    return {"status": "success"}

@app.route("/history")
def history():
    games = Game.query.order_by(Game.id.desc()).all()
    return render_template("history.html", games=games)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
