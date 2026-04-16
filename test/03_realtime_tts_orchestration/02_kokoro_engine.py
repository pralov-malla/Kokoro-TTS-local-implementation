from RealtimeTTS import KokoroEngine, TextToAudioStream

engine = KokoroEngine()
stream = TextToAudioStream(engine)
stream.feed("Hello world! How are you today?")
stream.play_async()

