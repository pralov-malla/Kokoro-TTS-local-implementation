from time import perf_counter

from RealtimeTTS import TextToAudioStream, KokoroEngine as RealtimeKokoroEngine


class KokoroEngine(RealtimeKokoroEngine):
    def post_init(self):
        self.on_first_audio_chunk_prepared = None
        self._first_audio_chunk_prepared_seen = False
        self._synthesis_started_at = None

        original_put = self.queue.put

        def instrumented_put(item, *put_args, **put_kwargs):
            if not self._first_audio_chunk_prepared_seen:
                self._first_audio_chunk_prepared_seen = True
                if self.on_first_audio_chunk_prepared:
                    if self._synthesis_started_at is not None:
                        latency_ms = (perf_counter() - self._synthesis_started_at) * 1000
                        self.on_first_audio_chunk_prepared(latency_ms)
                    else:
                        self.on_first_audio_chunk_prepared(None)
            return original_put(item, *put_args, **put_kwargs)

        self.queue.put = instrumented_put

    def synthesize(self, text: str, sentence_count: int = 0) -> bool:
        self._first_audio_chunk_prepared_seen = False
        self._synthesis_started_at = perf_counter()
        return super().synthesize(text, sentence_count)


def create_kokoro_stream(voice: str = "af_heart", speed: float = 1.0):
    engine = KokoroEngine(
        voice=voice,
        default_speed=speed,
    )
    return TextToAudioStream(engine=engine)
