# Chatbot - Universidade Aberta

This project is a chatbot developed to assist students of Universidade Aberta (UAB) by answering their questions based on specific contexts. The chatbot uses FAISS for efficient vector search and LLaMA for generating responses.

## Project Structure

- `app.py`: Main entry point for the Flask application.
- `config/settings.py`: Project configuration.
- `controllers/`: Logic for handling questions and database operations.
- `models/`: Models for embeddings and FAISS index creation.
- `views/`: Routes for the Flask application.
- `data/`: Data files and models used by the application.

## Installation

1. Clone the repository:
git clone https://github.com/hugo8072/Chatbot---Universidade-Aberta



2. Navigate to the project directory:
cd "Chatbot---Universidade-Aberta"



3. Create and activate a virtual environment:
python3 -m venv venv source venv/bin/activate



4. Install the required dependencies:
pip install -r requirements.txt



5. Download the necessary models:
python models/download_models.py


## Configuration

Configuration settings are in `config/settings.py`. Adjust parameters such as `FLASK_CONFIG`, `STATIC_FOLDER`, `TEMPLATES_FOLDER`, `MODEL_PATH`, and `FAISS_PATHS` as needed.

## Run the application

Start the Flask application:
python app.py



Access the chatbot at [http://localhost:5000](http://localhost:5000).

## Terminal Interaction

To interact with the chatbot via terminal, run:
python chatbot_terminal.py



