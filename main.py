from moviepy.editor import VideoFileClip

from text_utils import get_transcript

from rag_tools import set_open_params, get_completion,create_chunks, get_embedding
import yt_dlp
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ydl_opts = {}  
ydl = yt_dlp.YoutubeDL(ydl_opts)

url=input("Enter the url:") 
info_dict = ydl.extract_info(url, download=True)

downloaded_file=ydl.prepare_filename(info_dict)

video_clip=VideoFileClip(downloaded_file)#genai.mp4
audio_clip=video_clip.audio
audio_clip.write_audiofile("extracted_audio.mp3")
vdo_text = get_transcript("extracted_audio.mp3")

print(vdo_text)

print("Chunks")
text_chunks = create_chunks(vdo_text)
print("Embeddings")
embeddings = []
for chunk in text_chunks:
    embedding = get_embedding(chunk)
    embeddings.append(embedding)

while True:

    user_prompt = input("Enter your query(press 0 to exit):- \n")
    if user_prompt == '0':
        print("Quitting...")
        break
    query_embedding = get_embedding(user_prompt)

    user_prompt_embed_np = np.array(query_embedding).reshape(1,-1)
    similarity_matrix = cosine_similarity(embeddings, user_prompt_embed_np)

    chunk_idx = np.argmax(similarity_matrix)

    context = text_chunks[chunk_idx]

    messages = [
    {
        "role": "system",
        "content": f"""Provide answer to query of the user from the given context:
        {context}.
         If you don't have sufficient information reply with 'I don't know'."""
    },
    {
        "role": "user",
        "content": user_prompt
    }
    ]

    params = set_open_params()
    response = get_completion(messages= messages, params= params)

    print(response)

