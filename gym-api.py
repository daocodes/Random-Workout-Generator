import random
from collections import defaultdict

import requests


def suggest_reps(muscle):
    muscle = muscle.lower()
    if muscle in [
        "biceps",
        "triceps",
        "shoulders",
        "calves",
        "forearms",
        "abs",
        "obliques",
    ]:
        return "2–3 sets of 10–15 reps"
    elif muscle in ["quads", "hamstrings", "glutes", "chest", "back", "lats", "traps"]:
        return "3–4 sets of 6–12 reps"
    elif muscle in ["core", "serratus", "lower back"]:
        return "3 sets of 15–20 reps or time-based sets"
    else:
        return "3 sets of 8–12 reps"


# Helper: get muscle name → ID mapping
def get_muscle_name_to_id():
    url = "https://wger.de/api/v2/muscle/"
    response = requests.get(url)
    data = response.json()
    return {muscle["name"].lower(): muscle["id"] for muscle in data["results"]}


def informalizeMuscleNames():
    url = "https://wger.de/api/v2/muscle/"
    response = requests.get(url)
    data = response.json()

    informal_map = {
        "biceps brachii": "biceps",
        "triceps brachii": "triceps",
        "pectoralis major": "chest",
        "latissimus dorsi": "lats",
        "gluteus maximus": "glutes",
        "quadriceps femoris": "quads",
        "biceps femoris": "hamstrings",
        "rectus abdominis": "abs",
        "obliquus externus abdominis": "obliques",
        "trapezius": "traps",
        "deltoid": "shoulders",
        "anterior deltoid": "front delts",
        "soleus": "calves",
        "gastrocnemius": "calves",
        "serratus anterior": "serratus",
        "brachialis": "inner biceps",
    }

    result = {}
    for muscle in data["results"]:
        formal = muscle["name_en"].lower()
        informal = informal_map.get(formal, formal)
        result[informal] = muscle["id"]

    return result


# Your original structure, cleaned up
def allWorkoutsPerMuscle(muscleName):
    listOfWorkouts = []
    url = "https://wger.de/api/v2/exerciseinfo/?language=2&limit=100"

    # normalize muscle name to lowercase
    muscle_map = informalizeMuscleNames()
    muscleName = muscleName.lower()

    if muscleName not in muscle_map:
        print(f"No muscle found with name: {muscleName}")
        return []

    target_id = muscle_map[muscleName]

    while url:
        response = requests.get(url)
        data = response.json()
        for exercise in data["results"]:

            # print(exercise["name"])
            for muscle in exercise["muscles"]:
                if muscle["id"] == target_id:
                    listOfWorkouts.append(exercise)
                    break  # avoid duplicates if multiple muscles match

        url = data["next"]

    return listOfWorkouts
    # print()


def expand_muscle_groups(muscle_groups):
    muscles = []
    for group in muscle_groups:
        group = group.lower()
        if group == "arms":
            muscles.extend(["biceps", "triceps", "brachialis", "forearms"])
        elif group == "back":
            muscles.extend(["lats", "traps", "rhomboids", "erector spinae"])
        elif group == "legs":
            muscles.extend(["quads", "glutes", "hamstrings", "calves"])
        elif group == "shoulders":
            muscles.extend(["delts", "traps", "rotator cuff"])
        elif group == "core":
            muscles.extend(["abs", "obliques", "serratus", "lower back"])
        elif group == "chest":
            muscles.extend(["pectorals", "serratus", "front delts"])
        elif group == "upper body":
            muscles.extend(["chest", "back", "shoulders", "biceps", "triceps"])
        elif group == "lower body":
            muscles.extend(["quads", "hamstrings", "glutes", "calves"])
        elif group == "push":
            muscles.extend(["chest", "triceps", "shoulders"])
        elif group == "pull":
            muscles.extend(["back", "biceps", "forearms"])
        elif group == "full body":
            muscles.extend(
                [
                    "chest",
                    "back",
                    "shoulders",
                    "biceps",
                    "triceps",
                    "quads",
                    "hamstrings",
                    "glutes",
                    "calves",
                    "core",
                ]
            )
        else:
            muscles.append(group)

    return set(muscles)


