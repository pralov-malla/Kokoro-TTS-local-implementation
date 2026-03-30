import json
from pathlib import Path
from faster_whisper import WhisperModel

OUTPUT_DIR = Path("test_generated_sounds")

model = WhisperModel("small", device="cpu", compute_type="int8")

for i in [1, 2]:
    audio_path = OUTPUT_DIR / f"text{i}.wav"
    if not audio_path.exists():
        print("Missing:", audio_path)
        continue

    print("Transcribing:", audio_path)

    segments, _ = model.transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True,
        vad_filter=True,
    )

    words = []
    for segment in segments:
        if not segment.words:
            continue
        for w in segment.words:
            words.append({
                "word": w.word.strip(),
                "start": float(w.start),
                "end": float(w.end),
            })

    out_path = OUTPUT_DIR / f"text{i}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print("Saved:", out_path)

print("done")