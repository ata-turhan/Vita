import os
import torch
from TTS.api import TTS


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


# List available 🐸TTS models and choose the first one
model_names = TTS().list_models()
for model in model_names:
    print(model)

# model_name = "tts_models/multilingual/multi-dataset/your_tts"
model_name = "tts_models/multilingual/multi-dataset/bark"
# Init TTS
tts = TTS(model_name).to(device)

# Run TTS
# ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language

# Text to speech to a file
tts.tts_to_file(
    text="Hello world, I am ata turhan. I am speaking english!",
    speaker_wav="bark_voices/speaker/ata-88 seconds.wav",
    # language="en",
    file_path="output-88 seconds.wav",
)
