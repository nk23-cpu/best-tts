from flask import Flask, request, send_file
import edge_tts
import asyncio
import uuid
import os
import subprocess

app = Flask(__name__)

VOICE = "en-IN-NeerjaNeural"

async def generate_tts(text, mp3_file):
    communicate = edge_tts.Communicate(text, voice=VOICE)
    await communicate.save(mp3_file)

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text")

    file_id = str(uuid.uuid4())
    mp3_file = f"{file_id}.mp3"
    wav_file = f"{file_id}.wav"

    # Step 1: Edge TTS → MP3
    asyncio.run(generate_tts(text, mp3_file))

    # Step 2: MP3 → WAV (FFmpeg direct)
    subprocess.run([
        "ffmpeg", "-i", mp3_file,
        "-ac", "1", "-ar", "16000",
        wav_file
    ])

    os.remove(mp3_file)

    return send_file(wav_file, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
