from utils.static.paths import VECTORSTORE_DIR
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings


def query_agenda(
    query: str,
    filter_by: dict = None,
    persist_path: str = str(VECTORSTORE_DIR),
    top_k: int = 5
):
    """
    Runs a semantic similarity search on the agenda vector store.
    - query: the natural-language query.
    - filter_by: optional metadata filter, e.g., {"etiquetas": "urgente"}.
    - persist_path: path to the shared Chroma DB directory.
    - top_k: number of top results to return.
    """
    # Load embedding model
    embedding = OllamaEmbeddings(model="mxbai-embed-large")

    # Load shared vector store
    db = Chroma(
        embedding_function=embedding,
        persist_directory=persist_path
    )

    # Perform search
    results = db.similarity_search_with_score(query, k=top_k, filter=filter_by)

    # Display results
    print(f"\n🔎 Query: {query}")
    if not results:
        print(f"❌ No results found for query: '{query}'\n")
        return
    for i, (doc, score) in enumerate(results, 1):
        print(f"\nResult {i} (Score: {score:.4f})")
        print(f"📄 Text: {doc.page_content}")
        print(f"🗂️ Metadata: {doc.metadata}")


if __name__ == "__main__":
    # Example calls:
    query_agenda("tareas urgentes", filter_by={"etiquetas": "urgente"})
    # query_agenda("revisar documentación fiscal antes del plazo")
    # query_agenda("pendientes personales", filter_by={"etiquetas": "pendiente"})
