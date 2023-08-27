from transformers import BlipProcessor, BlipForConditionalGeneration
from views import raw_image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)

from sentence_transformers import SentenceTransformer


sentence_model = SentenceTransformer('thenlper/gte-large')