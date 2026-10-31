\# ♻️ Waste Classification AI - Garbage Classification



\## Project Overview

AI-powered waste classification using MobileNetV2 Transfer Learning. Classifies 12 types of waste with 92% accuracy.



\## Classes (12)

battery, biological, brown-glass, cardboard, clothes, green-glass, metal, paper, plastic, shoes, trash, white-glass



\## Results

\- \*\*Validation Accuracy: 91.65%\*\*

\- \*\*Overall Accuracy: 92%\*\*

\- Model: MobileNetV2 (Transfer Learning)

\- Dataset: 12,415 images



\## How to Run

```bash

\# Install

py -3.12 -m pip install -r requirements.txt



\# Train

py -3.12 src/train.py



\# Inference

py -3.12 src/inference.py \[STRIPPED 70 bytes].jpg



\# Web App

py -3.12 app.py

\# Open http://127.0.0.1:5000

