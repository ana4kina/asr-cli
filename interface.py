import tkinter
import pyaudio
import wave
import os
import time
import threading
from tkinter import filedialog
from src.asr_cli.main import cli_entrypoint
from src.preprocessing import visualize, preprocess_audio
from export import copy_text, save_txt, check_wav

FRAME_SIZE = 2048
HOP_SIZE = 512
SAMPLE_RATE = 16_000

class WInterface():

    def __init__(self):
        self.recording = False
        self.file = None
        self.result = None
        self.root = tkinter.Tk()
        self.root.title("Распознавание голоса")
        self.root.geometry("720x256")
        label = tkinter.Label(self.root, text="Файл",
                              font=("Arial", 50, "bold"))
        label.pack(anchor='n', expand=1)
        self.button1 = tkinter.Button(
            text="Выбрать файл",
            font=('Arial', 30),
            command=self.click_path
        )
        self.button1.pack(anchor='n')
        self.button2 = tkinter.Button(
            text="Записать голос",
            font=('Arial', 30),
            command=self.tap_to_rec
        )
        self.button2.pack(anchor='n')
        self.root.mainloop()

    def click_path(self):
        self.file = tkinter.filedialog.askopenfile().name
        check_wav(self.file)
        self.button1.destroy()
        self.button2.destroy()
        self.res_button()

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
        self.res_button()

    def res_button(self):
        self.button4 = tkinter.Button(
            text="Перевести в текст",
            font=('Arial', 30),
            command=self.recognition
        )
        self.button4.pack(anchor='center')

    def recognition(self):
        print(self.file)
        for idx, melspec in enumerate(preprocess_audio(self.file)):
            visualize(melspec, SAMPLE_RATE, idx)
        self.result = cli_entrypoint(self.file)
        self.button4.destroy()
        self.copy_button()
        self.save_txt_button()
        #self.at_start_button()

    def copy_button(self):
        self.copy_butt = tkinter.Button(
            text="Копировать текст",
            font=('Arial', 30),
            command=self.click_copy
        )
        self.copy_butt.pack(anchor='n')

    def save_txt_button(self):
        self.txt_button = tkinter.Button(
            text="Скачать .txt",
            font=('Arial', 30),
            command=self.click_txt
        )
        self.txt_button.pack(anchor='n')

    def click_copy(self):
        copy_text(self.result)
        label = tkinter.Label(self.root, text="Готово!",
                font=("Arial", 20))
        label.pack(anchor='n', expand=1)

    def click_txt(self):
        save_txt(self.result)
        label = tkinter.Label(self.root, text="Готово!",
                font=("Arial", 20))
        label.pack(anchor='n', expand=1)

    #def at_start_button(self):
    #    self.start_butt = tkinter.Button(
    #        text="В начало",
    #        font=('Arial', 30),
    #        command=self.to_start
    #    )
    #    self.start_butt.pack(anchor='n')

    #(self):
    #    if self.recording:
    #        self.recording = False
    #    else:
    #        self.recording = True
            #self.copy_butt.destroy()
            #self.txt_button.destroy()
            #self.start_butt.destroy()
            #self.root.destroy()
            #self.__init__()

WInterface()