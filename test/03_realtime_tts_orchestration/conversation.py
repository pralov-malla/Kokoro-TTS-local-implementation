from time import perf_counter

from gpt_streaming import ConversationManager
from kokoro_engine import create_kokoro_stream


class ConversationApp:
    def __init__(self, voice: str = "af_heart", speed: float = 1.0):
        self.llm = ConversationManager()
        self.stream = create_kokoro_stream(voice=voice, speed=speed)

    def ask(self, user_input: str):
        collected = []
        started_at = perf_counter()
        first_chunk_at = None

        def text_generator():
            nonlocal first_chunk_at
            for chunk in self.llm.stream_response(user_input):
                if chunk:
                    now = perf_counter()
                    if first_chunk_at is None:
                        first_chunk_at = now
                        latency_ms = (first_chunk_at - started_at) * 1000
                        print(f"[latency: {latency_ms:.0f} ms] ", end="", flush=True)
                    print(chunk, end="", flush=True)
                    collected.append(chunk)
                    yield chunk

        print("\nOfficer:", end=" ", flush=True)

        self.stream.feed(text_generator())
        self.stream.play()

        full_text = "".join(collected).strip()
        if full_text:
            self.llm.add_assistant_message(full_text)

        print()
        if first_chunk_at is None:
            print("Latency: no speakable chunk returned")

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
