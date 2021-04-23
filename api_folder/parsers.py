from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('level', required=True)
parser.add_argument('class', required=True)
parser.add_argument('speciality')
parser.add_argument('known_spells')