from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import uuid
import os

app = FastAPI()

VOICE = "en-IN-PrabhatNeural"

@app.get("/tts")
async def tts(text: str):

    uid = str(uuid.uuid4())
    mp3_file = f"{uid}.mp3"

    communicate = edge_tts.Communicate(text, voice=VOICE)
    await communicate.save(mp3_file)

    def iterfile():
        with open(mp3_file, "rb") as f:
            while chunk := f.read(1024):
                yield chunk

        os.remove(mp3_file)

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
