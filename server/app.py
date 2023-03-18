from flask import Flask, request, make_response, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    response = make_response(
        {
            "message": "Hello Campers!"
        },
        200
    )
    return response

# @app.route('/campers', methods=['GET', 'POST'])
# def campers():

#     campers = []
#     for camper in Camper.query.all():
#         camper_dict = camper.to_dict()
#         campers.append(camper_dict)

#     response = make_response(
#         campers,
#         200
#     )
#     return response

class Campers(Resource):
    def get(self):
        campers = []
        for camper in Camper.query.all():
            camper_dict = {
                "id": camper.id,
                "name": camper.name,
                "age": camper.age,
            }

            campers.append(camper_dict)
        response = make_response(
            campers,
            200,
        )

        return response
    
    def post(self):

        data = request.get_json()

        new_camper = Camper(
            id=data['id'],
            name=data['name'],
            age=data['age'],
        )

        db.session.add(new_camper)
        db.session.commit()

        return make_response(new_camper.to_dict(), 201)

api.add_resource(Campers, '/campers')

class CampersByID(Resource):
    def get(self, id):
        campers_by_id = []
        for camper in Camper.query.filter_by(id=id):
            camper_id_dict = {
                "id": camper.id,
                "name": camper.name,
                "age": camper.age,
                # "activities": camper.activities,
            }

            campers_by_id.append(camper_id_dict)
        
        if not camper: 
            abort(404, "Camper not found")

        response = make_response(
            campers_by_id,
            200,
        )

        return response

api.add_resource(CampersByID, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        activities = []
        for activity in Activity.query.all():
            activity_dict = {
                "id": activity.id,
                "name": activity.name,
                "difficulty": activity.difficulty,
            }

            activities.append(activity_dict)
        
        # if not camper: 
        #     abort(404, "Camper not found")

        response = make_response(
            activities,
            200,
        )

        return response
    
api.add_resource(Activities, '/activities')

class Signups(Resource):
    def get(self):
        pass

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
