import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY missing. Please check your .env file."
    )

client = Groq(api_key=api_key)


def transcribe_audio(audio_file):

    with open(audio_file, "rb") as file:

        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            response_format="text"
        )

    return transcription.strip()
