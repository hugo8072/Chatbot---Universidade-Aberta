from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np


# Loads the specified Hugging Face embeddings model.
def load_embeddings_model(model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
    """
    Loads the specified Hugging Face embeddings model.

    Args:
        model_name (str): Name of the Hugging Face model to load.

    Returns:
        HuggingFaceEmbeddings: The loaded embeddings model.
    """
    return HuggingFaceEmbeddings(model_name=model_name)


# Generates embeddings for a query using the provided embeddings model.
def embed_query_with_model(query, embeddings_model):
    """
    Generates embeddings for a query using the provided embeddings model.

    Args:
        query (str): The query to embed.
        embeddings_model: The embeddings model to use.

    Returns:
        np.ndarray: The generated query embeddings.
    """
    query_embedding = embeddings_model.embed_query(query)
    # Convert to NumPy array if necessary
    if isinstance(query_embedding, list):
        query_embedding = np.array(query_embedding)
    return query_embedding
