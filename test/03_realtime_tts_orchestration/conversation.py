from gpt_streaming import ConversationManager
from kokoro_engine import create_kokoro_stream


class ConversationApp:
    def __init__(self, voice: str = "af_heart", speed: float = 1.0):
        self.llm = ConversationManager()
        self.stream = create_kokoro_stream(voice=voice, speed=speed)

    def ask(self, user_input: str):
        collected = []
        latency_ms = None

        def text_generator():
            for chunk in self.llm.stream_response(user_input):
                if chunk:
                    print(chunk, end="", flush=True)
                    collected.append(chunk)
                    yield chunk

        def on_first_audio_chunk_prepared(kokoro_latency_ms):
            nonlocal latency_ms
            if latency_ms is None and kokoro_latency_ms is not None:
                latency_ms = kokoro_latency_ms

        print("\nOfficer:", end=" ", flush=True)

        self.stream.engine.on_first_audio_chunk_prepared = on_first_audio_chunk_prepared
        self.stream.feed(text_generator())
        self.stream.play()

        full_text = "".join(collected).strip()
        if full_text:
            self.llm.add_assistant_message(full_text)

        print()
        if latency_ms is not None:
            print(f"Kokoro latency: {latency_ms:.0f} ms")
        return full_text, latency_ms

    def run(self):
        while True:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                break

            if user_input.lower() == "reset":
                self.llm.reset()
                print("Conversation reset.")
                continue

            self.ask(user_input)


if __name__ == "__main__":
    app = ConversationApp()
    app.run()
