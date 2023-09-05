import os
import torch
from TTS.api import TTS


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models and choose the first one
model_name = "tts_models/multilingual/multi-dataset/bark"
# Init TTS
tts = TTS(model_name).to(device)

# Run TTS
# ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language

# Text to speech to a file
tts.tts_to_file(
    text="Hello world, I am ata turhan. I am speaking english!",
    speaker_wav="bark_voices/speaker/ata.wav",
    # language="en",
    file_path="output.wav",
)
