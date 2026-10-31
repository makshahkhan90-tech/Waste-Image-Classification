from flask import Flask, request, jsonify, render_template_string
from pathlib import Path
import json, numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "waste_classifier.h5"
CLASS_PATH = BASE_DIR / "models" / "class_names.json"

model = load_model(MODEL_PATH)
with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

HTML = """
<!DOCTYPE html>
<html><head><title>Waste Classifier AI</title>
<style>
body{font-family:Arial;background:#f0f8f0;text-align:center;padding:30px}
.card{background:white;padding:25px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,0.1);max-width:500px;margin:auto}
button{background:#2e7d32;color:white;padding:12px 20px;border:none;border-radius:8px;cursor:pointer;font-size:16px}
#result{margin-top:20px;font-size:18px;font-weight:bold}
img{max-width:100%;border-radius:10px;margin-top:15px}
</style></head>
<body>
<div class="card">
<h2>♻️ Waste Classification AI</h2>
<p>Upload waste image (plastic, paper, glass, metal, etc)</p>
<input type="file" id="file" accept="image/*"><br><br>
<button onclick="upload()">Classify</button>
<div id="result"></div>
<img id="preview" style="display:none">
</div>
<script>
function upload(){
  const file=document.getElementById('file').files[0];
  if(!file){alert('Select image');return;}
  document.getElementById('preview').src=URL.createObjectURL(file);
  document.getElementById('preview').style.display='block';
  const fd=new FormData(); fd.append('file',file);
  fetch('/predict',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
    document.getElementById('result').innerHTML=`Predicted: <span style="color:green">${d.predicted_class}</span><br>Confidence: ${(d.confidence*100).toFixed(2)}%`;
  });
}
</script>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/predict', methods=['POST'])
def predict():
    f=request.files['file']
    path=BASE_DIR/"temp.jpg"
    f.save(path)
    img=image.load_img(path,target_size=(224,224))
    x=image.img_to_array(img)/255.0
    x=np.expand_dims(x,axis=0)
    preds=model.predict(x)[0]
    idx=int(np.argmax(preds))
    return jsonify({"predicted_class":class_names[idx],"confidence":float(preds[idx])})

if __name__=='__main__': app.run(debug=True)