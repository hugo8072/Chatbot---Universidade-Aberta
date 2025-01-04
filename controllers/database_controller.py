import os
from models.faiss_index import create_faiss_index_from_text, create_faiss_index_from_excel
from models.embeddings import load_embeddings_model
from config.settings import FAISS_PATHS, CONTEXT_FILES
import numpy as np
import warnings

# Load the embeddings model to generate semantic vectors
embeddings_model = load_embeddings_model()


def verify_and_create_db():
    """
    Verify if the FAISS directories and indexes exist; if not, create the necessary indexes.
    """
    if not os.path.exists('vector_DB'):
        os.makedirs('vector_DB')

    if not os.path.exists(FAISS_PATHS['1']):
        print("Creating FAISS index for UAB...")
        create_faiss_index_from_text(CONTEXT_FILES['1'], FAISS_PATHS['1'], embeddings_model)

    if not os.path.exists(FAISS_PATHS['2']):
        print("Creating FAISS index for MPV...")
        create_faiss_index_from_text(CONTEXT_FILES['2'], FAISS_PATHS['2'], embeddings_model)

    if not os.path.exists(FAISS_PATHS['3']):
        print("Creating FAISS index for UCS Excel...")
        create_faiss_index_from_excel(CONTEXT_FILES['3'], FAISS_PATHS['3'], embeddings_model)


def search_faiss_with_embed_query(db, query, embeddings_model, top_k=5):
    """
    Perform a search in a FAISS index using an embedded query.

    Args:
        db: The FAISS database to search in.
        query (str): The query to search for.
        embeddings_model: The embeddings model to generate the query vector.
        top_k (int): The number of top results to return.

    Returns:
        list: List of documents corresponding to the most relevant results.
    """
    # Generate embeddings for the query using embed_query
    query_embedding = embeddings_model.embed_query(query)

    # Convert the embedding to a NumPy array if it is a list
    if isinstance(query_embedding, list):
        query_embedding = np.array(query_embedding)

    # Perform the search in the FAISS index
    D, I = db.index.search(query_embedding.reshape(1, -1), top_k)

    # Retrieve the contexts corresponding to the most relevant results
    results = []
    for i in I[0]:
        doc_id = db.index_to_docstore_id.get(i)
        if doc_id in db.docstore._dict:
            document = db.docstore._dict[doc_id]
            results.append(document)
            print(f"Result {len(results)}: {document.page_content}")
        else:
            print(f"Document with ID {doc_id} not found in docstore.")

    return results if results else None  # Return the list of found documents or None if empty
