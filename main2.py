import sys
import getopt
import wave
import pyaudio
import numpy as np
from log import setup_logger

logger = setup_logger("audioviz")

FPS = 60


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
        stream.write(data)
        data = wavefile.readframes(chunk)

        # TODO: create video frame from data
        handle_chunk(data)

    # Cleanup
    wavefile.close()
    stream.close()
    pa.terminate()


def handle_chunk(data, dtype):
    logger.info("Handling frame")
    sig = np.frombuffer(data, type=dtype)


if __name__ == "__main__":
    main(sys.argv[1:])
