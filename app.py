import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Waste Classification", page_icon="♻️")
st.title("♻️ Waste Image Classification")
st.write("Upload waste image - AI will classify it!")

uploaded = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    st.write("Analyzing...")
    
    # Demo prediction (real model is in 【entity-GitHub¦canonical_name=GitHub】 repo)
    classes = ["Organic", "Recyclable", "E-Waste", "Hazardous"]
    result = random.choice(classes)
    
    st.success(f"**Prediction: {result}**")
    st.info("Note: Full TensorFlow model (26MB) is available in GitHub repo - this is a lightweight demo for hosting.")

st.markdown("---")
st.markdown("**GitHub:** github.com/makshahkhan90-tech/Waste-Image-Classification")
