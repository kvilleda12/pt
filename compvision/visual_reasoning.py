from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import cv2 as cv

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

def process_frame(frame):
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    inputs = processor(pil_img, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(**inputs)

    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption