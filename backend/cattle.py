# import os
# import io
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from flask import Flask, request, jsonify
# from tensorflow.keras import layers, models
# from flask import send_from_directory



# # -------------------------------
# # CONFIGURATION
# # -------------------------------
# BREEDS = ['AYRSHIRE_CATTLE', 'GIR', 'Sahiwal']
# MODEL_PATH = 'cattle_expert_v1.keras'   # Place model in the same folder
# IMAGE_SIZE = (300, 300)

# app = Flask(__name__)

# # -------------------------------
# # LOAD TRAINED MODEL (The Manual Rebuild Fix)
# # -------------------------------
# def build_expert_architecture():
#     """
#     Rebuilds the EXACT same architecture you used during training.
#     This bypasses the 'batch_normalization' loading error.
#     """
#     # 1. Start with the EfficientNet base
#     base_model = tf.keras.applications.EfficientNetV2S(
#         weights=None, 
#         include_top=False, 
#         input_shape=(300, 300, 3)
#     )
    
#     # 2. Add your custom top layers
#     model = models.Sequential([
#         layers.Input(shape=(300, 300, 3)),
#         base_model,
#         layers.GlobalAveragePooling2D(),
#         layers.BatchNormalization(),
#         layers.Dense(512, activation='swish'),
#         layers.Dropout(0.4),
#         layers.Dense(256, activation='swish'),
#         layers.Dropout(0.3),
#         layers.Dense(len(BREEDS), activation='softmax')
#     ])
#     return model

# # Initialize and load the weights
# model = None
# try:
#     print("🔍 Rebuilding architecture and loading weights...")
#     model = build_expert_architecture()
    
#     # Check if the file exists first to avoid confusing errors
#     if not os.path.exists(MODEL_PATH):
#         raise FileNotFoundError(f"Could not find model file at {MODEL_PATH}")
        
#     # We load ONLY the weights (numbers) instead of the whole model object
#     model.load_weights(MODEL_PATH)
#     print("✅ Model loaded successfully via Weight Injection")
# except Exception as e:
#     print(f"❌ ERROR LOADING MODEL: {e}")
#     # Final fallback attempt
#     try:
#         model = tf.keras.models.load_model(MODEL_PATH, compile=False)
#         print("✅ Standard load worked as fallback.")
#     except:
#         print("🛑 CRITICAL: Could not load model at all.")

# # -------------------------------
# # PREDICTION ROUTE
# # -------------------------------
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({"error": "Model not loaded on server"}), 500
        
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image uploaded"}), 400
            
#         file = request.files['image']
#         img = Image.open(io.BytesIO(file.read())).convert('RGB').resize(IMAGE_SIZE)

#         img_array = np.array(img, dtype=np.float32)
#         # Apply EfficientNetV2 specific preprocessing
#         img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
#         img_array = np.expand_dims(img_array, axis=0)

#         preds = model.predict(img_array, verbose=0)[0]
#         idx = int(np.argmax(preds))

#         return jsonify({
#             "predicted_breed": BREEDS[idx].replace('_', ' ').title(),
#             "confidence": float(preds[idx])
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/")
# def home():
#     return send_from_directory(".", "index.html")
# # -------------------------------
# # RUN SERVER
# # -------------------------------
# if __name__ == "__main__":
#     # use_reloader=False is recommended on Macs to avoid double-loading the model
#     app.run(debug=True, port=9001, use_reloader=False)



# import os
# import io
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS 
# from tensorflow.keras import layers, models

# # --- CONFIGURATION ---
# # IMPORTANT: Ensure this matches your Kaggle training exactly!
# BREEDS = ['Ayrshire cattle', 'GIR', 'Sahiwal', 'UNKNOWN']
# MODEL_PATH = 'cattle_expert_v1_1.keras' 
# IMAGE_SIZE = (300, 300)

# app = Flask(__name__)
# CORS(app) # Allows browser connection

# # -------------------------------
# # 1. LOAD THE MODEL (Manual Rebuild Fix)
# # -------------------------------
# def build_expert_architecture():
#     base_model = tf.keras.applications.EfficientNetV2S(
#         weights=None, 
#         include_top=False, 
#         input_shape=(300, 300, 3)
#     )
#     model = models.Sequential([
#         layers.Input(shape=(300, 300, 3)),
#         base_model,
#         layers.GlobalAveragePooling2D(),
#         layers.BatchNormalization(),
#         layers.Dense(512, activation='swish'),
#         layers.Dropout(0.4),
#         layers.Dense(256, activation='swish'),
#         layers.Dropout(0.3),
#         layers.Dense(len(BREEDS), activation='softmax')
#     ])
#     return model

