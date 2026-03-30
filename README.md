# Kokoro TTS Local Implementation

Local experiments for generating speech with Kokoro TTS and running a small alignment pipeline with faster-whisper.

This project is tested on Windows and includes scripts for:

- Single-text TTS generation
- Voice blending
- Timestamp extraction from generated audio
- Segment extraction and merge flow

## Project Structure

```text
.
├─ main.py
├─ pyproject.toml
├─ uv.lock
├─ test/
│  └─ 01_voice_blending.py
├─ test_align_and_cut/
│  ├─ 01_generate_audio.py
│  ├─ 02_get_timestamps.py
│  └─ 03_extract_and_merge.py
└─ test_generated_sounds/
```

## Requirements

- Python 3.11+
- uv
- NVIDIA GPU optional (CPU fallback is supported in timestamp script)

## Setup

1. Create and sync environment:

```bash
uv sync
```

2. (Optional) Activate virtual environment:

```bash
source .venv/Scripts/activate
```

## Run Scripts

Generate baseline Kokoro output:

```bash
uv run main.py
```

Generate blended voice sample:

```bash
uv run test/01_voice_blending.py
```

Alignment and cut pipeline:

```bash
uv run test_align_and_cut/01_generate_audio.py
uv run test_align_and_cut/02_get_timestamps.py
uv run test_align_and_cut/03_extract_and_merge.py
```

## Output Folder

Generated audio/json files are written into:

- test_generated_sounds/

## Git Ignore Notes

The following paths are currently ignored by .gitignore:

- .env
- test_generated_sounds/
- data/

Meaning:

- .env stays local for secrets/tokens.
- test_generated_sounds/ is treated as generated output and not tracked.
- data/ is reserved for local datasets or intermediate files and not tracked.

## Troubleshooting

If faster-whisper errors with missing cublas64_12.dll on Windows, the timestamp script will fall back to CPU automatically.
