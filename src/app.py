"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_get_user():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200


@app.route('/user/favorites', methods=['GET'])
def handle_user_favorites():
    body = request.get_json()
    user_login = body['login']

    user = User.query.filter_by(login=user_login).first()
    favorites = user.serialize()["favorites"]
   
    return jsonify(favorites), 200



@app.route('/people', methods=['GET'])
def handle_get_people():
    people = Characters.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    
    return jsonify(all_people), 200



@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    
    return jsonify(all_planets), 200



@app.route('/people/<int:people_id>', methods=['GET'])
def handle_individual_people(people_id):
    people = Characters.query.filter_by(id = people_id)
   
    return jsonify(people), 200



@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_individual_planets(planet_id):
    planet = Planets.query.filter_by(id = planet_id)
   
    return jsonify(planet), 200



@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_favorite_person(people_id):
    body = request.get_json()
    user_id = body['id']
    
    newfav = Favorites(user_id = user_id, character_id = people_id, planet_id = None)
    db.session.add(newfav)
    db.session.commit()
    
    return jsonify('Favorite Person has been created'), 200



@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body['id']
    
    newfav = Favorites(user_id = user_id, character_id = planet_id, planet_id = None)
    db.session.add(newfav)
    db.session.commit()
    
    return jsonify('Favorite planet has been created'), 200



@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def handle_Delete_favorite_person(people_id):
    body = request.get_json()
    user_id = body['id']
    
    fav = Favorites.query.filter_by(user_id = user_id, character_id = people_id).first()
   
    db.session.add(fav)
    db.session.commit()
    
    return jsonify('Favorite has been Deleted'), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_Delete_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body['id']
    
    fav = Favorites.query.filter_by(user_id = user_id, character_id = planet_id).first()
   
    db.session.delete(fav)
    db.session.commit()
    
    return jsonify('Favorite Planet has been Deleted'), 200


























# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
