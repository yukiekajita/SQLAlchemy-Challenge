from flask import Flask, jsonify

# Dictionary of Justice League
justice_league_members = [
    {"superhero": "Aquaman", "real_name": "Arthur Curry"},
    {"superhero": "Batman", "real_name": "Bruce Wayne"},
    {"superhero": "Cyborg", "real_name": "Victor Stone"},
    {"superhero": "Flash", "real_name": "Barry Allen"},
    {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
    {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
    {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
]

#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
# YOUR CODE GOES HERE
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# @TODO: Complete the routes for your app here
# YOUR CODE GOES HERE
@app.route("/")
def home():
    return "Welcome to the Justice League"

@app.route("/api/vi.0/justice-league")
def justice_league():
    return jsonify(justice_league_members)

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    # YOUR CODE GOES HERE
    app.run(debug=True)
