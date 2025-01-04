from models.embeddings import load_embeddings_model
from models.faiss_index import load_faiss_index
from llama_cpp import Llama
from config.settings import MODEL_PATH, FAISS_PATHS
from controllers.database_controller import search_faiss_with_embed_query
import warnings
import os

# Ignore only deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load the embeddings model to generate semantic vectors
embeddings_model = load_embeddings_model()

# Initialize the LLaMA model with the specified path and context of 2500 tokens
llm = Llama(model_path=MODEL_PATH, n_ctx=2500, verbose=False)


def save_history_to_file(history, file_path="data/historico/history.txt"):
    """
    Save the question and answer history to a text file.

    Args:
        history (list): List of dictionaries containing questions and answers.
        file_path (str): Path to the file where the history will be saved.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Open the file in append mode ("a"), creating it if it doesn't exist
    with open(file_path, "a", encoding="utf-8") as file:
        for entry in history:
            file.write(f"Pergunta: {entry['pergunta']}\n")
            file.write(f"Resposta: {entry['resposta']}\n")
            file.write("-" * 50 + "\n")


def handle_question(data):
    """
    Process the received question, search in the appropriate context, and generate a response.

    Args:
        data (dict): Dictionary containing the question, context, and history.

    Returns:
        dict: Dictionary containing the answer and updated history.
    """
    question = data.get('question')
    context = data.get('context')
    history = data.get('history', [])

    db_path = FAISS_PATHS.get(context)
    if not db_path:
        return {'error': 'Contexto não encontrado.'}

    db = load_faiss_index(db_path, embeddings_model)
    results = search_faiss_with_embed_query(db, question, embeddings_model)

    if results:
        context_text = "\n\n".join([doc.page_content for doc in results])
        response = generate_response(question, context_text, history)
        history.append({"pergunta": question, "resposta": response})

        # Save the history to the file
        save_history_to_file(history)

        return {'answer': response, 'history': history}
    else:
        return {'answer': "Contexto relevante não encontrado.", 'history': history}


def generate_response(question, context_text, history):
    """
    Generate a response based on the question, provided context, and interaction history.

    Args:
        question (str): The question to be answered.
        context_text (str): The context text to be used for generating the response.
        history (list): List of dictionaries containing previous questions and answers.

    Returns:
        str: The generated response.
    """
    messages = [
        {"role": "system", "content": "És um chatbot para alunos da Universidade Aberta"
                                      ". Caso precises de mais dados para procurares "
                                      "a resposta, pergunta ao utilizador. Responde estritamente com base no contexto "
                                      "fornecido e de forma curta e simpática. Caso a resposta não esteja no "
                                      "contexto, responde 'Não consigo responder a essa questão, experimente "
                                      "reformular a questão ou mudar de tema.' Não utilizes conhecimento prévio. "
                                      "Responde em português de Portugal e evita o gerúndio."},
        {"role": "system", "content": "Sempre que te for possível enumerar dados ou factos, por favor fá-lo. Isto é, "
                                      "sempre que te perguntarem 'quantos/quais/onde/quando etc.' responde com "
                                      "números"},
        {"role": "system", "content": f"Contexto: {context_text}"}
    ]

    for pair in history[-3:]:
        messages.append({"role": "user", "content": pair['pergunta']})
        messages.append({"role": "assistant", "content": pair['resposta']})

    messages.append({"role": "user", "content": question})

    # Print what is sent to the model
    print("\n--- Prompt Sent to the Model ---")
    print(f"Current Question: {question}\n")
    print(f"Context: {context_text}\n")
    print("History (last 3 interactions):")
    for pair in history[-3:]:
        print(f"Question: {pair['pergunta']}")
        print(f"Answer: {pair['resposta']}")
    print("\n--- End of Prompt ---\n")

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=250,
        temperature=0.2,
        top_p=0.9
    )

    return response['choices'][0]['message']['content'].strip()
