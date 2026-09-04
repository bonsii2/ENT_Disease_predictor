"""
Utility script to generate lightweight sample Keras model files (.keras)
for Ear, Nose, and Throat disease prediction.

Run this script once after installing dependencies to generate working dummy model files
so that Flask load_model() succeeds immediately.
"""

import os
import json
import tensorflow as tf

def create_and_save_dummy_model(num_classes, save_path):
    print(f"Creating dummy model for {num_classes} classes -> {save_path}")
    
    # Simple lightweight Sequential model accepting 224x224 RGB image inputs
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 3)),
        tf.keras.layers.Conv2D(8, (3, 3), activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.save(save_path)
    print(f"Saved: {save_path}")

def main():
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)

    configs = [
        ("ear_classes.json", "ear_disease_model.keras"),
        ("nose_classes.json", "nose_disease_model.keras"),
        ("throat_classes.json", "throat_model.keras")
    ]

    for json_file, model_file in configs:
        json_path = os.path.join(models_dir, json_file)
        model_path = os.path.join(models_dir, model_file)
        
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                classes = json.load(f)
            create_and_save_dummy_model(len(classes), model_path)
        else:
            print(f"Warning: {json_path} not found. Skipping.")

if __name__ == "__main__":
    main()
