from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import InvalidIdTokenError
from functools import wraps

# create the extension

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# initialize the app with the extension
db = SQLAlchemy(app)
api = Api(app)

# default_app = firebase_admin.initialize_app()

cred = credentials.Certificate("fb_admin_config.json")
firebase_admin.initialize_app(cred)

temp_ID_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU4NWI5MGI1OWM2YjM2ZDNjOTBkZjBlOTEwNDQ1M2U2MmY4ODdmNzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd29ya291dC10cmFja2VyLWJkMGY1IiwiYXVkIjoid29ya291dC10cmFja2VyLWJkMGY1IiwiYXV0aF90aW1lIjoxNjY0Nzk1MDQ2LCJ1c2VyX2lkIjoiM3V4d1RBb05ac05xSWZyQ3lDSHlEQ2F4bUlxMSIsInN1YiI6IjN1eHdUQW9OWnNOcUlmckN5Q0h5RENheG1JcTEiLCJpYXQiOjE2NjQ4MTI1NDksImV4cCI6MTY2NDgxNjE0OSwiZW1haWwiOiJ0ZXN0QGVtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ0ZXN0QGVtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.UfhYx0J02MIQaqwWcd6k50QcPekHEAhb2al8yvwXRXURBxPRCdBvXIJoxVRKyfRa8f3T7FYfhlctPuUZCcuea-qiczwFCsQwrgVSfgK6J1SA1r3UP0Qg1eTdD5bVFWPDUPgEU7kx3UCtUXT8HylxVxVBsegGqi6lUY4OF2nnNBOwd6OxWfyUkABWBXJ5EvJ02d3Tb0kIz54mebqfBz-Dtxh7sGyCcz77DAdQLVB1V7xsTYn3pxTpBi80W3xO55prETwT4ZP3UruNLCNdsqdo4gGrJkIFth4emE5ohdboTPB6mSCc5frSOMmT9uGmuDxzUkoPb_47542UKSCxBla2uA"
ID_token2 = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU4NWI5MGI1OWM2YjM2ZDNjOTBkZjBlOTEwNDQ1M2U2MmY4ODdmNzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd29ya291dC10cmFja2VyLWJkMGY1IiwiYXVkIjoid29ya291dC10cmFja2VyLWJkMGY1IiwiYXV0aF90aW1lIjoxNjY0ODEzMzIzLCJ1c2VyX2lkIjoiUk5LZXhjYWFsOFVoV1FmT2tZb1NHNzNvemNHMyIsInN1YiI6IlJOS2V4Y2FhbDhVaFdRZk9rWW9TRzczb3pjRzMiLCJpYXQiOjE2NjQ4MTMzMjMsImV4cCI6MTY2NDgxNjkyMywiZW1haWwiOiJ0ZXN0MkBlbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidGVzdDJAZW1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.pHDTx2vsn1o4ptNaGtEzdi2GKXwZEujLL0OB2ijzzVarsDnCL_C9UZye8xPn-Ht-ZFcjgGOxTffDpiVqSu3dNbzm8OZ2Nr30OlGB9rWcmbsJuBJtSlRECup5bne54__a1bhnxhG4IdZEscJZh8beMgseoBGViVpFf4bnk5ItJT0lsdSl9fLALQksG7v3znxr5yjH2qlP_gnjTWDEnk9_s6ojUuW21Yui0xve8HfnXFPy2TyDjybGnGIUeDqOCPJBakGUJynqejbwVXxkkDe98yQSGZnBbhuVZyw6pYAD1ajYxYBRoimZMEI2bowWmOW0hV3IuOradozfNstsLwi07w"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String, unique=True)
    workouts = db.relationship("Workout", backref="user")


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_date = db.Column(db.String)
    exercises = db.relationship("Exercise", backref="workout")
    user_id = db.Column(db.String, db.ForeignKey("user.id"))


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String)
    sets = db.relationship("Sets", backref="exercise")
    workout_id = db.Column(db.String, db.ForeignKey("workout.id"))
    comment = db.Column(db.String)


class Sets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    easy = db.Column(db.Boolean)
    done = db.Column(db.Boolean)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing.",
                            "error": "Unauthorized"}), 401
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = User.query.filter_by(firebase_uid=uid).first()
        except Exception as e:
            return {
                       "message": "Something went wrong",
                       "data": None,
                       "error": str(e)
                   }, 500
        return f(user, *args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
@token_required
def getUser(user):
    sets = [
        {"index": user.workouts[0].exercises[0].sets[0].id,
         "reps": user.workouts[0].exercises[0].sets[0].reps,
         "weight": user.workouts[0].exercises[0].sets[0].weight,
         "easy": user.workouts[0].exercises[0].sets[0].easy,
         "done": user.workouts[0].exercises[0].sets[0].done
         }]

    workoutData = {
        "index": user.workouts[0].exercises[0].id,
        "name": user.workouts[0].exercises[0].exercise_name,
        "comment": user.workouts[0].exercises[0].comment,
        "sets": sets}

    user_data = [
        {"date": user.workouts[0].workout_date, "workoutData": workoutData}
    ]
    return user_data, 200


if __name__ == "__main__":
    app.run(debug=True)

#
# initial_workout_data = [
#     {
#         "index": 0,
#         "name": "",
#         "sets": [
#             {"index": 0, "reps": 0, "weight": 0, "easy": True, "done": False},
#             {"index": 1, 'reps': 0, "weight": 0, "easy": True, "done": False},
#         ],
#         "comment": "",
#     },
# ]
