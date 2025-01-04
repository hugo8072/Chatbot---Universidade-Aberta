import json
from controllers.chatbot_controller import handle_question
from config.settings import FAISS_PATHS
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def choose_context():
    """
    Allows the user to choose the context they want to use for interacting with the chatbot.
    """
    print("Choose the context you want to use:")
    print("1. Administrative Aspects of UAB")
    print("2. Virtual Pedagogical Model")
    print("3. Programmatic Contents of UCS of the 3rd year of LEI.")

    choice = input("Enter the number corresponding to the context: ")

    if choice == '1':
        return '1'  # Corresponds to the path for FAISS_PATHS['1']
    elif choice == '2':
        return '2'  # Corresponds to the path for FAISS_PATHS['2']
    elif choice == '3':
        return '3'  # Corresponds to the path for FAISS_PATHS['3']
    else:
        print("Invalid choice.")
        return None


def run_chatbot_terminal():
    """
    Starts the interaction loop with the chatbot through the terminal.
    """
    print("Welcome to the Chatbot! To exit, type 'exit'.")

    context_key = choose_context()
    if not context_key:
        print("Context not selected correctly. Exiting.")
        return

    history = []

    while True:
        question = input("\nAsk your question: ")

        if question.lower() == "exit":
            print("Shutting down the Chatbot. Goodbye!")
            break
        elif not question:
            print("Please write your question correctly.")
            continue

        # Data for the handle_question function
        data = {
            'question': question,
            'context': context_key,
            'history': history
        }

        print("Messages sent:", data)  # For debugging purposes, can be removed

        # Process the question using handle_question from chatbot_controller
        response_data = handle_question(data)

        if 'error' in response_data:
            print(f"\nError: {response_data['error']}")
        else:
            print("\nAnswer:", response_data['answer'])

        # Update the history
        history = response_data['history']


if __name__ == "__main__":
    run_chatbot_terminal()
