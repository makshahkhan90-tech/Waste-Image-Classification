import os, json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

BASE_DIR = Path("D:/Waste-Classification-Project")
DATASET_ROOT = BASE_DIR / "dataset" / "garbage-classification"

def find_data_dir(root):
    for p in root.rglob("*"):
        if p.is_dir() and (p / "cardboard").exists():
            return p
    return root

DATA_DIR = find_data_dir(DATASET_ROOT)
print(f"DATA_DIR: {DATA_DIR}")

IMG_SIZE = 224
BATCH = 16  # kam kar diya taake RAM pe load na aaye
EPOCHS_HEAD = 5  # fast ke liye 5
EPOCHS_FINE = 2  # fast ke liye 2

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.1,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    str(DATA_DIR), target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH, class_mode='categorical',
    subset='training', shuffle=True
)
val_gen = datagen.flow_from_directory(
    str(DATA_DIR), target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH, class_mode='categorical',
    subset='validation', shuffle=False
)

class_names = list(train_gen.class_indices.keys())
print(f"Classes: {class_names}")

(BASE_DIR / "models").mkdir(exist_ok=True)
(BASE_DIR / "report").mkdir(exist_ok=True)

with open(BASE_DIR / "models" / "class_names.json", "w") as f:
    json.dump(class_names, f, indent=2)

base = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base.trainable = False

model = models.Sequential([
    base,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='categorical_crossentropy', metrics=['accuracy'])
print("\n--- Training Head (5 epochs) ---")
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS_HEAD)

print("\n--- Fine Tuning (2 epochs) ---")
base.trainable = True
for layer in base.layers[:-50]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS_FINE)

# Save
model.save(BASE_DIR / "models" / "waste_classifier.h5")
print("Model saved to models/waste_classifier.h5")

# Eval
val_gen.reset()
preds = model.predict(val_gen)
y_pred = np.argmax(preds, axis=1)
y_true = val_gen.classes

report = classification_report(y_true, y_pred, target_names=class_names)
print("\n" + report)

with open(BASE_DIR / "report" / "evaluation_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10,8))
plt.imshow(cm, cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names, rotation=45, ha='right')
plt.yticks(tick_marks, class_names)
plt.tight_layout()
plt.savefig(BASE_DIR / "report" / "confusion_matrix.png")
print("Report saved!")