from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.players import Players

app = Flask(__name__)
api = Api(app)


def abort_if_class_not_found(player_id):
    session = db_session.create_session()
    news = session.query(Players).get(player_id)
    if not news:
        abort(404, message=f"Player {player_id} not found")


class ClassResource(Resource):
    def get(self, class_id):
        abort_if_class_not_found(class_id)
        db_sess = db_session.create_session()
        player = db_sess.query(Players).get(class_id)
        return jsonify({'player': player.to_dict()})

    def delete(self, class_id):
        abort_if_class_not_found(class_id)
        db_sess = db_session.create_session()
        player = db_sess.query(Players).get(class_id)
        db_sess.delete(player)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ClassListResource(Resource):
    def get(self):
        session = db_session.create_session()
        players = session.query(Players).all()
        return jsonify({'players': [item.to_dict() for item in players]})
