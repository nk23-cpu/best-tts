from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import subprocess
import uuid
import os

app = FastAPI()

VOICE = "en-IN-PrabhatNeural"

async def generate_tts(text, filename):
    communicate = edge_tts.Communicate(text, voice=VOICE)
    await communicate.save(filename)

def mp3_to_pcm(mp3_file):
    pcm_file = mp3_file.replace(".mp3", ".pcm")

    command = [
        "ffmpeg",
        "-i", mp3_file,
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "-ac", "1",
        "-ar", "22050",
        pcm_file
    ]

    subprocess.run(command)
    return pcm_file

@app.get("/tts")
async def tts(text: str):

    uid = str(uuid.uuid4())
    mp3_file = f"{uid}.mp3"

    await generate_tts(text, mp3_file)
    pcm_file = mp3_to_pcm(mp3_file)

    def iterfile():
        with open(pcm_file, "rb") as f:
            while chunk := f.read(1024):
                yield chunk

        os.remove(mp3_file)
        os.remove(pcm_file)

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
