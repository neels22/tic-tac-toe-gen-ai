from youtube_transcript_api import YouTubeTranscriptApi

# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts('wm7eqTbCheI')

# iterate over all available transcripts


def getting_yt_text():
    for transcript in transcript_list:
        # print(transcript.fetch())
        # print("="*100 + "this is the text")
        # translating the transcript will return another transcript object
        # print(transcript.translate('en').fetch())
        text = transcript.translate('en').fetch()
        # print("="*100)
        # print(text[0]['text'])
        return text[0]['text']


text = getting_yt_text()

print(text)