# model = None
# try:
#     print("🔍 Rebuilding architecture...")
#     model = build_expert_architecture()
#     abs_path = os.path.join(os.path.dirname(__file__), MODEL_PATH)
#     print(f"🧠 Loading weights: {abs_path}")
#     model.load_weights(abs_path)
#     print("✅ Model loaded successfully!")
# except Exception as e:
#     print(f"❌ ERROR: {e}")

# # -------------------------------
# # 2. ROUTES
# # -------------------------------

# # This shows your website when you visit 127.0.0.1:9001
# @app.route("/")
# def home():
#     return send_from_directory(".", "index.html")

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         if 'image' not in request.files:
#             return jsonify({"error": "No image uploaded"}), 400
            
#         file = request.files['image']
#         img = Image.open(io.BytesIO(file.read())).convert('RGB').resize(IMAGE_SIZE)

#         img_array = np.array(img, dtype=np.float32)
#         img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
#         img_array = np.expand_dims(img_array, axis=0)

#         preds = model.predict(img_array, verbose=0)[0]
        
#         # --- THE FIX IS HERE ---
#         sorted_indices = np.argsort(preds)[::-1]
#         top_idx = int(sorted_indices[0])
#         second_idx = int(sorted_indices[1]) # We need the 2nd best guess to calculate margin
        
#         confidence = float(preds[top_idx])
#         margin = confidence - float(preds[second_idx]) # Now 'margin' is defined!
#         # -----------------------
#         print(f"DEBUG: Top Breed: {BREEDS[top_idx]}, Confidence: {confidence:.2f}, Margin: {margin:.2f}")
#         # Logic for Unknown
#         if BREEDS[top_idx] == "UNKNOWN" or confidence < 0.40 or margin < 0.10:
#             return jsonify({
#                 "predicted_breed": "Not Recognized",
#                 "confidence": confidence,
#                 "message": "The AI is unsure."
#             })

#         return jsonify({
#             "predicted_breed": BREEDS[top_idx].replace('_', ' ').title(),
#             "confidence": confidence
#         })

#     except Exception as e:
#         print(f"Prediction Error: {e}") # This helps you see the error in your terminal
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=9001, use_reloader=False)


import os
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras import layers, models

# ---------------- CONFIG ----------------
BREEDS = ['Ayrshire cattle', 'GIR', 'Holstein Friesian cattle', 'Jersey cattle', 'Sahiwal', 'UNKNOWN']
IMAGE_SIZE = (300, 300)
MODEL_WEIGHTS = "cattle_expert_v2_final.keras"  # ✅ weights only
PORT = 9003
# ---------------------------------------

app = Flask(__name__)
CORS(app)

# ---------------- MODEL -----------------
def build_model():
    base = tf.keras.applications.EfficientNetV2S(
        include_top=False,
        weights=None,
        input_shape=(300, 300, 3)
    )

    model = models.Sequential([
        layers.Input(shape=(300, 300, 3)),
        base,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(512, activation="swish"),
        layers.Dropout(0.4),
        layers.Dense(256, activation="swish"),
        layers.Dropout(0.3),
        layers.Dense(len(BREEDS), activation="softmax")
    ])
    return model


print("🧠 Rebuilding model architecture...")
model = build_model()

weights_path = os.path.join(os.path.dirname(__file__), MODEL_WEIGHTS)

if not os.path.exists(weights_path):
    raise FileNotFoundError(f"❌ WEIGHTS NOT FOUND: {weights_path}")

model.load_weights(weights_path)
print("✅ Model weights loaded successfully!")

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        img = img.resize(IMAGE_SIZE)

        arr = np.array(img, dtype=np.float32)
        arr = tf.keras.applications.efficientnet_v2.preprocess_input(arr)
        arr = np.expand_dims(arr, axis=0)

        preds = model.predict(arr, verbose=0)[0]

        top = int(np.argmax(preds))
        sorted_idx = np.argsort(preds)[::-1]

        confidence = float(preds[top])
        margin = confidence - float(preds[sorted_idx[1]])

        print(f"🎯 {BREEDS[top]} | conf={confidence:.2f} | margin={margin:.2f}")

        if BREEDS[top] == "UNKNOWN" or confidence < 0.30 or margin < 0.15:
            return jsonify({
                "predicted_breed": "UNKNOWN",
                "confidence": confidence,
                "message": "Low confidence"
            })

        return jsonify({
            "predicted_breed": BREEDS[top],
            "confidence": confidence
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": str(e)}), 500


# ---------------- RUN -------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True,
        use_reloader=False
    )
