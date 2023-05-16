import torch
import whisper

# cuda
model = whisper.load_model("small", device="cpu")
result = model.transcribe("input/test.m4a")

print(result["text"])