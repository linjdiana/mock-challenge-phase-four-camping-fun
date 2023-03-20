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
    # def get(self):
    #     campers = Camper.query.all()
    #     campers_dict_list = [camper.to_dict() for camper in campers]
    #     response = make_response(
    #         campers_dict_list,
    #         200
    #     )
    #     return response

    
    def post(self):

        data = request.get_json()
        try:
            new_camper = Camper(
                id=data['id'],
                name=data['name'],
                age=data['age'],
            )

            db.session.add(new_camper)
            db.session.commit()
            
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message, 422
            )

        return make_response(new_camper.to_dict(), 201)

api.add_resource(Campers, '/campers')

class CampersByID(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return make_response({
                "error": "Camper not found"
            }, 404)
        response = make_response(
            camper.to_dict(rules=('activities',)),
            200
        )
        return response


api.add_resource(CampersByID, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        activities = Activity.query.all()
        activities_dict_list = [activity.to_dict() for activity in activities]

        response = make_response(activities_dict_list, 200)
        return response
 
api.add_resource(Activities, '/activities')

class ActivitiesById(Resource):

    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            return make_response({
                "error": "Activity not found"
            }, 404)
        try:
            db.session.delete(activity)
            db.session.commit()
        except Exception as e:
            return make_response(
                {
                    "errors": [e.__str__()]
                },
                422
            )
        return make_response(
            "",
            200
        )
api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        data = request.get_json()
        try:
            signup = Signup(
                time=data["time"],
                camper_id=data["camper_id"],
                activity_id=data["activity_id"]
            )
            db.session.add(signup)
            db.session.commit()
        except Exception as e:
            response_dict = {
                "errors": [e.__str__()]
            }
            return make_response(
                response_dict,
                422
            )
        response = make_response(
            signup.activity.to_dict(),
            201
        )
        return response

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
