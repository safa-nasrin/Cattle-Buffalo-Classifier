# 🐄🐃 Livestock Breed Expert Classifier

> **Project Overview:** A full-stack artificial intelligence application that classifies cattle and buffalo breeds from images or live cameras using dual fine-tuned EfficientNetV2S models.

---

## 📌 Main Features

* **⚡ Dual-Backend Node Engine:**
    * **Cattle Server:** Runs on Port `9003` (Handles 6 classes)
    * **Buffalo Server:** Runs on Port `9002` (Handles 4 classes)
* **🧠 Deep Learning Backbone:**
    * Utilizes **EfficientNetV2S** transfer learning weights.
    * Optimized with data augmentation and custom fine-tuning.
* **🎨 Responsive Client Dashboard:**
    * Interactive sliding category toggle buttons.
    * Support for dragging images directly from Google Images.
    * HTML5 MediaStreams API integration for live webcam capture.
* **🛡️ Security Guard Logic:**
    * Rejects low-confidence guesses ($<60\%$).
    * Filters out background/noise using specific margin thresholds.

---

## 📊 Supported Classifications

### 🐄 Cattle Node (Port 9003)
* Ayrshire cattle
* GIR
* Holstein Friesian cattle
* Jersey cattle
* Sahiwal
* UNKNOWN (Noise Class)

### 🐃 Buffalo Node (Port 9002)
* JAFFRABADI
* MEHSANA
* MURRAH
* NILI_RAVI

---

## 🛠️ Step-by-Step Local Deployment

### 1️⃣ Prepare Environment
```bash
# Clone and enter the workspace
git clone [https://github.com/safa-nasrin/Cattle-Buffalo-Classifier.git](https://github.com/safa-nasrin/Cattle-Buffalo-Classifier.git)
cd BREED

# Initialize Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install flask flask-cors tensorflow pillow numpy
