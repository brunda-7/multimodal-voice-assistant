import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self, persist_directory="./chroma_db", session_id=None):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.current_session_id = session_id or str(uuid.uuid4())[:8]
        logger.info(f"🆕 Memory Service Initialized - Session: {self.current_session_id}")
    
    def get_collection(self, conversation_id):
        """Get or create collection for a conversation"""
        collection_name = f"conversation_{conversation_id}"
        try:
            collection = self.client.get_collection(collection_name)
        except:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": f"Memory for conversation {conversation_id}"}
            )
        return collection
    
    def store_conversation(self, conversation_id, messages):
        """Store conversation messages"""
        try:
            collection = self.get_collection(conversation_id)
            
            documents = []
            metadatas = []
            ids = []
            
            for i, message in enumerate(messages):
                content = getattr(message, 'content', None)
                if content and len(content.strip()) > 0:
                    timestamp = getattr(message, 'timestamp', datetime.now())
                    message_id = f"{self.current_session_id}_{i}_{timestamp.timestamp()}"
                    
                    documents.append(content)
                    metadatas.append({
                        "is_user": getattr(message, 'is_user', False),
                        "timestamp": timestamp.isoformat(),  # ✅ FIX: ISO format
                        "conversation_id": conversation_id,
                        "session_id": self.current_session_id,
                    })
                    ids.append(message_id)
            
            if documents:
                logger.info(f"🔄 Storing {len(documents)} messages")
                
                embeddings = self.embedder.encode(documents, convert_to_tensor=False)
                embeddings_list = [embedding.tolist() for embedding in embeddings]
                
                collection.add(
                    embeddings=embeddings_list,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                
                logger.info(f"✅ Successfully stored {len(documents)} messages")
                
        except Exception as e:
            logger.error(f"❌ Error storing conversation: {str(e)}")
    
    def get_relevant_context(self, conversation_id, query, n_results=5):
        """Retrieve relevant context efficiently"""
        try:
            logger.info(f"🔍 Retrieving context for: '{query}'")
            
            collection = self.get_collection(conversation_id)
            
            # ✅ FIX: Use ChromaDB's native filtering (MUCH faster)
            results = collection.get(
                where={"session_id": self.current_session_id},
                limit=n_results * 2,  # Get extra to sort by recency
                include=["documents", "metadatas"]
            )
            
            if not results['documents']:
                logger.info("🔍 No context found")
                return {"documents": [], "metadatas": []}
            
            # ✅ FIX: Sort by timestamp (most recent first)
            messages_with_times = []
            for doc, meta in zip(results['documents'], results['metadatas']):
                try:
                    # Parse ISO timestamp for sorting
                    timestamp = datetime.fromisoformat(meta.get('timestamp', ''))
                    messages_with_times.append((doc, meta, timestamp))
                except:
                    # Fallback if timestamp parsing fails
                    messages_with_times.append((doc, meta, datetime.now()))
            
            # Sort by timestamp descending (newest first)
            messages_with_times.sort(key=lambda x: x[2], reverse=True)
            
            # Take only the most recent n_results
            recent_messages = messages_with_times[:n_results]
            
            recent_docs = [doc for doc, meta, timestamp in recent_messages]
            recent_metas = [meta for doc, meta, timestamp in recent_messages]
            
            logger.info(f"🔍 Returning {len(recent_docs)} recent messages")
            
            # Log context
            for i, (doc, meta) in enumerate(zip(recent_docs, recent_metas)):
                role = "USER" if meta.get('is_user') else "AI"
                logger.info(f"   {i+1}. {role}: {doc[:60]}...")
            
            # ✅ FIX: Return FLAT lists (not nested)
            return {
                "documents": recent_docs,    # [doc1, doc2, doc3] - NOT [[doc1, doc2, doc3]]
                "metadatas": recent_metas    # [meta1, meta2, meta3] - NOT [[meta1, meta2, meta3]]
            }
            
        except Exception as e:
            logger.error(f"❌ Error retrieving context: {str(e)}")
            return {"documents": [], "metadatas": []}
    
    def start_new_session(self):
        """Start a fresh session"""
        old_session = self.current_session_id
        self.current_session_id = str(uuid.uuid4())[:8]
        logger.info(f"🔄 New session: {old_session} → {self.current_session_id}")
        return {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_session_info(self):
        """Get current session information"""
        return {
            "session_id": self.current_session_id,
            "timestamp": datetime.now().isoformat()
        }