def workoutMaker(workoutList, muscleList):
    listOfExercises = []
    used_ids = set()
    muscle_to_exercises = defaultdict(list)

    # Categorize exercises by primary muscle group
    for workout in workoutList:
        for muscle in workout.get("muscles", []):
            if muscle["name_en"].lower() in [m.lower() for m in muscleList]:
                muscle_to_exercises[muscle["name_en"].lower()].append(workout)

    # Determine target number of exercises
    total_muscles = len(muscleList)
    total_exercises = 8 if total_muscles >= 4 else 6

    # Ensure each muscle gets at least 2 exercises
    for muscle in muscleList:
        key = muscle.lower()
        options = [w for w in muscle_to_exercises[key] if w["id"] not in used_ids]
        random.shuffle(options)
        selected = options[:2]  # Get up to 2 per muscle group

        for w in selected:
            if len(listOfExercises) < total_exercises:
                listOfExercises.append(w)
                used_ids.add(w["id"])

    # Fill remaining slots randomly with matching exercises
    all_valid = [
        w
        for m in muscleList
        for w in muscle_to_exercises[m.lower()]
        if w["id"] not in used_ids
    ]
    random.shuffle(all_valid)
    for w in all_valid:
        if len(listOfExercises) >= total_exercises:
            break
        listOfExercises.append(w)
        used_ids.add(w["id"])

    print("\nHere's your randomly generated workout:")

    for w in listOfExercises:
        print(f"- {get_english_name(w)}")
    return listOfExercises


def get_english_name(w):
    for t in w.get("translations", []):
        if t.get("language") == 2:
            return t.get("name")
    return "Unknown Name"


def getDescription(exercise_data):
    """
    Extract English description from exercise JSON data.
    Returns description string or a default message if not found.
    """
    translations = exercise_data.get("translations", [])
    for t in translations:
        if t.get("language") == 2:  # language code 2 for English
            desc = t.get("description")
            if desc:
                return desc
    return "No description available"


def generateRandomWorkout():
    listOfRoutines = [
        "Arms",
        "Legs",
        "Back",
        "Chest",
        "Shoulders",
        "Core",
        "Biceps",
        "Triceps",
        "Quads",
        "Hamstrings",
        "Glutes",
        "Calves",
        "Lats",
        "Traps",
        "Delts",
        "Obliques",
        "Upper Body",
        "Lower Body",
        "Chest and Back",
        "Shoulders and Arms",
        "Push",
        "Pull",
        "Full Body",
        "Cardio",
        "Chest-Only",
        "Back-Only",
        "Quad-Focused Legs",
        "Hamstring-Focused Legs",
        "Glute-Focused Legs",
        "Core-Only",
    ]

    muscle_map = informalizeMuscleNames()

    muscleGroups = input(
        "What muscle groups are you looking to work on? (Seperate them by a space)"
    ).lower()
    if not muscleGroups:
        print("Please enter at least one muscle group.")
        return
    workoutList = []

    muscleArray = expand_muscle_groups(muscleGroups.split())

    for i in muscleArray:
        i = i.lower()
        if i in muscle_map:
            print("Looking up workouts for:", i)
            workouts = allWorkoutsPerMuscle(i)
            workoutList.extend(workouts)
        #  for workout in workouts:
        #      workout_name = workout.get("name")
        #     workoutList.append(workout_name)

    if len(workoutList) == 0:
        print(
            "Sorry! We didn't recognize any muscles or groups that you picked. Try again!"
        )
    else:
        print("Found", len(workoutList), "total exercises.")

    buffer = input("Would you like to continue? (Enter anything)")
    exerciseArray = workoutMaker(workoutList, muscleArray)
    decision = (
        input("Do you need help performing these exercises? (Y/N) ").strip().lower()
    )

    if decision in ("y", "yes"):
        for i, e in enumerate(exerciseArray, start=1):
            name = get_english_name(e)
            desc = getDescription(e)
            muscles = [m["name_en"] for m in e.get("muscles", [])]
            reps = suggest_reps(muscles[0]) if muscles else "3 sets of 8–12 reps"
            print(f"{i}. {name}:\n   {desc}\n   Recommended: {reps}\n")

    duration = len(exerciseArray) * 10
    print("Workout Duration Estimate:", duration, "minutes")


generateRandomWorkout()
