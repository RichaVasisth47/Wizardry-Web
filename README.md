#🧹 Wizardry Web

A fully custom-designed, immersive dark-fantasy full-stack web application built around the magical universe of Harry Potter. This project brings together local JSON data loading, a custom dark-fantasy UI, database-driven features, and cinematic immersive audio—100% conceptualized, designed, and developed from scratch.

##🔮 Key Features
- Magical Homepage & Data Management: Loads character data locally from structured JSON files (`characters.json`) to showcase iconic characters and spells dynamically.
- Custom Dark-Fantasy UI/UX: Hand-crafted CSS layout featuring custom Google Fonts (Cinzel Decorative and MedievalSharp), parchment-style containers, and golden glows.
- 🎵 Cinematic Background Theme: Immersive background music (`harry_potter.mp3`) featuring a persistent floating toggle button with browser autoplay policy handling.
- 🦉 Owl Post & Dispatch Sound: An interactive form that allows users ("witches and wizards") to dispatch messages with a localized sound effect (`owl_hoot.mp3`) and synchronized background muting to prevent audio clashes.
- 🗄️ Database-Driven Persistence: Powered by Flask-SQLAlchemy and SQLite, ensuring that all dispatched owl messages are permanently stored and updated in a secure local database (`owl_posts.db`).
- 📜 Magical Owl Archive: A dedicated live archive page where visitors can view all stored messages sent across the realm.
- 🗑️ Message Management (Vanish Feature): Includes a dynamic delete function allowing administrators/users to remove unwanted or erroneous messages instantly.

##🛠️ Tech Stack
- Backend: Python, Flask, Flask-SQLAlchemy, SQLite
- Frontend: HTML5, Jinja2 Templating, Custom CSS3, JavaScript (Audio API)
- Data Storage: Local JSON files (`characters.json`, `spells.json`)
- Security & Tools: Python-Dotenv (`.env`), Git & GitHub, PyCharm / VS Code

##🚀 Getting Started Locally
To run this project on your local machine, follow these steps:
1. Clone the repository: 
   ```bash
   git clone [https://github.com/RichaVasisth47/Wizardry-Web.git](https://github.com/RichaVasisth47/Wizardry-Web.git)
   cd Wizardry-Web

Create and activate a virtual environment:

Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

Install dependencies:

Bash
pip install Flask Flask-SQLAlchemy python-dotenv

Set up environment variables: Create a .env file in the root directory and add your secret key:

Code snippet
SECRET_KEY=your_magical_secret_key_here

Run the application:

Bash
python main.py

Open your browser and navigate to http://127.0.0.1:5000 to enter the magical realm! ✨

Developed by Richa Vasisth, a full-stack developer 🌟
