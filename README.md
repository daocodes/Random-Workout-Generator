Random Workout Generator using the WGER API
===========================================

This Python project is a command-line workout generator that pulls live data from the WGER API (https://wger.de/en/software/api) 
to help users create a customized workout based on the muscle groups they want to target. 

Users input muscle groups (e.g., "arms", "core", "legs"), and the program returns a random list of exercises along with set and 
rep recommendations and exercise descriptions (if requested).

--------------------------------------------------------------------------------

Features
--------

- User input for desired muscle groups
- Compound muscle group recognition (e.g., "arms" → biceps, triceps, etc.)
- Pulls real-time exercise data from WGER’s public API
- Suggests reps and sets based on muscle group type
- Outputs English names, descriptions, and estimated workout duration
- Supports compound groupings like "push", "pull", and "full body"

--------------------------------------------------------------------------------

Technologies Used
-----------------

- Python 3
- WGER Public Exercise API
- Requests module
- Random module
- Collections (defaultdict)

--------------------------------------------------------------------------------

How to Use
----------

1. Run the script.
2. When prompted, enter the muscle group(s) you want to train.
3. Review the list of exercises generated.
4. Optionally get detailed instructions and rep/set suggestions.
5. Use the workout at the gym or at home!

Example muscle inputs:
- arms
- legs
- core
- push
- pull
- full body

--------------------------------------------------------------------------------

Reflection
----------

This was my first time working with a real API and pulling live data. I learned a lot about data handling, 
user input processing, and organizing code for real-world use. 

As an aspiring Software Engineer, this project gave me hands-on experience in backend logic, 
API consumption, and making programs that solve everyday problems. I’m excited to keep building, 
learning, and growing on my journey toward becoming a full-fledged SWE.

