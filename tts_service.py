from TTS.api import TTS
import tempfile
import os
import threading
import time

class TTSService:
    def __init__(self):
        self.model_loaded = False
        self.tts = None
        self._lock = threading.Lock()
        
    def load_model(self):
        """Load TTS model with thread safety"""
        with self._lock:
            if not self.model_loaded:
                print("⚡ Loading TTS model...")
                try:
                    # Fast model optimized for chat responses
                    self.tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
                    self.model_loaded = True
                    print("✅ TTS model loaded successfully")
                except Exception as e:
                    print(f"❌ Failed to load TTS model: {str(e)}")
                    raise
    
    def text_to_speech(self, text):
        """Convert text to speech efficiently"""
        start_time = time.time()
        
        # Ensure model is loaded
        self.load_model()
        
        # Validate input
        if not text or not text.strip():
            return None
            
        # Limit text length for performance
        text = text[:200].strip()
        if not text:
            return None
        
        audio_path = None
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                audio_path = tmp_file.name
            
            # Generate speech with speed optimization
            self.tts.tts_to_file(
                text=text,
                file_path=audio_path,
                length_scale=0.6,  # Faster speech rate
            )
            
            # Read audio data
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            
            # Log performance
            processing_time = time.time() - start_time
            print(f"✅ TTS generated in {processing_time:.2f}s: '{text[:30]}...'")
            
            return audio_data
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ TTS failed after {processing_time:.2f}s: {str(e)}")
            return None
            
        finally:
            # Ensure cleanup
            if audio_path and os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except Exception as cleanup_error:
                    print(f"⚠️ TTS cleanup warning: {cleanup_error}")