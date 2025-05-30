import sys
import time
from pathlib import Path

from utils.static.paths import AGENDA_FILE, VECTORSTORE_DIR
from a_processing.preprocess import preprocess_agenda
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama


def build_vectorstore(
    agenda_path: str = str(AGENDA_FILE), persist_path: str = str(VECTORSTORE_DIR)
):
    start = time.time()
    print("🔧 Preprocessing raw agenda...")
    tasks = preprocess_agenda(agenda_path)
    texts = [t["texto"] for t in tasks]
    metadatas = [
        {
            "fecha": t["fecha"],
            "etiquetas": ", ".join(t["etiquetas"]) if t["etiquetas"] else None,
        }
        for t in tasks
    ]

    print(f"🧠 Generating embeddings for {len(texts)} items...")
    embedding = OllamaEmbeddings(model="mxbai-embed-large")

    print(f"💾 Persisting to vector store at {persist_path}...")
    db = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metadatas,
        persist_directory=persist_path,
    )
    elapsed = time.time() - start
    print(
        f"✅ Embedded {len(texts)} items in {elapsed:.2f}s and stored at: {persist_path}\n"
    )
    return db


# //We need to pass the context bcs the LLM does not know our custom data, so we retrieve the relevant data and send that inf as context
def generate_answer(question: str, context_docs: list) -> str:
    llm = ChatOllama(model="llama3.2:3b")
    context_text = "\n".join([doc.page_content for doc, _ in context_docs])
    prompt = f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer:"
    response = llm.invoke(prompt)
    return response.content


def query_loop(db):
    print("\n🧠 Ask your agenda anything! Type 'exit' to quit.\n")
    while True:
        q = input("🔎 Query: ").strip()
        if q.lower() == "exit":
            print("👋 Goodbye!")
            break

        print("🔍 Searching...")
        start = time.time()
        results = db.similarity_search_with_score(q, k=5)
        duration = time.time() - start
        print(f"⌛ Search completed in {duration:.2f}s")

        if not results:
            print(f"❌ No results found for query: '{q}'\n")
        else:
            for i, (doc, score) in enumerate(results, 1):
                print(f"\nResult {i} (Score: {score:.4f})")
                print(f"📄 {doc.page_content}")
                print(f"🗂️ {doc.metadata}")

            print("\n🧠 Generating answer from LLM...")
            answer = generate_answer(q, results)
            print("\n💬 LLM Answer:")
            print(answer)


if __name__ == "__main__":
    VECTORSTORE_DIR_PATH = Path(VECTORSTORE_DIR)

    # // First build the vector store if it does not exist 
    if not VECTORSTORE_DIR_PATH.exists():
        print("📂 Vector store not found. Building new store...\n")
        db = build_vectorstore()
    else:
        print("📂 Loading existing vector store...")
        start = time.time()
        embedding = OllamaEmbeddings(model="mxbai-embed-large")
        db = Chroma(
            embedding_function=embedding, persist_directory=str(VECTORSTORE_DIR_PATH)
        )
        print(f"✅ Loaded vector store in {time.time() - start:.2f}s\n")

    query_loop(db)
