from RealtimeTTS import TextToAudioStream, KokoroEngine


def create_kokoro_stream(voice: str = "af_heart", speed: float = 1.0):
    engine = KokoroEngine(
        voice=voice,
        default_speed=speed,
    )
    return TextToAudioStream(engine=engine)