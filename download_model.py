from modelscope import snapshot_download
import os

print("Downloading model all-MiniLM-L6-v2 from ModelScope...")
try:
    model_dir = snapshot_download('sentence-transformers/all-MiniLM-L6-v2')
    print("Model downloaded successfully to:", model_dir)
    with open("local_model_path.txt", "w") as f:
        f.write(model_dir)
except Exception as e:
    print("Error downloading model:", e)
