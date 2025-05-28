Absolutely — here's a clear explanation of what `main.py` does, step by step:

**Summary of `run/main.py` with function names:**

1. **`build_vectorstore()`**

   * **Purpose:** Preprocesses the raw agenda, generates embeddings, and persists them to the shared Chroma vector store.
   * **Key steps:**

     * Calls `preprocess_agenda()`
     * Instantiates `OllamaEmbeddings` to embed all items
     * Uses `Chroma.from_texts()` to save vectors + metadata
     * Prints timing and success message

2. **`query_loop()`**

   * **Purpose:** Enters an interactive terminal loop, accepts user queries, and displays search results.
   * **Key steps:**

     * Prompts with `input("🔎 Query: ")`
     * Embeds the query via the same `OllamaEmbeddings` model
     * Runs `db.similarity_search_with_score(...)` on the loaded Chroma store
     * Prints each result’s text, metadata, and similarity score

3. **`__main__` block**

   * **Checks** whether `VECTORSTORE_DIR` exists.

     * If **missing**, calls `build_vectorstore()` to create it.
     * If **present**, quickly loads it with `Chroma(...)`.
   * **Finally**, calls `query_loop(db)` to let you ask questions until you type `exit`.


---

## 🧠 `main.py` — Your RAG Pipeline Orchestrator

This is the **entry point** to your agenda assistant.

It handles:

### ✅ 1. **Preprocessing + Embedding (if needed)**

```python
if not Path(VECTORSTORE_PATH).exists():
    print("🔧 Building vector store...")
    db = build_vectorstore(AGENDA_PATH, VECTORSTORE_PATH)
```

* Checks if the vector DB (`./chroma_db`) already exists.
* If not, it:

  * Reads and processes `agenda.txt` into structured tasks.
  * Generates embeddings for each task using `mxbai-embed-large` via Ollama.
  * Stores vectors + metadata in Chroma DB.

---

### ✅ 2. **Loading Vector Store**

```python
else:
    print("📂 Loading existing vector store...")
    embedding = OllamaEmbeddings(model="mxbai-embed-large")
    db = Chroma(embedding_function=embedding, persist_directory=VECTORSTORE_PATH)
```

* If you already embedded the agenda before, it just reuses the Chroma DB.
* Saves time and avoids duplicating work.

---

### ✅ 3. **Interactive Query Loop**

```python
def query_loop(db):
    print("\n🧠 Ask your agenda anything! Type 'exit' to quit.\n")
    while True:
        q = input("🔎 Query: ").strip()
        ...
```

* You can **type natural language questions** (e.g., `"urgent personal tasks"`).
* For each query:

  * It’s embedded into a vector.
  * Chroma returns the top 5 most semantically similar tasks.
  * Each result includes:

    * The **text of the task**
    * Its **metadata** (like `fecha`, `etiquetas`)
    * A **similarity score**

---

### ✅ 4. **Sample Output**

```text
🔎 Query: fiscal documents

Result 1 (Score: 0.2123)
📄 Urgente: revisar y presentar documentación fiscal antes del plazo
🗂️ {'fecha': None, 'etiquetas': ['urgente']}
```

---

## 🧪 TL;DR: What `main.py` Does

| Feature       | What it does                               |
| ------------- | ------------------------------------------ |
| 🧹 Preprocess | Turns messy text into structured tasks     |
| 🧠 Embed      | Uses Ollama to turn tasks into vectors     |
| 📦 Store      | Saves vectors + metadata into Chroma       |
| 🔍 Query      | Lets you ask questions in natural language |
| 🧾 Results    | Returns the most relevant agenda tasks     |

---

Would you like to:

* Add support for **filters by date or tags** during querying?
* Export query results to a file?
* Build a simple UI or chatbot on top of this?

Let’s expand this however you like!
