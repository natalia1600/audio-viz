import sys
import getopt
import wave
import pyaudio
import numpy as np
from log import setup_logger
import matplotlib.pyplot as plt

logger = setup_logger("audioviz")

FPS = 60
DURATION = 30


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
    logger.info("Handling frame")
    sig = np.frombuffer(data, dtype)

    plt.figure(1)

    plot_a = plt.subplot(211)
    plot_a.plot(sig)
    plot_a.set_xlabel("sample rate * time")
    plot_a.set_ylabel("energy")

    plot_b = plt.subplot(212)
    plot_b.specgram(sig, NFFT=1024, Fs=sample_rate, noverlap=900)
    plot_b.set_xlabel("Time")
    plot_b.set_ylabel("Frequency")

    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
