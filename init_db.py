from app import db
from app import User, Workout, Exercise, Sets

# db.create_all()
uid1 = "3uxwTAoNZsNqIfrCyCHyDCaxmIq1"
uid2 = "RNKexcaal8UhWQfOkYoSG73ozcG3"

user1 = User(firebase_uid=uid2)

workout1 = Workout(workout_date="2022-10-03", user=user1)

exercise1 = Exercise(exercise_name="biceps",
                     workout=workout1, comment="I am totally user 2",
                     )

set1 = Sets(reps=10, weight=15, easy=True, done=False,
            exercise=exercise1)

set2 = Sets(reps=11, weight=16, easy=True, done=False,
            exercise=exercise1)

db.session.add(user1)
db.session.add(workout1)
db.session.add(exercise1)
db.session.add_all([set1, set2])
db.session.commit()
