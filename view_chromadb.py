import chromadb
import os

def view_chroma_content():
    # Connect to your ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    print("📊 CHROMADB CONTENT ANALYSIS")
    print("=" * 50)
    
    # List all collections
    collections = client.list_collections()
    print(f"📁 Found {len(collections)} collections:")
    
    for collection in collections:
        print(f"\n🎯 Collection: {collection.name}")
        print("-" * 30)
        
        # Get collection details
        coll = client.get_collection(collection.name)
        
        # Get all items in this collection
        try:
            items = coll.get()
            
            if items['ids']:
                print(f"📝 Total messages: {len(items['ids'])}")
                print("\n📋 Stored Messages:")
                print("-" * 40)
                
                for i, (doc, metadata, doc_id) in enumerate(zip(items['documents'], items['metadatas'], items['ids'])):
                    print(f"{i+1}. ID: {doc_id}")
                    print(f"   📄 Content: {doc[:100]}...")
                    print(f"   👤 User: {metadata.get('is_user', 'N/A')}")
                    print(f"   🕒 Timestamp: {metadata.get('timestamp', 'N/A')}")
                    print(f"   🆔 Session: {metadata.get('session_id', 'N/A')}")
                    print(f"   💬 Type: {metadata.get('message_type', 'text')}")
                    print()
            else:
                print("❌ No messages found in this collection")
                
        except Exception as e:
            print(f"❌ Error reading collection: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    view_chroma_content()