from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    place = db.Column(db.String(100))
    track_count = db.Column(db.Integer)
    players = db.relationship('Player', backref='game', cascade="all, delete-orphan")

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    order = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    scores = db.relationship('Score', backref='player', cascade="all, delete-orphan")

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_number = db.Column(db.Integer)
    value = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
