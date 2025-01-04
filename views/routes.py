from flask import Flask, request, jsonify, send_from_directory
from controllers.chatbot_controller import handle_question
from config.settings import STATIC_FOLDER, TEMPLATES_FOLDER


# Initialize the routes for the Flask application.
def initialize_routes(app):
    # Main route that serves the home page (index.html)
    @app.route('/')
    def serve_index():
        return send_from_directory(TEMPLATES_FOLDER, 'index.html')

    # Route to serve static CSS files
    @app.route('/static/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(f'{STATIC_FOLDER}/css', filename)

    # Route to serve static JavaScript files
    @app.route('/static/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(f'{STATIC_FOLDER}/js', filename)

    # Route to handle questions sent by the chatbot
    @app.route('/ask', methods=['POST'])
    def ask():
        data = request.json
        response = handle_question(data)
        return jsonify(response)
