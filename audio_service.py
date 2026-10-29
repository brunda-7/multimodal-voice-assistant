import whisper
import tempfile
import os
from pydub import AudioSegment
import io

class AudioService:
    def __init__(self):
        self.model_loaded = False
        self.model = None
    
    def load_model(self):
        """Load the Whisper model"""
        print("🔄 Loading Whisper model...")
        self.model = whisper.load_model("base")
        self.model_loaded = True
        print("✅ Whisper model loaded successfully")
    
    def convert_to_wav(self, audio_file):
        """Convert WebM/other formats to WAV"""
        try:
            # Read the audio file
            audio_file.seek(0)
            audio_data = audio_file.read()
            
            # Create AudioSegment from bytes
            if audio_file.name.endswith('.webm'):
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
            else:
                # Try to detect format
                audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Convert to WAV format
            wav_io = io.BytesIO()
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_io, format="wav")
            wav_io.seek(0)
            
            return wav_io
            
        except Exception as e:
            print(f"❌ Audio conversion error: {str(e)}")
            raise Exception(f"Could not convert audio file: {str(e)}")
    
    def speech_to_text(self, audio_file):
        """Convert speech to text using Whisper"""
        if not self.model_loaded:
            self.load_model()
        
        temp_wav_path = None
        
        try:
            # Get file info
            audio_file.seek(0, 2)
            file_size = audio_file.tell()
            audio_file.seek(0)
            print(f"📁 Original file: {audio_file.name}, Size: {file_size} bytes")
            
            if file_size < 1000:
                return "Audio file too small. Please record for longer."
            
            # Convert to WAV if needed
            if audio_file.name.endswith('.webm'):
                print("🔄 Converting WebM to WAV...")
                wav_io = self.convert_to_wav(audio_file)
                
                # Save converted WAV to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(wav_io.read())
                    temp_wav_path = tmp_file.name
                
                audio_path = temp_wav_path
            else:
                # Save original file directly
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    for chunk in audio_file.chunks():
                        tmp_file.write(chunk)
                    temp_wav_path = tmp_file.name
                
                audio_path = temp_wav_path
            
            print(f"📁 Processing audio file: {audio_path}")
            
            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                fp16=False,
                language='en',
                task='transcribe',
                no_speech_threshold=0.5
            )
            
            transcribed_text = result["text"].strip()
            print(f"✅ Transcribed text: '{transcribed_text}'")
            
            if not transcribed_text:
                return "No speech detected. Please speak clearly into the microphone."
            
            return transcribed_text
            
        except Exception as e:
            error_msg = f"Error in speech-to-text: {str(e)}"
            print(error_msg)
            return f"Audio processing error: {str(e)}"
        
        finally:
            # Clean up temporary file
            if temp_wav_path and os.path.exists(temp_wav_path):
                os.unlink(temp_wav_path)