import asyncio
import os
import tempfile

import edge_tts
import pygame

VOICE_MAP = {
    "en": "en-US-GuyNeural",
    "hi": "hi-IN-MadhurNeural",
    "mr": "mr-IN-AarohiNeural",
}


async def _save_audio(text: str, lang: str, out_file: str):
    voice = VOICE_MAP.get(lang, "en-US-GuyNeural")
    print(f"[TTS] lang={lang}, voice={voice}")
    print(f"[TTS TEXT] {text[:150]}")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_file)


def speak_interruptible(text, lang="en", enabled=True, stop_checker=None):
    if not enabled or not text.strip():
        return True

    temp_file = None
    try:
        fd, temp_file = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        asyncio.run(_save_audio(text, lang, temp_file))

        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print("[TTS ERROR] MP3 not created properly")
            return False

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        print("[TTS] Playback started")

        while pygame.mixer.music.get_busy():
            if stop_checker and stop_checker():
                pygame.mixer.music.stop()
                print("[TTS] Playback interrupted")
                return False
            pygame.time.wait(100)

        print("[TTS] Playback finished")
        return True

    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return False

    finally:
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        try:
            pygame.mixer.quit()
        except Exception:
            pass

        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass