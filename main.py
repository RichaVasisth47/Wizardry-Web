import os
from flask import request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def load_json(filename):
    with open(os.path.join(BASE_DIR, "data", filename), encoding="utf-8") as f:
        return json.load(f)




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
    characters = load_json("characters.json")[:10]
    return render_template("index.html", characters=characters)

@app.route("/spells")
def spells():
    return render_template("spells.html", spells=load_json("spells.json"))

@app.route("/houses")
def houses():
  return render_template("houses.html")

@app.route("/character/<string:character_id>")
def character_detail(character_id):
      all_characters = load_json("characters.json")
      character = next((c for c in all_characters if c["id"] == character_id), None)
      if character is None:
          abort(404)

      # Custom roles/biography dictionary for main characters
      character_roles = {
              "Harry Potter": "The Boy Who Lived, the wizard destined to defeat Lord Voldemort and leader of Dumbledore's Army.",
              "Hermione Granger": "The brightest witch of her age, known for her unmatched intellect, loyalty, and vital role in finding the Horcruxes.",
              "Ron Weasley": "Harry's fiercely loyal best friend, master chess player, and a core member of Dumbledore's Army.",
              "Severus Snape": "The enigmatic Double Agent, Potions Master, and Head of Slytherin house who secretly protected Harry throughout his journey.",
              "Draco Malfoy": "A Slytherin student, member of the Inquisitorial Squad, and a key figure caught in the pressures of the Death Eaters.",
              "Albus Dumbledore": "The legendary Headmaster of Hogwarts, powerful wizard, and mentor to Harry Potter."
      }
      character["bio"] = character_roles.get(
          character.get("name"),
          "A remarkable member of the magical world with a unique journey in Hogwarts."
      )
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

if __name__ == "__main__":
  app.run(debug=True)