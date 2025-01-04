import os
from sentence_transformers import SentenceTransformer


def download_model(model_name, save_directory='data/llms'):
    """
    Downloads a model from the Sentence Transformers library and saves it locally.

    Args:
        model_name (str): Name of the model to download.
        save_directory (str): Directory to save the downloaded model.

    Returns:
        str: Path to the saved model.
    """
    model_path = os.path.join(save_directory, model_name.replace('/', '_'))
    if not os.path.exists(model_path):
        print(f"Downloading model {model_name}...")
        model = SentenceTransformer(model_name)
        model.save(model_path)
    else:
        print(f"Model '{model_name}' is already in the folder '{save_directory}'.")
    return model_path


def download_gguf_model_if_needed(model_url, model_filename, save_directory='data/llms'):
    """
    Downloads a GGUF model from a URL if it is not already saved locally.

    Args:
        model_url (str): URL to download the model from.
        model_filename (str): Filename to save the downloaded model.
        save_directory (str): Directory to save the downloaded model.

    Returns:
        str: Path to the saved model.
    """
    import requests

    model_path = os.path.join(save_directory, model_filename)
    if not os.path.exists(model_path):
        print(f"Downloading GGUF model from {model_url}...")
        response = requests.get(model_url)
        response.raise_for_status()
        with open(model_path, 'wb') as model_file:
            model_file.write(response.content)
        print(f"Model '{model_filename}' downloaded successfully.")
    else:
        print(f"Model '{model_filename}' is already present in the folder '{save_directory}'.")
    return model_path


if __name__ == "__main__":
    sentence_model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    download_model(sentence_model_name)

    model_url = ("https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF/resolve/main/Hermes-3-Llama-3.1-8B"
                 ".Q4_K_M.gguf")
    model_filename = "Hermes-3-Llama-3.1-8B.Q4_K_M.gguf"
    download_gguf_model_if_needed(model_url, model_filename)
