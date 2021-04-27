from flask_restful import reqparse, abort, Api, Resource

player_parser = reqparse.RequestParser()
player_parser.add_argument('id', required=True)
player_parser.add_argument('name', required=True)
player_parser.add_argument('level', required=True)
player_parser.add_argument('y_class', required=True)
player_parser.add_argument('race')
player_parser.add_argument('speciality')
player_parser.add_argument('known_spells')
