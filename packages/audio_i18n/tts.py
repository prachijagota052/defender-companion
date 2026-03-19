import asyncio
import edge_tts
import pygame
import os

# Mapping for high-quality Neural voices
VOICE_MAP = {
    "en": "en-US-GuyNeural",
    "hi": "hi-IN-MadhurNeural",
    "mr": "mr-IN-AarohiNeural"
}

async def _stream_speech(text, lang):
    voice = VOICE_MAP.get(lang, "en-US-GuyNeural")
    communicate = edge_tts.Communicate(text, voice)
    
    # Save to a temporary file
    temp_file = "temp_alert.mp3"
    await communicate.save(temp_file)
    
    # Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    
    pygame.mixer.quit()
    if os.path.exists(temp_file):
        os.remove(temp_file)

def speak(text, lang="en", enabled=True, **kwargs):
    """The main entry point called by service.py"""
    if not enabled or not text.strip():
        return
        
    try:
        asyncio.run(_stream_speech(text, lang))
    except Exception as e:
        print(f"TTS Error: {e}")
