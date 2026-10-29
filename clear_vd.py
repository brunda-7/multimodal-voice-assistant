import chromadb

def clear_all_collections():
    """Clear ALL collections in ChromaDB"""
    client = chromadb.PersistentClient(path="./chroma_db")
    
    collections = client.list_collections()
    print(f"🗑️ Found {len(collections)} collections to delete:")
    
    for collection in collections:
        try:
            client.delete_collection(collection.name)
            print(f"✅ Deleted: {collection.name}")
        except Exception as e:
            print(f"❌ Failed to delete {collection.name}: {e}")
    
    print("🎯 All collections cleared!")

# Usage
clear_all_collections()