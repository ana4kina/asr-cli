import tkinter
import pyaudio
import wave
import os
import time
import threading
#from tkinter import filedialog
#from src.asr_cli.main import cli_entrypoint
from src.preprocessing import visualize
from src.preprocessing import preprocess_audio

FRAME_SIZE = 2048
HOP_SIZE = 512
SAMPLE_RATE = 16_000

class WInterface():

    def __init__(self):
        self.path = False
        self.recording = False
        self.file = None
        self.root = tkinter.Tk()
        self.root.title("Распознавание голоса")
        self.root.geometry("720x256")
        label = tkinter.Label(self.root, text="Файл",
                              font=("Arial", 50, "bold"))
        label.pack(anchor='n', expand=1)
        self.button1 = tkinter.Button(
            text="Ввести путь",
            font=('Arial', 30),
            command=self.click_path
        )
        self.button1.pack(anchor='n')
        self.button2 = tkinter.Button(
            text="Записать голос",
            font=('Arial', 30),
            command=self.click_recording
        )
        self.button2.pack(anchor='n')
        self.root.mainloop()

    def click_path(self):
        if self.path:
            self.path = False
        else:
            self.path = True
            self.file = tkinter.filedialog.askopenfile().name
            self.button1.destroy()
            self.button2.destroy()
            self.res_buttom()

    def click_recording(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            self.tap_to_rec()

    def tap_to_rec(self):
        self.button3 = tkinter.Button(
            text="Нажмите для записи :)",
            font=('Arial', 30, "bold"),
            command=self.click_handler
        )
        self.button3.pack()
        self.label = tkinter.Label(text='00:00:00')
        self.label.pack()
        self.recording = False

    def click_handler(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=1024,
            # input_device_index = 1
        )

        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(
                text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1

        while exists:
            if os.path.exists(f'records/recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'records/recording{i}.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        self.file = os.path.realpath(f'records/recording{i}.wav')
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.res_buttom()

    def res_buttom(self):
        self.path = False
        self.button4 = tkinter.Button(
            text="Перевести в текст",
            font=('Arial', 30),
            command=self.click_text()
        )
        self.button4.pack(anchor='center')

    def click_text(self):
        if self.path:
            self.path = False
        else:
            self.path = True
            self.recognition()

    def recognition(self):
        print(self.file)
        #cli_entrypoint(self.file)
        for idx, melspec in enumerate(preprocess_audio()):
            visualize(melspec, SAMPLE_RATE, idx)


WInterface()