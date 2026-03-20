import asyncio
import edge_tts

TEXT = "नमस्ते। यह एक हिंदी आवाज़ परीक्षण है।"
VOICE = "hi-IN-MadhurNeural"
OUT = "hi_test.mp3"

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUT)
    print("saved", OUT)

asyncio.run(main())