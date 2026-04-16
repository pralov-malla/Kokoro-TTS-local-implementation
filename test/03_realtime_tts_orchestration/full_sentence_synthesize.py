import os
import tempfile
import winsound
from time import perf_counter

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

from gpt_response import ConversationManager


def main():
    voice = "af_heart"
    speed = 1.0
    sample_rate = 24000

    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipeline = KPipeline(
        lang_code="a",
        repo_id="hexgrad/Kokoro-82M",
        device=device,
    )
    voice_tensor = pipeline.load_voice(voice)

    llm = ConversationManager()

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break
        if user_input.lower() == "reset":
            llm.reset()
            print("Conversation reset.")
            continue

        full_text = llm.complete_response(user_input)
        if not full_text:
            continue

        print(f"\nOfficer: {full_text}")

        synth_started = perf_counter()
        first_chunk_latency_ms = None
        chunks = []
        for _, _, audio in pipeline(
            full_text,
            voice=voice_tensor,
            speed=speed,
            split_pattern=r"$^",
        ):
            if first_chunk_latency_ms is None:
                first_chunk_latency_ms = (perf_counter() - synth_started) * 1000
            chunks.append(np.asarray(audio))
        if not chunks:
            continue

        audio = np.concatenate(chunks, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            wav_path = temp_wav.name
        try:
            sf.write(wav_path, audio, sample_rate)
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        finally:
            try:
                os.remove(wav_path)
            except OSError:
                pass

        if first_chunk_latency_ms is not None:
            print(f"Kokoro latency: {first_chunk_latency_ms:.0f} ms")


if __name__ == "__main__":
    main()
