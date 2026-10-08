import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
  # Home page ya featured characters
  url = "https://hp-api.onrender.com/api/characters"
  response = requests.get(url)
  return render_template("index.html", characters=response.json()[:10])


@app.route("/spells")
def spells():
  url = "https://hp-api.onrender.com/api/spells"
  response = requests.get(url)
  return render_template("spells.html", spells=response.json())


@app.route("/houses")
def houses():
  return render_template("houses.html")


@app.route("/character/<string:character_id>")
def character_detail(character_id):
    url = f"https://hp-api.onrender.com/api/character/{character_id}"
    response = requests.get(url)
    character_data = response.json()
    character = character_data[0] if isinstance(character_data, list) and character_data else character_data

    # Custom roles/biography dictionary for main characters
    character_roles = {
        "Harry Potter": "The Boy Who Lived, the wizard destined to defeat Lord Voldemort and leader of Dumbledore's Army.",
        "Hermione Granger": "The brightest witch of her age, known for her unmatched intellect, loyalty, and vital role in finding the Horcruxes.",
        "Ron Weasley": "Harry's fiercely loyal best friend, master chess player, and a core member of Dumbledore's Army.",
        "Severus Snape": "The enigmatic Double Agent, Potions Master, and Head of Slytherin house who secretly protected Harry throughout his journey.",
        "Draco Malfoy": "A Slytherin student, member of the Inquisitorial Squad, and a key figure caught in the pressures of the Death Eaters.",
        "Albus Dumbledore": "The legendary Headmaster of Hogwarts, powerful wizard, and mentor to Harry Potter."
    }

    # Get bio if available, otherwise use a default magical line
    char_name = character.get("name")
    character['bio'] = character_roles.get(char_name,
                                           "A remarkable member of the magical world with a unique journey in Hogwarts.")

    return render_template("characters.html", character=character)

if __name__ == "__main__":
  app.run(debug=True)