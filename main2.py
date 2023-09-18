import sys
import getopt
import wave
import pyaudio
import numpy as np
from log import setup_logger
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import warnings
warnings.filterwarnings("ignore")

logger = setup_logger("audioviz")

FPS = 60
DURATION = 1


def main(argv):
    opts, _ = getopt.getopt(argv, "hi:", ["input="])
    for opt, arg in opts:
        if opt == "-h":
            print("main.py -i <wavefile>")
            sys.exit()
        elif opt in ("-i", "--input"):
            run_from_file(arg)
            return

    run_from_sysaudio()


def run_from_sysaudio():
    logger.info("Running visualizer for system audio")


def run_from_file(filepath):
    logger.info(f"Running visualzer for file: {filepath}")
    wavefile = wave.open(filepath, "rb")
    pa = pyaudio.PyAudio()

    # Sample width in bytes
    sample_width = wavefile.getsampwidth()
    dtype = get_dtype(sample_width)

    format = pa.get_format_from_width(sample_width)
    channels = wavefile.getnchannels()
    rate = wavefile.getframerate()

    # Calculate chunk size
    chunk = int((1 / FPS) * rate)

    logger.info(f"sample width: {sample_width}")
    logger.info(f"format      : {format}")
    logger.info(f"channels    : {channels}")
    logger.info(f"sample rate : {rate}")
    logger.info(f"chunk       : {chunk}")

    stream = pa.open(
        format=format,
        channels=channels,
        rate=rate,
        output=True,
    )

    data = wavefile.readframes(chunk)

    while data:
        # stream.write(data)
        # data = wavefile.readframes(chunk)
        data = wavefile.readframes(DURATION * rate)

        # TODO: create video frame from data
        handle_chunk(data, dtype, rate)
        break

    # Cleanup
    wavefile.close()
    stream.close()
    pa.terminate()


def get_dtype(sample_width: int):
    if sample_width == 1:
        return np.int8
    if sample_width == 2:
        return np.int16
    logger.error(f"Invalid sample width: {sample_width}")
    exit(1)


def handle_chunk(data, dtype, sample_rate):
    T = 1 / sample_rate
    logger.info("Handling frame")
    sig = np.frombuffer(data, dtype)
    left, right = sig[0::2], sig[1::2]

    # LEFT
    left_size = left.size
    fft_sig_abs = abs(fft(left))
    freq_left = np.linspace(0.0, 1.0/(2.0*T), left_size//2)
    amp_left = 2/left_size * np.abs(fft_sig_abs[0:left_size//2])

    # RIGHT
    right_size = right.size
    fft_sig_abs = abs(fft(right))
    freq_right = np.linspace(0.0, 1.0/(2.0*T), right_size//2)
    amp_right = 2/left_size * np.abs(fft_sig_abs[0:right_size//2])

def plot_sig_data(data, dtype, sample_rate):
    T = 1 / sample_rate
    logger.info("Handling frame")
    sig = np.frombuffer(data, dtype)
    left, right = sig[0::2], sig[1::2]


    fig, (plot_a, plot_b, plot_c) = plt.subplots(3)
    plot_a.plot(left)
    plot_a.set_xlabel("sample rate * time")
    plot_a.set_ylabel("energy")

    left_size = left.size
    fft_sig_abs = abs(fft(left))
    xf_left = np.linspace(0.0, 1.0/(2.0*T), left_size//2)
    yf_left = 2/left_size * np.abs(fft_sig_abs[0:left_size//2])
    plot_b.semilogy(xf_left, yf_left)

    plot_b.set_xlabel("Left - Frequency")
    plot_b.set_ylabel("Left - Amplitude")

    plot_c.specgram(left, NFFT=1024, Fs=T, noverlap=900)

    plot_c.set_xlabel("Time")
    plot_c.set_ylabel("Frequency")

    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
