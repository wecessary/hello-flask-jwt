from app import User, Workout, Exercise

users = User.query.all()
workouts = Workout.query.all()
exercises = Exercise.query.all()

print(workouts[0].user)
print(users[0].workouts[0].workout_date)
print(users[0].workouts[0].exercises[0].exercise_id)
print(users[0].workouts[0].exercises[0].exercise_name)
print(users[0].workouts[0].exercises[0].comment)
print(users[0].workouts[0].exercises[0].sets[0].reps)
print(users[0].workouts[0].exercises[0].sets[0].easy)

print(users[0].workouts[0].exercises[0].sets[0].set_id)
