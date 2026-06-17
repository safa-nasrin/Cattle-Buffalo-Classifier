# import os
# import io
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from flask import Flask, request, jsonify, send_from_directory
# from tensorflow.keras import layers, models, optimizers

# # --- 1. CONFIGURATION ---
# BREEDS = ['Ayrshire cattle', 'GIR', 'JAFFRABADI', 'MEHSANA', 'MURRAH', 'NILI_RAVI']
# MODEL_PATH = 'buffalo_expert_v2.keras'
# IMAGE_SIZE = (224, 224)

# app = Flask(__name__)

# # -------------------------------
# #   2. THE "EXPERT" ARCHITECTURE (Required for Rebuild)
# # -------------------------------
# def rebuild_expert_model():
#     # We rebuild the structure so your Mac understands the layers perfectly
#     base_model = tf.keras.applications.EfficientNetV2S(
#         weights=None, # None because we are loading your custom weights
#         include_top=False,
#         input_shape=(224, 224, 3),
#         include_preprocessing=True 
#     )
    
#     model = models.Sequential([
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

# # -------------------------------
# #   3. LOAD THE MODEL (Mac-Specific Fix)
# # -------------------------------
# print("🔍 Loading Model for Mac...")
# model = None

# if os.path.exists(MODEL_PATH):
#     try:
#         # Step A: Create the empty structure
#         model = rebuild_expert_model() 
#         # Step B: Load the intelligence (weights) into that structure
#         model.load_weights(MODEL_PATH) 
#         print("✅ SUCCESS: Expert Model loaded correctly on Mac!")
#     except Exception as e:
#         print(f"❌ Weight loading failed: {e}")
#         model = None
# else:
#     print(f"❌ ERROR: {MODEL_PATH} not found in backend folder!")

# # -------------------------------
# #   4. API ENDPOINTS
# # -------------------------------
# @app.route('/')
# def index():
#     # Adjust this path if your index.html is in the ../frontend folder
#     return send_from_directory('.', 'index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded on server'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     try:
#         file = request.files['image']
#         img = Image.open(io.BytesIO(file.read())).convert('RGB')
#         img = img.resize(IMAGE_SIZE)
#         img_array = np.array(img, dtype=np.float32)
#         img_array = np.expand_dims(img_array, axis=0)

#         preds = model.predict(img_array, verbose=0)[0]
#         idx = np.argmax(preds)

#         return jsonify({
#             'predicted_breed': BREEDS[idx].replace('_', ' ').title(),
#             # RIGHT (Sending a raw number)
#             'confidence': float(preds[idx]),
#             'top_3': [{'breed': BREEDS[i].title(), 'confidence': f"{float(preds[i]) * 100:.2f}%"} 
#                       for i in np.argsort(preds)[-3:][::-1]]
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # -------------------------------
# #   5. RUN SERVER
# # -------------------------------
# if __name__ == '__main__':
#     print("🚀 Buffalo Breed API is starting...")
#     app.run(debug=True, port=9001)



#EFFICIENTNETV2S HALF WORKING VERSION(1ST what i done)
# import os
# import io
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from flask import Flask, request, jsonify, send_from_directory
# from tensorflow.keras import layers, models
# from flask_cors import CORS
# # --- 1. CONFIGURATION ---
# # Alphabetical order as trained on Kaggle




# BREEDS = ['Ayrshire cattle', 'GIR', 'JAFFRABADI', 'MEHSANA', 'MURRAH', 'NILI_RAVI']
# MODEL_PATH = 'buffalo_expert_v2.keras'
# IMAGE_SIZE = (224, 224)

# app = Flask(__name__)
# CORS(app)

# # --- 2. ARCHITECTURE REBUILD (The Mac Fix) ---
# def rebuild_expert_model():
#     base_model = tf.keras.applications.EfficientNetV2S(
#         weights=None, 
#         include_top=False, 
#         input_shape=(224, 224, 3),
#         include_preprocessing=True 
#     )
#     model = models.Sequential([
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

# # --- 3. LOAD THE MODEL ---
# print("🔍 Loading Expert Model...")
# model = None
# if os.path.exists(MODEL_PATH):
#     try:
#         model = rebuild_expert_model()
#         model.load_weights(MODEL_PATH)
#         print("✅ SUCCESS: Expert Model loaded correctly!")
#     except Exception as e:
#         print(f"❌ Error loading weights: {e}")
# else:
#     print(f"❌ ERROR: {MODEL_PATH} not found in this folder!")

