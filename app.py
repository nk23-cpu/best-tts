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

# ✅ GET + POST dono allow
@app.route("/tts", methods=["GET", "POST"])
def tts():
    if request.method == "POST":
        text = request.json.get("text")
    else:
        text = request.args.get("text")

    if not text:
        return "No text provided", 400

    file_id = str(uuid.uuid4())
    mp3_file = f"{file_id}.mp3"
    wav_file = f"{file_id}.wav"

    # Step 1: TTS
    asyncio.run(generate_tts(text, mp3_file))

    # Step 2: Convert
    subprocess.run([
        "ffmpeg", "-i", mp3_file,
        "-ac", "1", "-ar", "16000",
        wav_file
    ])

    os.remove(mp3_file)

    return send_file(wav_file, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
