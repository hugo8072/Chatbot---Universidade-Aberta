Chatbot - Universidade Aberta

This project is a chatbot designed to assist students of Universidade Aberta (UAB) by answering their questions based on specific contexts. The chatbot leverages FAISS for efficient vector search and LLaMA for generating responses.


Project Structure
app.py: Main entry point for the Flask application.
config/settings.py: Configuration settings for the project.
controllers/: Contains the logic for handling questions and database operations.
models/: Contains the models for embeddings and FAISS index creation.
views/: Contains the routes for the Flask application.
data/: Contains the data files and models used by the application.


Installation

Clone the repository:  
git clone https://github.com/hugo8072/Chatbot---Universidade-Aberta
cd chatbot-project

Create a virtual environment and activate it:  
python3 -m venv venv
source venv/bin/activate

Install the required dependencies: 

pip install -r requirements.txt

Download the necessary models:  
python models/download_models.py


Configuration:
The configuration settings are located in config/settings.py. You can adjust the settings such as FLASK_CONFIG, STATIC_FOLDER, TEMPLATES_FOLDER, MODEL_PATH, and FAISS_PATHS as needed.  


Start the Flask application:  
python app.py
Open your web browser and navigate to http://localhost:5000 to interact with the chatbot.  


Terminal Interaction
To interact with the chatbot via the terminal, run the chatbot_terminal.py script:
python chatbot_terminal.py



