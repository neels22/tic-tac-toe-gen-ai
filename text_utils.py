
# import whisper
from openai import OpenAI

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('api_key')
client = OpenAI(api_key=api_key) 



def get_transcript(path):
    audio_file= open(path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text