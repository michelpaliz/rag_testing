import time
from pathlib import Path

from utils.static.paths import AGENDA_FILE, VECTORSTORE_DIR
from a_processing.preprocess import preprocess_agenda
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


def embed_agenda(
    data_path: str = str(AGENDA_FILE), persist_path: str = str(VECTORSTORE_DIR)
):
    """
    Reads the agenda, generates embeddings, and stores them in a shared Chroma DB.
    Displays progress and timing in the terminal.
    """
    start = time.time()
    print("🔧 Preprocessing raw agenda...")
    # //We preprocess the data first line by line
    tasks = preprocess_agenda(data_path)
    # // Then we collecting the cleaned text lines
    texts = [task["texto"] for task in tasks]
    metadatas = [
        {
            "fecha": task["fecha"],
            "etiquetas": ", ".join(task["etiquetas"]) if task["etiquetas"] else None,
        }
        for task in tasks
    ]

    print(f"🧠 Generating embeddings for {len(texts)} items...")

    # //IMPORTANT
    # // this generates the embeddings and this will be used to turn texts into vectors
    embedding = OllamaEmbeddings(model="mxbai-embed-large")

    # //Now down below we start vectorizing + metadata and saved on the db to sik chroma
    print(f"💾 Persisting to vector store at {persist_path}...")
    db = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_path,
    )
    elapsed = time.time() - start
    print(
        f"✅ Embedded {len(texts)} items in {elapsed:.2f}s and stored at: {persist_path}"
    )
    return db


if __name__ == "__main__":
    # Ensure vector store directory exists or is created during embedding
    if not Path(VECTORSTORE_DIR).exists():
        Path(VECTORSTORE_DIR).mkdir(parents=True, exist_ok=True)
    embed_agenda()
