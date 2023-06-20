import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import simpleaudio
import yaml
import random
import wavio
import requests
import charset_normalizer.md__mypyc

Fs = 44100  # Sample frequency

def random_key(length, keyid):
    random.seed(keyid)
    key_int = random.randbytes(length)
    return key_int
def encrypt(raw, keyid):
    raw_bytes = raw.encode("utf-8")
    raw_int = int.from_bytes(raw_bytes, "big")
    key_int = random_key(len(raw_bytes), keyid)
    encrypted = raw_int ^ int.from_bytes(key_int, "big")
    encrypted_bytes = int.to_bytes(encrypted, (encrypted.bit_length() + 7) // 8, "big")
    return encrypted_bytes
def decrypt(encrypted, keyid):
    decrypted = int.from_bytes(encrypted, "big")^int.from_bytes(random_key(len(encrypted), keyid), "big")
    decrypted_bytes = int.to_bytes(decrypted, (decrypted.bit_length() + 7) // 8, "big")
    return decrypted_bytes.decode("utf-8")

def FFT(Fs, data):
    L = len(data)
    N = np.power(2, np.ceil(np.log2(L)))  # closes power of two
    result = np.abs(fft(x=data, n=int(N))) / L * 2  # Do FFT using the function
    axisFreq = np.arange(int(N / 2)) * Fs / N  # get the coords
    result = result[range(int(N / 2))]  # Because its symmetric so we cut half off
    return axisFreq, result

print("Loading dictionary...")

try:
    open("dt.yml")
except IOError:
    with open("dt.yml", "w") as fl:
        fl.write(decrypt(requests.get("https://gitee.com/jason31416/files/raw/master/src/fft/dte.yml").content, 13232423))

with open("dt.yml") as fl:
    dt = yaml.safe_load(fl)

def play(f):
    t = np.linspace(0, 0.5, Fs)  # Gen sig
    y = 0
    for i in f:
        y += i[1] * np.sin(2 * np.pi * i[0] * t)
    # fftt(y)

    audio = y * (2 ** 15 - 1) / np.max(np.abs(y))
    audio = audio.astype(np.int16)
    play_obj = simpleaudio.play_buffer(audio, 1, 2, Fs)  # Wait for playback to finish before exiting
    play_obj.wait_done()

def fftt(y):
    # Do fft to the signal
    x, result = FFT(Fs, y)

    # draw da graph xd
    fig2 = plt.figure(figsize=(16, 9))
    plt.title('FFT')
    plt.plot(x, result)
    plt.xlabel('Frequency/Hz')
    plt.ylabel('Amplitude')
    plt.grid()

while True:
    s = input("What do you want to say in Eridian?").replace(",", "").replace(".", "").replace("'s", "").replace("'", "").replace("!", "").replace("?", " question").replace(":", "").replace('"', "").replace("\n", "").split(" ")

    x = 0

    for i in s:
        if i.lower() not in dt:
            dt[i.lower()] = [(random.randint(1, 44000), random.randint(1, 5)) for i in range(random.randint(1, 5))]
            x += 1
        play(dt[i.lower()])

    with open("dt.yml", "w") as fl:
        yaml.safe_dump(dt, fl)