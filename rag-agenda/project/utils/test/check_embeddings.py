# after you do:
db = Chroma(embedding_function=embedding, persist_directory=VECTORSTORE_PATH)

# add this:
store = db.get()  
docs = store["documents"]  
print(f"\n🔢 Vector store contains {len(docs)} documents.\n")
