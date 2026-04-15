import numpy as np
import soundfile as sf
import torch
from pathlib import Path
from kokoro import KPipeline

OUTPUT_DIR = Path("test_generated_sounds")
OUTPUT_DIR.mkdir(exist_ok=True)

texts = [
    "Hello. I am Pratik Lama",
    "George Clinton and I am here to demonstrate voice blending",
    "take your visa interview",
]

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

pipeline = KPipeline(
    lang_code="a",
    repo_id="hexgrad/Kokoro-82M",
    device=DEVICE,
)
voice = pipeline.load_voice("af_sarah")


def generate_audio(text, path):
    chunks = []
    for _, _, audio in pipeline(text, voice=voice, speed=1):
        chunks.append(np.asarray(audio))
    full_audio = np.concatenate(chunks, axis=0)
    sf.write(path, full_audio, 24000)


for i, text in enumerate(texts, start=1):
    generate_audio(text, OUTPUT_DIR / f"text{i}.wav")

print("done")