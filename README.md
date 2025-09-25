DeepGuard — AI-Powered Deepfake Detection Tool

DeepGuard is a multi-modal deepfake detection system that analyzes images and videos using artifact detection, motion analysis, and fusion models to determine content authenticity. It also provides visualizations (ELA, DCT) and optional PDF reports for easy sharing.

⸻

Features
	•	Artifact Detection: Detects inconsistencies in images using a CNN-based pipeline.
	•	Motion Analysis: Detects abnormal facial motion using LSTM-based temporal analysis.
	•	Fusion Model: Combines artifact and motion scores to generate a confidence score for manipulation.
	•	Visualizations:
	•	Error Level Analysis (ELA) maps
	•	Discrete Cosine Transform (DCT) maps
	•	Multi-File Support: Handles images (.jpg, .png) and videos (.mp4, .avi).
	•	PDF Report Generation: Summarizes analysis results with file hash, scores, and confidence.
	•	Cross-Platform: Works on macOS (supports Apple MPS GPU).

⸻

Installation

Prerequisites
	•	Python 3.9 or 3.10
	•	PyTorch with MPS support (for Apple Silicon)
	•	virtualenv or pyenv recommended
  Step-by-Step
	1.	Clone the repository: git clone https://github.com/Yashraj2050/ai_detection.git
cd ai_detection
2.	Create and activate a virtual environment:python -m venv deepguard-venv
source deepguard-venv/bin/activate
	3.	Install dependencies: pip install -r requirements.txt
	4.	Set environment variable for the source folder: export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
  Usage

Run the Streamlit app: streamlit run src/app.py
	•	Upload an image or video file.
	•	Wait for the artifact, motion, and fusion analysis to complete.
	•	View visualizations and manipulation confidence.
	•	Optionally, download a PDF report.

⸻

Project Structure
deepguard_1/
│
├─ src/
│   ├─ app.py                # Main Streamlit app
│   ├─ utils/
│   │   ├─ io_utils.py       # File loading and frame extraction
│   │   └─ preprocessing.py  # Face detection, landmark extraction
│   ├─ detectors/
│   │   ├─ ela.py            # ELA maps
│   │   └─ dct_utils.py      # DCT maps
│   ├─ models/
│   │   ├─ artifact_detector.py  # CNN artifact detection
│   │   ├─ motion_detector.py    # LSTM motion detection
│   │   └─ fusion.py             # Fusion model
│   └─ checkpoints/          # Pre-trained model weights (artifact, motion, fusion)
│
├─ deepfake.py               # Optional deepfake detection using DeepFace & Transformers
├─ requirements.txt          # Dependencies list
└─ README.md                 # Project documentation
Model Checkpoints
	•	artifact_detector.pth — Artifact detection weights
	•	motion_lstm.h5 — Motion LSTM model weights
	•	fusion.pkl — Fusion model weights
Dependencies

Key Python packages:
	•	torch, torchvision, timm
	•	tensorflow (for LSTM motion model)
	•	mediapipe (face detection & landmarks)
	•	opencv-python, imageio, Pillow
	•	streamlit
	•	reportlab (PDF report generation)
	•	numpy, scikit-learn
	•	plotly (optional visualizations)
	•	transformers, deepface, web3 (for advanced features)

⸻

Troubleshooting
	•	Blank Streamlit screen: Ensure all dependencies are installed and Python version is compatible.
	•	ModuleNotFoundError: Activate the virtual environment and reinstall missing packages.
	•	Checkpoint errors: Place pre-trained model files in src/checkpoints/.

⸻

License

MIT License

⸻

