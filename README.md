Retrieval-Augmented Generation (RAG) workflow test. 

RAG pattern:

1. **Retrieval**

   * We **preprocess** your raw `agenda.txt` into structured records.
   * We **embed** those records into vectors with a local embedding model (`mxbai-embed-large`).
   * We store those vectors + metadata in a Chroma vector database.

2. **Augmentation**

   * At query time, we **retrieve** the most semantically relevant items by embedding your natural‐language query and doing a similarity search (optionally filtered by tags or dates).
   * Those retrieved items become the “context” or “knowledge” we feed into an LLM for any downstream generation task (in your case, you’re just printing them, but you could extend it to summarization or answer generation).

3. **Generation**

   * Although our current scripts stop at retrieval and display, you can easily plug in an LLM (via Ollama or another interface) to **generate** a concise answer or summary based on the retrieved agenda items.

RAG pipeline: **Preprocess → Embed → Retrieve → (Generate)**.
