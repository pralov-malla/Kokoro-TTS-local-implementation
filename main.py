import soundfile as sf
from pathlib import Path
import torch
from kokoro import KPipeline

OUTPUT_DIR = Path("test_generated_sounds")
OUTPUT_DIR.mkdir(exist_ok=True)

print(torch.cuda.is_available(), torch.cuda.get_device_name(0))

pipeline = KPipeline(lang_code="a", device="cuda")

for i, (gs, ps, audio) in enumerate(
    pipeline("Hi, I am pratik lama and I am your visa interview officer.", voice="af_heart")
):
    sf.write(OUTPUT_DIR / f"out_{i}.wav", audio, 24000)