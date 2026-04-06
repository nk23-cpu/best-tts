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

@app.route("/tts", methods=["GET", "POST"])
def tts():
    # 🔥 DEBUG: check request type
    print("\n===== NEW REQUEST =====")

    if request.method == "POST":
        data = request.json
        print("POST DATA:", data)
        text = data.get("text")
    else:
        text = request.args.get("text")
        print("GET TEXT:", text)

    # ❌ check
    if not text:
        print("❌ No text received")
        return "No text provided", 400

    print("✅ FINAL TEXT RECEIVED:", text)

    file_id = str(uuid.uuid4())
    mp3_file = f"{file_id}.mp3"
    wav_file = f"{file_id}.wav"

    # 🎤 Generate TTS
    asyncio.run(generate_tts(text, mp3_file))

    # 🔁 Convert MP3 → WAV
    subprocess.run([
        "ffmpeg", "-i", mp3_file,
        "-ac", "1", "-ar", "16000",
        wav_file
    ])

    os.remove(mp3_file)

    print("🔊 Audio generated & sending back\n")

    return send_file(wav_file, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
