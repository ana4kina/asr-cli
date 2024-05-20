import os
import soundfile as sf
import pyperclip
from pydub import AudioSegment


def check_wav(file):
    print(file)
    filename, file_extension = os.path.splitext(file)
    if file_extension != '.wav':
        to_wav(file, filename, file_extension)

def to_wav(file, filename, file_extension):
    if file_extension == '.mp3':
        sound = AudioSegment.from_mp3(file)
        sound.export(file, format="wav")
    elif file_extension == '.ogg':
        data, samplerate = sf.read(file)
        sf.write(filename + ".wav", data, samplerate)    

def copy_text(name):
    pyperclip.copy(name)
    pyperclip.paste()

def save_txt(text):
    with open("result.txt", "w") as output:
        output.write(str(text))
