import json, re
from pathlib import Path
from pydub import AudioSegment

DIR = Path("test_generated_sounds")

CLIPS = [
    ("text1.wav", "text1.json", "Hello I am",                     0, 0),
    ("text2.wav", "text2.json", "George Clinton and I am here to", 0, 0),
]
FULL_APPEND  = "text3.wav"
FADE_MS      = 8
CROSSFADE_MS = 40
FINAL_OUT    = "final_output.wav"


def clean(text):
    return re.sub(r"[^\w\s']", "", text.lower()).split()


def find_phrase(words, phrase):
    tokens, source_index = [], []
    for i, w in enumerate(words):
        for token in clean(w["word"]):
            tokens.append(token)
            source_index.append(i)
    target = clean(phrase)
    n = len(target)
    for i in range(len(tokens) - n + 1):
        if tokens[i:i + n] == target:
            return source_index[i], source_index[i + n - 1]
    raise ValueError(f"Phrase not found: {phrase!r} in {tokens}")


def extract_clip(wav, jsn, phrase, pad_start_ms, pad_end_ms):
    audio = AudioSegment.from_wav(DIR / wav)
    words = json.loads((DIR / jsn).read_text())
    start_word, end_word = find_phrase(words, phrase)
    start_ms = words[start_word]["start"] * 1000
    end_ms   = words[end_word]["end"]     * 1000
    clip = audio[start_ms - pad_start_ms : end_ms + pad_end_ms]
    return clip.fade_in(FADE_MS).fade_out(FADE_MS)


# --- assemble ---

parts = [extract_clip(*row) for row in CLIPS]

if FULL_APPEND:
    full = AudioSegment.from_wav(DIR / FULL_APPEND)
    parts.append(full.fade_in(FADE_MS).fade_out(FADE_MS))

result = parts[0]
for part in parts[1:]:
    result = result.append(part, crossfade=CROSSFADE_MS)

result.export(DIR / FINAL_OUT, format="wav")
print(f"saved → {DIR / FINAL_OUT}")