# # --- 4. API ROUTES ---
# @app.route('/')
# def index():
#     return send_from_directory('.', 'index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded'}), 500
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     try:
#         file = request.files['image']
#         img = Image.open(io.BytesIO(file.read())).convert('RGB').resize(IMAGE_SIZE)
#         img_array = np.expand_dims(np.array(img, dtype=np.float32), axis=0)

#         preds = model.predict(img_array, verbose=0)[0]
#         idx = np.argmax(preds)

#         # Send raw float for confidence so JS can do the math
#         return jsonify({
#             'predicted_breed': BREEDS[idx].replace('_', ' ').title(),
#             'confidence': float(preds[idx]),
#             'top_3': [{'breed': BREEDS[i].title(), 'confidence': float(preds[i])} 
#                       for i in np.argsort(preds)[-3:][::-1]]
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=9001)



# import os
# import io
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from tensorflow.keras import layers, models

# # --- 1. CONFIGURATION ---
# BREEDS = ['AYRSHIRE_CATTLE', 'GIR', 'JAFFRABADI', 'MEHSANA', 'MURRAH', 'NILI_RAVI']
# IMAGE_SIZE = (224, 224)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_FILE_PATH = os.path.join(BASE_DIR, 'buffalo_expert_v3.keras')

# app = Flask(__name__)
# CORS(app)

# # --- 2. ARCHITECTURE REBUILD (The Mac Fix) ---
# # This solves the "expects 1 input but received 2" error
# def rebuild_expert_model():
#     # Rebuild the EfficientNet base without the top head
#     base_model = tf.keras.applications.EfficientNetV2S(
#         weights=None, 
#         include_top=False, 
#         input_shape=(224, 224, 3)
#     )
    
#     # Rebuild the exact same classifier head you used on Kaggle
#     model = models.Sequential([
#         layers.Input(shape=(224, 224, 3)),
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

# # --- 3. LOAD THE BRAIN ---
# model = None
# print(f"📂 Project Directory: {BASE_DIR}")
# print("🔍 Attempting to rebuild and load weights...")

# if not os.path.exists(MODEL_FILE_PATH):
#     print(f"❌ ERROR: {MODEL_FILE_PATH} not found!")
# else:
#     try:
#         model = rebuild_expert_model()
#         # Loading weights is more flexible across Keras versions than loading the whole model
#         model.load_weights(MODEL_FILE_PATH)
#         print("✅ SUCCESS: Model rebuilt and weights loaded correctly!")
#     except Exception as e:
#         print(f"❌ Rebuild failed. Trying standard load as fallback...")
#         try:
#             model = tf.keras.models.load_model(MODEL_FILE_PATH)
#             print("✅ SUCCESS: Standard load worked!")
#         except Exception as e2:
#             print(f"❌ BOTH METHODS FAILED.")
#             print(f"Detailed Error: {e}")

# # --- 4. ROUTES ---

# @app.route('/')
# def index():
#     # Serves the index.html from the same folder
#     if os.path.exists(os.path.join(BASE_DIR, 'index.html')):
#         return send_from_directory(BASE_DIR, 'index.html')
#     return "❌ Error: index.html not found in backend folder!", 404

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not initialized on server'}), 500
    
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image provided'}), 400

#         file = request.files['image']
#         img = Image.open(io.BytesIO(file.read())).convert('RGB').resize(IMAGE_SIZE)
        
#         # Convert to numpy and preprocess
#         img_array = np.array(img, dtype=np.float32)
#         # Scale pixels for EfficientNet (-1 to 1 or 0 to 1 depending on version)
#         img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
#         img_array = np.expand_dims(img_array, axis=0)

#         # Predict
#         preds = model.predict(img_array, verbose=0)[0]
#         idx = np.argmax(preds)

#         return jsonify({
#             'predicted_breed': BREEDS[idx].replace('_', ' ').title(),
#             'confidence': float(preds[idx]),
#             'top_3': [{'breed': BREEDS[i].title().replace('_', ' '), 'confidence': float(preds[i])} 
#                       for i in np.argsort(preds)[-3:][::-1]]
#         })
#     except Exception as e:
#         print(f"Prediction error: {e}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     # use_reloader=False is important on Macs to prevent double-loading
#     app.run(debug=True, port=9001, use_reloader=False)


