import os

from flask import request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests
from flask import Flask, render_template




load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_magical_key") # Flash messages

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///owl_posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model (Table Structure)
class OwlPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wizard_name = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    house = db.Column(db.String(50), default="Gryffindor") # New Field


with app.app_context():
    db.create_all()

@app.route("/")
def home():
  # Home page or featured characters
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


# 🦉 Owl Post Route (Contact Form)
@app.route("/owl-post", methods=["GET", "POST"])
def owl_post():
    if request.method == "POST":
        wizard_name = request.form.get("wizard_name")
        receiver = request.form.get("receiver")
        message = request.form.get("message")
        house = request.form.get("house")  # Get house from dropdown

        new_post = OwlPost(wizard_name=wizard_name, receiver=receiver, message=message, house=house)
        db.session.add(new_post)
        db.session.commit()

        flash("Your owl has successfully taken flight! 🦉✨", "success")
        return redirect(url_for("owl_archive"))

    return render_template("owl_post.html")

# 📜 Owl Archive Route (Display Saved Messages)
@app.route("/owl-archive")
def owl_archive():
    posts = OwlPost.query.all()
    return render_template("owl_archive.html", posts=posts)

# 🗑️ Delete Owl Post Route
@app.route("/delete-post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post_to_delete = OwlPost.query.get_or_404(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    flash("The owl post has vanished into thin air! 🦉💨", "success")
    return redirect(url_for("owl_archive"))

@app.route('/characters')
def characters():
    try:
        response = requests.get('https://hp-api.onrender.com/api/characters', timeout=5)
        response.raise_for_status()
        characters_data = response.json()
    except Exception as e:
        # PythonAnywhere free tier fallback data
        characters_data = [
            {
                "name": "Harry Potter",
                "house": "Gryffindor",
                "actor": "Daniel Radcliffe",
                "image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f"
            },
            {
                "name": "Hermione Granger",
                "house": "Gryffindor",
                "actor": "Emma Watson",
                "image": ""
            }
        ]
    return render_template('characters.html', characters=characters_data)


if __name__ == "__main__":
  app.run(debug=True)