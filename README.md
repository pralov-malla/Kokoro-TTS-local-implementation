# Kokoro TTS Local Implementation

Local experiments for running Kokoro TTS on-device, plus a real-time conversational orchestration flow that streams GPT text into speech.

This repository is especially focused on:

- Realtime text + speech orchestration (`test/03_realtime_tts_orchestration`)
- Comparing perceived responsiveness between streaming vs full-sentence synthesis
- Reproducible local setup with `uv` and `uv sync`

## What This Project Contains

- Baseline Kokoro generation (`main.py`)
- Voice blending experiments (`test/01_voice_blending/voice_blending.py`)
- Alignment and phrase extraction pipeline (`test/02_test_align_and_cut/*`)
- Realtime conversational TTS orchestration (`test/03_realtime_tts_orchestration/*`)

## Project Structure

```text
.
├─ main.py
├─ pyproject.toml
├─ uv.lock
├─ README.md
├─ test/
│  ├─ 01_voice_blending/
│  │  └─ voice_blending.py
│  ├─ 02_test_align_and_cut/
│  │  ├─ 01_generate_audio.py
│  │  ├─ 02_get_timestamps.py
│  │  └─ 03_extract_and_merge.py
│  └─ 03_realtime_tts_orchestration/
│     ├─ __init__.py
│     ├─ conversation_streaming.py
│     ├─ full_sentence_synthesize.py
│     ├─ gpt_response.py
│     └─ kokoro_engine.py
└─ test_generated_sounds/
```

## Core Realtime Folder (Important)

`test/03_realtime_tts_orchestration` has two interaction modes:

1. `conversation_streaming.py`
   Streams GPT output token-by-token and feeds it directly into `RealtimeTTS` + Kokoro.

2. `full_sentence_synthesize.py`
   Waits for a complete GPT response, then synthesizes and plays it.

Both paths report a `Kokoro latency` value in milliseconds.

### Internal Flow

- `gpt_response.py`
  Handles chat state and OpenAI calls (`complete_response` and `stream_response`).
- `kokoro_engine.py`
  Extends `RealtimeTTS.KokoroEngine` and instruments first audio chunk timing.
- `conversation_streaming.py`
  Uses streamed text + streaming synthesis.
- `full_sentence_synthesize.py`
  Uses full response + single synthesis phase.

## Requirements

- Python `>=3.11`
- `uv` (dependency + environment manager)
- Windows is currently the tested environment
- Optional NVIDIA GPU for faster TTS/ML workloads

## Setup With uv (Recommended)

### 1) Install uv

Choose one:

```powershell
winget install --id=astral-sh.uv -e
```

or

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```bash
uv --version
```

### 2) Sync Dependencies (`uv sync`)

From the project root:

```bash
uv sync
```

What `uv sync` does here:

- Creates/updates `.venv`
- Resolves and installs dependencies from `pyproject.toml`
- Uses `uv.lock` for reproducibility when present

### 3) Configure API Key

Create a local `.env` file in project root:

```env
OPENAI_API_KEY=your_key_here
```

The realtime scripts load this via `python-dotenv` in `gpt_response.py`.

### 4) Run Without Manual Activation

Use `uv run` (preferred):

```bash
uv run main.py
```

Manual activation is optional:

```bash
source .venv/Scripts/activate
```

## Realtime Orchestration Usage

### Streaming Mode (faster perceived response)

```bash
uv run test/03_realtime_tts_orchestration/conversation_streaming.py
```

Commands inside the app:

- `reset` clears conversation memory
- `exit` or `quit` stops the app

### Full-Sentence Mode (simpler, less overlap)

```bash
uv run test/03_realtime_tts_orchestration/full_sentence_synthesize.py
```

Commands inside the app are the same (`reset`, `exit`, `quit`).

## Latency Comparison (Streaming vs Full Sentence)

If you want a direct comparison, use this protocol.

### Metric

Use the printed value:

- `Kokoro latency: <N> ms`

This approximates time to first synthesized audio chunk after synthesis starts.

### Method (Reproducible)

1. Run each mode separately.
2. Use the same 10 user prompts for both runs.
3. Ignore the first prompt as warm-up (model/cache initialization effects).
4. Record the next 9 latency values.
5. Compare mean and median.

Example prompt set:

```text
Why do you want to study in the United States?
Why this university?
Who is sponsoring your education?
What is your plan after graduation?
Have you traveled internationally before?
How is this program related to your previous studies?
What is your expected yearly budget?
Why should I trust you will return to your home country?
What are your career goals?
Do you have relatives in the United States?
```

### Expected Trend

- Streaming mode usually feels more responsive because text generation and TTS preparation overlap.
- Full-sentence mode often has longer wait before first sound because synthesis starts only after full LLM completion.

Your exact numbers depend on GPU/CPU, network latency to OpenAI, and first-run warm-up state.

## Other Scripts

### Baseline TTS

```bash
uv run main.py
```

### Voice Blending

```bash
uv run test/01_voice_blending/voice_blending.py
```

### Align and Cut Pipeline

```bash
uv run test/02_test_align_and_cut/01_generate_audio.py
uv run test/02_test_align_and_cut/02_get_timestamps.py
uv run test/02_test_align_and_cut/03_extract_and_merge.py
```

Outputs are written under `test_generated_sounds/`.

## Troubleshooting

- OpenAI auth errors:
  Confirm `.env` exists and `OPENAI_API_KEY` is valid.
- CUDA not available:
  Scripts fall back to CPU where implemented, but performance may be slower.
- Windows audio playback issues:
  `full_sentence_synthesize.py` uses `winsound`; ensure default output device is available.
- Dependency mismatch after updates:
  Re-run `uv sync`.

## Notes

- `.env` and generated audio are intentionally local-only (typically gitignored).
- If you change dependencies in `pyproject.toml`, run `uv sync` again to keep `.venv` in sync.
