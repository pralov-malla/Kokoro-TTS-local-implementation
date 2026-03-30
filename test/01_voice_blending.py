import soundfile as sf
import torch
from pathlib import Path
from kokoro import KPipeline


OUTPUT_DIR = Path("test_generated_sounds")
OUTPUT_DIR.mkdir(exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("CUDA:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

pipeline = KPipeline(lang_code="a", device=DEVICE)


def mix_voices(pipeline, voice_names, weights=None):
    voices = [pipeline.load_voice(v) for v in voice_names]

    if weights is None:
        weights = [1.0] * len(voices)

    total = sum(weights)
    weights = [w / total for w in weights]

    mixed = sum(w * v for w, v in zip(weights, voices))
    return mixed


mixed_voice = mix_voices(
    pipeline,
    ["bf_emma", "af_nicole"],
    weights=[0.5, 0.5],
)

texts = [
    "Hello. I am Pratik Lama and I am here to take your visa interview. I will ask you a few questions and you have to answer them. Are you ready?",
    "This is the second sentence.",
    "And this is the third one.",
]

for text_idx, text in enumerate(texts):
    print(f"\nGenerating for text {text_idx}: {text}")

    for chunk_idx, (gs, ps, audio) in enumerate(
        pipeline(
            text,
            voice=mixed_voice,
            speed=1,
            split_pattern=r"\n+",
        )
    ):
        print(f"Text {text_idx} - Chunk {chunk_idx}: {gs}")
        sf.write(OUTPUT_DIR / f"mixed_out_t{text_idx}_c{chunk_idx}.wav", audio, 24000)