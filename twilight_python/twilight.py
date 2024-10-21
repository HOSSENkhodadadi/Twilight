import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

import os
from groq import Groq

import asyncio
import edge_tts

import pygame, sys, time 

# print("1 = The first section")
# print("2 = The second section")
# print("x = exit")
# while True:
#     user_input = input("Command: ")
#     if user_input == "1":
#         pygame.mixer.music.load("twilight/1.wav")
#         pygame.mixer.music.play()

#     if user_input == "2":
#         pygame.mixer.music.load("twilight/2.wav")
#         pygame.mixer.music.play()

#     if user_input == "x":
#         sys.exit()

# pygame.mixer.music.unload()
# pygame.mixer.music.play(loops = 0, start = 2, fade_ms = 2000)
# pygame.mixer.music.rewind()
# pygame.mixer.music.stop()
# pygame.mixer.music.unpause()
# pygame.mixer.music.fadeout(1000)
# pygame.mixer.music.get_volume()
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.get_pos()
# pygame.mixer.music.set_pos(10)
# pygame.mixer.music.queue("song2.mp3")

print(70 * "#")
print("***** Playing the story ****")
pygame.mixer.init()
pygame.mixer.music.load("twilight/1.wav")
pygame.mixer.music.play()
input("Enter to exit the section 1")
pygame.mixer.music.load("twilight/2.wav")
pygame.mixer.music.play()
input("Enter to exit the section 2")
pygame.mixer.music.stop()

print(70 * "#")
print("***** Recording the user response ****")
import time
def record_audio(output_file, duration=5, rate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    
    # Countdown timer
    for remaining in range(duration, 0, -1):
        mins, secs = divmod(remaining, 60)  # Divide into minutes and seconds
        timer = f'Time remaining: {mins:02d}:{secs:02d}'  # Format MM:SS
        print(timer, end="\r")  # Print countdown on the same line
        time.sleep(1)  # Wait for 1 second
    
    sd.wait()  # Wait until the recording is finished
    print("\nFinished recording.")
    
    # Save the audio to a WAV file
    wav.write(output_file, rate, recording)

# Record 5 seconds of audio and save to 'user_response.wav'
duration = input("How much time do you need to response?")
duration  = int(duration)
record_audio('user_response.wav', duration=duration)
print(70 * "#")
print("***** Transcribing the response ****")

# Initialize the Groq client
client = Groq()

# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/user_response.wav" # Replace with your audio file!

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()), # Required audio file
      model="whisper-large-v3-turbo", # Required model to use for transcription
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      language="en",  # Optional
      temperature=0.0  # Optional
    )
    # Print the transcription text
    # print("\n", transcription.text, "\n")

    response = transcription.text

print(response)

print(70 * "#")
print("***** Generating the prompt ****")


context = """personality Interaction: On the second day of her travels, Hypatia encounters a confident and sharp-tongued merchant. He stands tall at the market, haggling with customers and negotiating deals with ease. As their paths cross, the merchant challenges Hypatia to a debate about ethics in trade.

“Ah, a philosopher!” he says with a smirk. “What do you know of trade and business, living in your ivory tower?”

Teaching the Skill: "Ad hominem," I think to myself. This is a classic example of attacking me instead of addressing the topic at hand. It’s not about me or my background—it’s about the validity of the argument. You see, when someone makes a personal attack instead of engaging with the issue, they are trying to shift the focus away from the real debate. It’s a tactic to avoid the core of the discussion. In situations like these, I must remind myself and my opponent to focus on the argument, not the individual.

Challenge: The merchant leans forward and sneers, "You philosophers sit in your libraries and dream of ideal worlds. How can you even begin to understand ethics when you’ve never sold a thing in your life?"

“I am Lucius, and I’ve spent years building my trade. You think you can lecture me about fairness? Let’s see you argue ethics when you know nothing about business.”"""
question = """ How would I respond to Lucius' personal attack? Can you think of a way to refocus the conversation on the ethical principles without allowing his words to undermine my position?"""

response1 = """ well, I think Hypatia background in the trade has nothing to do with her ability in ethics in trade you can gain knowledge through reading and studying the books, of course real world eperience can improve her knowledge but not quite necessary, I believe the merchant is attacking on Hypatia herself rather than challenging her knowledge """
prompt = f"given the context and the question tell the user if his response is reasonable then explain the reason for him, remember the user is answering instead of the hypatia,  context: {context}, question:{question}, response: {response}"

# print(prompt)

# !export  GROQ_API_KEY = "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"
#export GROQ_API_KEY="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"

print(70 * "#")
print("***** LLama is responding ****")

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
        
    ],
    model="llama3-8b-8192",
)

# print(chat_completion.choices[0].message.content)   


print(70 * "#")
print("***** Generating audio response ****")

VOICES = ['en-AU-NatashaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 
          'en-CA-LiamNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural']
TEXT = chat_completion.choices[0].message.content
VOICE = VOICES[0]
OUTPUT_FILE = "hypatia_asyncio_3.mp3"

async def amain() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
    loop.run_until_complete(amain())
finally:
    loop.close()

print(70 * "#")
print("***** Listen to llama response to your answer ****")
pygame.mixer.music.load("hypatia_asyncio_3.mp3")
pygame.mixer.music.play()
input("Enter to exit")
