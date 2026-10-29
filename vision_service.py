from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class VisionService:
    def __init__(self):
        self.model_loaded = False
        self.processor = None
        self.model = None
    
    def load_model(self):
        """Load the larger BLIP model for better accuracy"""
        print("🔄 Loading enhanced BLIP model...")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model_loaded = True
        print("✅ Enhanced BLIP model loaded successfully")
    
    def generate_caption(self, image_file):
        """Generate high-quality caption with optimized parameters"""
        if not self.model_loaded:
            self.load_model()
        
        try:
            # Open and preprocess image
            image = Image.open(image_file).convert('RGB')
            
            # Generate caption with enhanced parameters
            inputs = self.processor(image, return_tensors="pt")
            
            out = self.model.generate(
                **inputs,
                max_length=100,           # Increased for more detail
                num_beams=6,              # Balanced between quality and speed
                early_stopping=True,      # Stop when confident
                no_repeat_ngram_size=2,   # Prevent word repetition
                length_penalty=1.5,       # Encourage slightly longer captions
                temperature=0.8,          # Balanced creativity
            )
            
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            # Post-process caption for better quality
            caption = self._post_process_caption(caption)
            
            print(f"✅ Enhanced caption: {caption}")
            return caption
            
        except Exception as e:
            error_msg = f"Error in image captioning: {str(e)}"
            print(error_msg)
            return f"Could not process image: {str(e)}"
    
    def _post_process_caption(self, caption):
        """Clean up and improve caption quality"""
        # Capitalize first letter
        if caption and len(caption) > 0:
            caption = caption[0].upper() + caption[1:]
        
        # Ensure it ends with proper punctuation
        if caption and not caption.endswith(('.', '!', '?')):
            caption += '.'
        
        return caption