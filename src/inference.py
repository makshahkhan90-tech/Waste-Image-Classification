import json
from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "waste_classifier.h5"
CLASS_PATH = BASE_DIR / "models" / "class_names.json"

model = load_model(MODEL_PATH)
with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

def predict_waste(img_path: str):
    img = image.load_img(img_path, target_size=(224,224))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(preds))
    return {
        "predicted_class": class_names[idx],
        "confidence": float(preds[idx])
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: py -3.12 src/inference.py <image_path>")
    else:
        result = predict_waste(sys.argv[1])
        print(f"Predicted: {result['predicted_class']} ({result['confidence']*100:.2f}%)")